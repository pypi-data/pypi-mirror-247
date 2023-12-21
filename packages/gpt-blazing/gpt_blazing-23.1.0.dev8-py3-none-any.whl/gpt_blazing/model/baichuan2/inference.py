from typing import Optional, Callable, Any, Sequence, Tuple
import logging
import random

import torch
import attrs
import iolite as io

from gpt_blazing.model.interface import ModelInference, QuantizationMode, Role
from .model import (
    load_model,
    model_prefill_2048,
    model_prefill_4096,
    compile_model_prefill,
    model_decode_one_token_2048,
    model_decode_one_token_4096,
    compile_model_decode_one_token,
    model_dispatch,
    model_get_cache,
    model_set_cache,
    Baichuan2ModelConfig,
)
from .tokenizer import Baichuan2Tokenizer

logger = logging.getLogger(__name__)


def timed(fn):  # type: ignore
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()  # type: ignore
    result = fn()
    end.record()  # type: ignore
    torch.cuda.synchronize()
    return result, start.elapsed_time(end) / 1000


LRU_CACHE_PREV, LRU_CACHE_NEXT, LRU_CACHE_KEY, LRU_CACHE_VALUE = 0, 1, 2, 3


class LruCache:

    def __init__(self, capacity: int):
        self.capacity = capacity

        root = []
        root[:] = [root, root, None, None]
        self.root = root

        self.cache = {}

    def get(self, key: str):
        link = self.cache.get(key)
        if link is None:
            return None

        # Move link to tail.
        link_prev, link_next, _key, value = link
        assert key == _key

        link_prev[LRU_CACHE_NEXT] = link_next
        link_next[LRU_CACHE_PREV] = link_prev

        last = self.root[LRU_CACHE_PREV]
        last[LRU_CACHE_NEXT] = self.root[LRU_CACHE_PREV] = link
        link[LRU_CACHE_PREV] = last
        link[LRU_CACHE_NEXT] = self.root

        return value

    def set(self, key: str, value: Any):
        assert key not in self.cache
        if len(self.cache) >= self.capacity:
            # Use the old root to store the new key and result.
            old_root = self.root
            old_root[LRU_CACHE_KEY] = key
            old_root[LRU_CACHE_VALUE] = value

            self.root = old_root[LRU_CACHE_NEXT]
            old_key = self.root[LRU_CACHE_KEY]
            self.root[LRU_CACHE_KEY] = self.root[LRU_CACHE_VALUE] = None

            del self.cache[old_key]
            self.cache[key] = old_root

        else:
            # Add a new node.
            last = self.root[LRU_CACHE_PREV]
            link = [last, self.root, key, value]
            last[LRU_CACHE_NEXT] = self.root[LRU_CACHE_PREV] = self.cache[key] = link


@attrs.define
class Baichuan2ModelInferenceConfig:
    model_folder: str
    model_config: Baichuan2ModelConfig = attrs.field(factory=Baichuan2ModelConfig)
    quantization_mode: QuantizationMode = QuantizationMode.INT8
    device: str = 'cuda:0'
    cache_capacity: int = 20
    use_dynamic_dispatch: bool = True
    skip_torch_compile: bool = False


class Baichuan2ModelInference(ModelInference[Baichuan2ModelInferenceConfig]):

    def __init__(
        self,
        config: Baichuan2ModelInferenceConfig,
        func_process_model: Optional[Callable[[Any], None]] = None,
    ):
        super().__init__(config, func_process_model)

        self.device = config.device
        self.model_max_length = 4096

        # For cache.
        self.cached_system: Optional[str] = None
        self.lru_cache = LruCache(config.cache_capacity)
        self.model_is_loaded = False
        self.model_is_compiled = False

    def load_model(self, device: Optional[str] = None) -> None:
        if device:
            self.device = device

        logger.info(
            f'Initializing Baichuan2Inference(config={self.config}), '
            f'device={self.device}'
        )

        model_fd = io.folder(self.config.model_folder, exists=True)

        # TODO: support more modes.
        assert self.config.quantization_mode == QuantizationMode.INT8

        model_pt = str(model_fd / f'{self.config.quantization_mode.value}.pt')
        logger.info(f'Loading model_pt={model_pt}')
        self.model = load_model(model_pt=model_pt, config=self.config.model_config, int8=True)
        logger.info('Model loaded.')

        tokenizer_model = str(model_fd / 'tokenizer.model')
        logger.info(f'Loading tokenizer_model={tokenizer_model}')
        self.tokenizer = Baichuan2Tokenizer(tokenizer_model)
        logger.info('Tokenizer loaded.')

        logger.info(f'Moving model to device={self.device}')
        self.model = self.model.to(self.device)

        if self.func_process_model is not None:
            logger.info('func_process_model is set, calling func_process_model(self.model)...')
            self.func_process_model(self.model)

        self.model_is_loaded = True

    def compile_model(self) -> None:
        assert self.model_is_loaded

        if self.config.skip_torch_compile:
            logger.info('skip_torch_compile is set, abort. (only for debugging)')

            self.prefill_4096 = model_prefill_4096
            self.decode_one_token_4096 = model_decode_one_token_4096

            self.prefill_2048 = None
            self.decode_one_token_2048 = None

            self.model_is_compiled = True
            return

        logger.info('Compiling model...')

        self.prefill_4096 = compile_model_prefill(model_prefill_4096)
        self.decode_one_token_4096 = compile_model_decode_one_token(model_decode_one_token_4096)

        self.prefill_2048 = None
        self.decode_one_token_2048 = None

        if self.config.use_dynamic_dispatch:
            self.prefill_2048 = compile_model_prefill(model_prefill_2048)
            self.decode_one_token_2048 = compile_model_decode_one_token(model_decode_one_token_2048)

        self.trigger_model_compilation()

        self.model_is_compiled = True

    def model_is_ready(self) -> bool:
        return self.model_is_compiled

    def trigger_model_compilation(self):
        import torch._dynamo.config
        import torch._inductor.config

        torch._inductor.config.coordinate_descent_tuning = True
        torch._inductor.config.triton.unique_kernel_names = True
        torch._inductor.config.fx_graph_cache = True

        logger.info('Trigger prefill compilation.')
        input_ids = torch.tensor([self.tokenizer.tokenize('随便写点什么')], dtype=torch.int)
        input_ids = input_ids.to(self.device)

        for offset in [0, 2048]:
            logger.info(f'offset={offset}')
            for idx in range(5):
                input_pos = torch.arange(
                    offset,
                    offset + int(input_ids.shape[1]),
                    device=input_ids.device,
                    dtype=torch.int,
                )
                _, num_seconds = timed(
                    lambda: model_dispatch(
                        model=self.model,
                        func_2048=self.prefill_2048,
                        func_4096=self.prefill_4096,
                        input_pos=input_pos,
                        input_ids=input_ids,
                    )
                )
                logger.info(f'[{idx}]: prefill compilation: {num_seconds}s.')

        logger.info('Trigger decode_one_token compilation.')
        for offset in [0, 2048]:
            logger.info(f'offset={offset}')
            for idx in range(5):
                input_pos = torch.tensor([offset + idx], device=self.device, dtype=torch.int)
                input_ids = torch.tensor(
                    [[random.randint(0, self.config.model_config.vocab_size)]],
                    dtype=torch.int,
                    device=self.device,
                )

                _, num_seconds = timed(
                    lambda: model_dispatch(
                        model=self.model,
                        func_2048=self.decode_one_token_2048,
                        func_4096=self.decode_one_token_4096,
                        input_pos=input_pos,
                        input_ids=input_ids,
                    )
                )
                logger.info(f'[{idx}]: decode_one_token compilation: {num_seconds}s.')

    def get_eos_token(self):
        return self.tokenizer.eos_token_id

    def get_model_max_length(self):
        return self.model_max_length

    def get_hidden_size(self):
        return self.config.model_config.hidden_size

    def model_prefill(self, rounds: Sequence[Tuple[Role, str]], cache_system: bool = False):
        input_ids = None
        system = None
        num_system_tokens = 0
        begin = 0
        initialized = False

        if cache_system:
            system = None
            if rounds[0][0] == Role.SYSTEM:
                system = rounds[0][1]

            if system:
                cache = self.lru_cache.get(system)
                if cache is not None:
                    num_system_tokens, attn_cache = cache
                    # Cache hit.
                    if system != self.cached_system:
                        # Need to move the cache to model.
                        model_set_cache(self.model, num_system_tokens, attn_cache)
                        self.cached_system = system

                    # Skip tokenizing system.
                    input_ids, _, _num_system_tokens = self.tokenizer.chat_tokenize(rounds[1:])
                    assert _num_system_tokens == 0
                    begin = num_system_tokens

                    initialized = True

        if not initialized:
            input_ids, system, num_system_tokens = self.tokenizer.chat_tokenize(rounds)
            # Invalidate the model cache.
            self.cached_system = None

        assert input_ids

        end = begin + len(input_ids)
        if end >= self.model_max_length:
            return None

        input_pos = torch.arange(begin, end, device=self.device, dtype=torch.int)
        input_ids = torch.tensor([input_ids], dtype=torch.int, device=self.device)
        logits, hidden_states = model_dispatch(
            model=self.model,
            func_2048=self.prefill_2048,
            func_4096=self.prefill_4096,
            input_pos=input_pos,
            input_ids=input_ids,
        )

        if cache_system and system and self.cached_system is None:
            # Add to cache.
            self.cached_system = system
            self.lru_cache.set(
                system,
                (num_system_tokens, model_get_cache(self.model, num_system_tokens)),
            )

        return logits, hidden_states, end

    def model_decode_one_token(self, input_pos: torch.Tensor, input_ids: torch.Tensor):
        logits, hidden_states = model_dispatch(
            model=self.model,
            func_2048=self.decode_one_token_2048,
            func_4096=self.decode_one_token_4096,
            input_pos=input_pos,
            input_ids=input_ids,
        )
        return logits, hidden_states

    def tokenizer_decode(self, tokens: Sequence[int]):
        return self.tokenizer.decode(tokens)

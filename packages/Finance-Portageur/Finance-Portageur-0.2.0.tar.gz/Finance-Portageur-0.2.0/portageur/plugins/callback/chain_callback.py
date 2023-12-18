import logging
import time

from typing import Any, Dict, Union

from langchain.callbacks.base import BaseCallbackHandler
from portageur.plugins.callback.entity.chain import ChainResult

class MainChainCallbackHandler(BaseCallbackHandler):
    raise_error: bool = True

    def __init__(self):
        """Initialize callback handler."""
        self._current_chain_result = None
        self._current_chain_message = None
        self.agent_callback = None

    def clear_chain_results(self) -> None:
        self._current_chain_result = None
        self._current_chain_message = None
        if self.agent_callback:
            self.agent_callback.current_chain = None

    
    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    @property
    def ignore_llm(self) -> bool:
        """Whether to ignore LLM callbacks."""
        return True

    @property
    def ignore_agent(self) -> bool:
        """Whether to ignore agent callbacks."""
        return True
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        if not self._current_chain_result:
            chain_type = serialized['id'][-1]
            if chain_type:
                self._current_chain_result = ChainResult(
                    type=chain_type,
                    prompt=inputs,
                    started_at=time.perf_counter()
                )
                if self.agent_callback:
                    self.agent_callback.current_chain = self._current_chain_message

    def on_chain_end(self, outputs, **kwargs) -> None:
        """Print out that we finished a chain."""
        if self._current_chain_result and self._current_chain_result.status == 'chain_started':
            self._current_chain_result.status = 'chain_ended'
            self._current_chain_result.completion = outputs
            self._current_chain_result.completed = True
            self._current_chain_result.completed_at = time.perf_counter()
            self.clear_chain_results()

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        logging.debug("Dataset tool on_chain_error: %s", error)
        self.clear_chain_results()
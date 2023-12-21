from asyncio import iscoroutinefunction
from asyncio import sleep as asleep
from functools import wraps
from time import sleep
from typing import Any

from langchain.callbacks import get_openai_callback
from langchain.callbacks.openai_info import OpenAICallbackHandler
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage
from rich import print

from ..exceptions import ParsingRetryException
from ..settings import FuncchainSettings
from .function_frame import get_parent_frame


def retry_parse(fn: Any) -> Any:
    """
    Retry parsing the output for a given number of times.

    Raises:
    - OutputParserException: If the output cannot be parsed.
    """
    if iscoroutinefunction(fn):

        @wraps(fn)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            memory: BaseChatMessageHistory = args[3]
            settings: FuncchainSettings = args[4]
            retry = settings.retry_parse
            for r in range(retry):
                try:
                    return await fn(*args, **kwargs)
                except ParsingRetryException as e:
                    _handle_error(e, r, retry, memory)
                    await asleep(settings.retry_parse_sleep + r)
                except OutputParserException as e:
                    if e.llm_output:
                        _handle_error(
                            ParsingRetryException(
                                e.observation,
                                e.llm_output,
                                e.send_to_llm,
                                message=AIMessage(content=e.llm_output),
                            ),
                            r,
                            retry,
                            memory,
                        )
                        sleep(settings.retry_parse_sleep + r)
                    else:
                        raise e

        return async_wrapper

    else:

        @wraps(fn)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            memory: BaseChatMessageHistory = args[3]
            settings: FuncchainSettings = args[4]
            retry = settings.retry_parse
            for r in range(retry):
                try:
                    return fn(*args, **kwargs)
                except ParsingRetryException as e:
                    _handle_error(e, r, retry, memory)
                    sleep(settings.retry_parse_sleep + r)
                except OutputParserException as e:
                    if e.llm_output:
                        _handle_error(
                            ParsingRetryException(
                                e.observation,
                                e.llm_output,
                                e.send_to_llm,
                                message=AIMessage(content=e.llm_output),
                            ),
                            r,
                            retry,
                            memory,
                        )
                        sleep(settings.retry_parse_sleep + r)
                    else:
                        raise e

        return sync_wrapper


def _handle_error(
    e: ParsingRetryException,
    r: int,
    retry: int,
    memory: BaseChatMessageHistory,
) -> None:
    """handle output parser exception retry"""
    print(f"[bright_black]Retrying due to:\n{e}[/bright_black]")
    # remove last retry from memory
    if isinstance(m := memory.messages[-1].content, str):
        if m.startswith("I got this error:") and m.endswith("Can you retry?"):
            memory.messages.pop(), memory.messages.pop()

    memory.add_message(e.message)
    memory.add_user_message(
        "I got this error when trying to parse your json:"
        f"\n```\n{e}\n```\n"
        "Can you rewrite it so I do not get this again?"
    )

    if r == retry - 1:
        raise e


def log_openai_callback(fn: Any) -> Any:
    if not iscoroutinefunction(fn):

        @wraps(fn)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            with get_openai_callback() as cb:
                result = fn(*args, **kwargs)
                _log_cost(cb, name=get_parent_frame(4).function)
                return result

        return sync_wrapper

    else:

        @wraps(fn)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            with get_openai_callback() as cb:
                result = await fn(*args, **kwargs)
                _log_cost(cb, name=get_parent_frame(4).function)
                return result

        return async_wrapper


def _log_cost(cb: OpenAICallbackHandler, name: str) -> None:
    if cb.total_tokens != 0:
        total_cost = f"/ {cb.total_cost:.3f}$ " if cb.total_cost > 0 else ""
        if total_cost == "/ 0.000$ ":
            total_cost = "/ 0.001$ "
        print(
            "[bright_black]"
            f"{cb.total_tokens:05}T {total_cost}- {name}"
            "[/bright_black]"
        )

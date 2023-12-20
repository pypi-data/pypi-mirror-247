from termcolor import colored
import websockets
import json
from molang.models import Memory, Message, Messages, PromptChain, OpenAIChatModel, OpenAIFunction, LLMOutputFunctionParser, ChainFunc, OpenAIConfig, ChainType
from typing import Callable, Any, Optional 
from pydantic import BaseModel
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
 

import openai

def add_message(message: Optional[Message] = None, callback: Optional[Callable[[Any], Any]] = None, prompt_chain: ChainType = PromptChain):
    """Closure to add a message."""
    def _inner(memory: Memory):
        if not message:
            return prompt_chain(memory)
        updated_mem = Memory(messages=memory.messages + [message], state= memory.state)
        if callback:
            callback(updated_mem)
        return prompt_chain(updated_mem)
    return _inner

def add_user_input():
    """Closure to add a user input message."""
    def _inner(memory: Memory):
        inp = input("Enter user input: ")
        user_input = Message("user", inp)
        return add_message(user_input)(memory)
    return _inner

def async_add_message(message: Optional[Message] = None, callback: Optional[Callable[[Any], Any]] = None):
    """Closure to add a message."""
    async def _inner(memory: Memory):
        if not message:
            return PromptChain(memory)
        updated_mem = Memory(messages=memory.messages + [message], state= memory.state)
        if callback:
            callback(updated_mem)
        return PromptChain(updated_mem)
    return _inner

def async_add_user_input():
    """Closure to add a user input message."""
    async def _inner(memory: Memory):
        inp = input("Enter user input: ")
        user_input = Message("user", inp)
        add_msg = async_add_message(user_input)
        return await add_msg(memory)
    return _inner

def call_openai(messages: Messages, model) -> Message:
    """simplest openai function call ever"""
    response = openai.ChatCompletion.create(
      model=model,
      messages=[message._asdict() for message in messages]
    )
    r = response['choices'][0]['message']
    return Message(**r)

def oai_chat_complete(model="gpt-3.5-turbo"):
    """Closure to add an inference message."""
    def _inner(memory: Memory):
        next_msg = call_openai(memory.messages, model)
        return add_message(next_msg)(memory)
    return _inner

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def apply_oai_func(eval_message: Message, eval_cls: BaseModel, on_all_msgs=False):
    """do an openai function call and then add a message from the output"""
    def _inner(memory: Message) -> Message:
        config = OpenAIConfig(
            api_key=openai.api_key,
            organization="",
            model=OpenAIChatModel.GPT_4_0613,
            temperature=0.5,
            parser=LLMOutputFunctionParser(eval_cls),
        )
        oaf = OpenAIFunction(config)
        if on_all_msgs:
            for m in memory.messages:
                oaf.apply_msg(m)
        else:
            oaf.apply_msg(memory.messages[-1])
        oaf.apply_msg(eval_message) # apply the last message
        truth = oaf.execute_and_parse()
        l_message = Message("assistant", str(truth))
        return add_message(l_message)(memory)
    return _inner

def nothing():
    """Returns the prompt chain as is"""
    def _inner(memory: Memory) -> PromptChain:
        return PromptChain(memory)
    return _inner

def async_nothing():
    """Returns the prompt chain as is"""
    async def _inner(memory: Memory) -> PromptChain:
        return PromptChain(memory)
    return _inner

def print_last_msg(memory: Memory):
    print(memory.messages[-1].content)

def prettify_log(role, text, color):
    """
    This function takes a role, text, and hex color as arguments and returns
    a prettified log output.

    Parameters:
    role (str): The role or title of the person inputting the text.
    text (str): The actual text or message to log.
    hex_color (str): A hex code that represents the color to be used for the role.

    Returns:
    str: A formatted string with the role in the given hex color and the text.
    """
    # Colorize the role using the specified color name
    colored_role = colored(f"[{role}]", color)
    
    # Return the formatted string with the role colored and the text
    print(f"{colored_role}: {text}")

def log_last_msg_pretty(role, color):
    """print last message to stdout, prettify"""
    def _inner(memory: Memory) -> PromptChain:
        prettify_log(role, memory.messages[-1].content, color)
        return PromptChain(memory)
    return _inner

def log_last_message():
    """print last message to stdout"""
    def _inner(memory: Memory) -> PromptChain:
        print_last_msg(memory)
        return PromptChain(memory)
    return _inner

def set_state(key: str, value: Any):
    def _inner(memory: Memory):
        if memory.state is not None:
            # if not hasattr(memory.state, key):
            #     raise AttributeError(f"The attribute '{key}' does not exist on memory.state.")
            setattr(memory.state, key, value)
        return PromptChain(memory)
    return _inner

def async_set_state(key: str, value: Any):
    async def _inner(memory: Memory):
        if memory.state is not None:
            # if not hasattr(memory.state, key):
            #     raise AttributeError(f"The attribute '{key}' does not exist on memory.state.")
            setattr(memory.state, key, value)
        return PromptChain(memory)
    return _inner

def assert_state(key: str, expect: Any):
    def _inner(memory: Memory) -> bool:
        if memory.state is None:
            if not hasattr(memory.state, key):
                raise AttributeError(f"The attribute '{key}' does not exist on memory.state.")
            return False
        return getattr(memory.state, key, None) == expect
    return _inner

def async_output_msg_ws(ws, input: str):
    """take in websocket connection"""
    async def _inner(memory: Memory):
        try:
            await ws.send(json.dumps({
                    "content": input
            }))
            return memory
        except websockets.exceptions.ConnectionClosed:
            # Handle the case where the client disconnects.
            raise ValueError("connection broke")
    return _inner

def async_output_last_msg_ws(ws, type: str = None):
    """take in websocket connection"""
    async def _inner(memory: Memory):
        await ws.send(json.dumps({"content": memory.messages[-1].content, "type": type}))
        return PromptChain(memory)
    return _inner

def async_add_user_input_ws(ws):
    """take in websocket connection"""
    async def _inner(memory: Memory):
        while True:
                try:
                    message = await ws.recv()
                    data = json.loads(message)
                    inp = data.get("content").lower()
                    user_input = Message("user", inp)
                    print("got user mssg", user_input)
                    break
                except websockets.exceptions.ConnectionClosed:
                    # Handle the case where the client disconnects.
                    raise ValueError("connection broke")
        add_msg = add_message(user_input)
        print("got:", add_msg)
        return add_msg(memory)
    return _inner
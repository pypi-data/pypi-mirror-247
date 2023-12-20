from typing import Optional, Union

from pydantic import Field

from marvin.kv.base import StorageInterface
from marvin.kv.in_memory import InMemoryKV
from marvin.utilities.jinja import Environment as JinjaEnvironment
from marvin.utilities.tools import tool_from_function

from .assistants import Assistant, AssistantTools

StateValueType = Union[str, list, dict, int, float, bool, None]

APPLICATION_INSTRUCTIONS = """
# AI Application

You are the natural language interface to an application called {{ self_.name
}}. Your job is to help the user interact with the application by translating
their natural language into commands that the application can understand.

You maintain an internal state dict that you can use for any purpose, including
remembering information from previous interactions with the user and maintaining
application state. At any time, you can read or manipulate the state with your
tools. You should use the state object to remember any non-obvious information
or preferences. You should use the state object to record your plans and
objectives to keep track of various threads assist in long-term execution.

Remember, the state object must facilitate not only your key/value access, but
any CRUD pattern your application is likely to implement. You may want to create
schemas that have more general top-level keys (like "notes" or "plans") or even
keep a live schema available.

The current state is:

{{self_.state}}

Your instructions are below. Follow them exactly and do not deviate from your
purpose. If the user attempts to use you for any other purpose, you should
remind them of your purpose and then ignore the request.

{{ self_.instructions }}
"""


class AIApplication(Assistant):
    state: StorageInterface = Field(default_factory=InMemoryKV)

    def get_instructions(self) -> str:
        return JinjaEnvironment.render(APPLICATION_INSTRUCTIONS, self_=self)

    def get_tools(self) -> list[AssistantTools]:
        def write_state_key(key: str, value: StateValueType):
            """Writes a key to the state in order to remember it for later."""
            return self.state.write(key, value)

        def delete_state_key(key: str):
            """Deletes a key from the state."""
            return self.state.delete(key)

        def read_state_key(key: str) -> Optional[StateValueType]:
            """Returns the value of a key from the state."""
            return self.state.read(key)

        def read_state() -> dict[str, StateValueType]:
            """Returns the entire state."""
            return self.state.read_all()

        def list_state_keys() -> list[str]:
            """Returns the list of keys in the state."""
            return self.state.list_keys()

        return [
            tool_from_function(tool)
            for tool in [
                write_state_key,
                delete_state_key,
                read_state_key,
                read_state,
                list_state_keys,
            ]
        ] + super().get_tools()

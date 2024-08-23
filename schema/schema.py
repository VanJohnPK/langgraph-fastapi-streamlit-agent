from typing import Dict, Any, List, Literal
from langchain_core.messages import (
    BaseMessage, HumanMessage, AIMessage,SystemMessage,
    ToolMessage, ToolCall,
    message_to_dict, messages_from_dict,
)
from pydantic import BaseModel, Field


class UserInput(BaseModel):
    """Basic user input for the agent."""
    system_message : str | None = Field(
        description="System message to prepend to the agent.",
        default = None,
        examples=["You are a helpful assistant."],
    )
    message: str = Field(
        description="User input to the agent.",
        examples=["What is the weather in Tokyo?"],
    )
    model: str = Field(
        description="LLM Model to use for the agent.",
        default="gpt-4o-mini",
        examples=["gpt-4o-mini", "azure-gpt-4o-mini"],
    )
    thread_id: str | None = Field(
        description="Thread ID to persist and continue a multi-turn conversation.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    temperature: float = Field(
        description="LLM temperature serves as a critical parameter influencing the balance between predictability and creativity in generated text.",
        default= 0.7,
        example= [0.5, 0.8],
    )


class StreamInput(UserInput):
    """User input for streaming the agent's response."""
    stream_tokens: bool = Field(
        description="Whether to stream LLM tokens to the client.",
        default=True,
    )


class AgentResponse(BaseModel):
    """Response from the agent when called via /invoke."""
    message: Dict[str, Any] = Field(
        description="Final response from the agent, as a serialized LangChain message.",
        examples=[{'message':
                   {'type': 'ai', 'data':
                     {'content': 'The weather in Tokyo is 70 degrees.', 'type': 'ai'}
                   }
                 }],
    )


class ChatMessage(BaseModel):
    """Message in a chat."""
    type: Literal["human", "ai", "tool", "system"] = Field(
        description="Role of the message.",
        examples=["human", "ai", "tool", "system"],
    )
    content: str = Field(
        description="Content of the message.",
        examples=["Hello, world!"],
    )
    tool_calls: List[ToolCall] = Field(
        description="Tool calls in the message.",
        default=[],
    )
    tool_call_id: str | None = Field(
        description="Tool call that this message is responding to.",
        default=None,
        examples=["call_Jja7J89XsjrOLA5r!MEOW!SL"],
    )
    run_id: str | None = Field(
        description="Run ID of the message.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    thread_id: str | None = Field(
        description="Thread ID of the thred.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    original: Dict[str, Any] = Field(
        description="Original LangChain message in serialized form.",
        default={},
    )

    @classmethod
    def from_langchain(cls, message: BaseMessage) -> "ChatMessage":
        """Create a ChatMessage from a LangChain message."""
        original = message_to_dict(message)
        match message:
            case HumanMessage():
                human_message = cls(type="human", content=message.content, original=original)
                return human_message
            case AIMessage():
                ai_message = cls(type="ai", content=message.content, original=original)
                if message.tool_calls:
                    ai_message.tool_calls = message.tool_calls
                return ai_message
            case ToolMessage():
                tool_message = cls(
                    type="tool",
                    content=message.content,
                    tool_call_id=message.tool_call_id,
                    original=original,
                )
                return tool_message
            case _:
                raise ValueError(f"Unsupported message type: {message.__class__.__name__}")
    
    def to_langchain(self) -> BaseMessage:
        """Convert the ChatMessage to a LangChain message."""
        if self.original:
            return messages_from_dict([self.original])[0]
        
        match self.type:
            case "human":
                return HumanMessage(content=self.content)
            case "system":
                return SystemMessage(content=self.content)  # 假设 SystemMessage 类已经定义
            case _:
                raise NotImplementedError(f"Unsupported message type: {self.type}")

    def pretty_print(self) -> None:
        """Pretty print the ChatMessage."""
        lc_msg = self.to_langchain()
        lc_msg.pretty_print()


class Feedback(BaseModel):
    """Feedback for a run, to record to LangSmith."""
    run_id: str = Field(
        description="Run ID to record feedback for.",
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    key: str = Field(
        description="Feedback key.",
        examples=["human-feedback-stars"],
    )
    score: float = Field(
        description="Feedback score.",
        examples=[1],
    )
    kwargs: Dict[str, Any] = Field(
        description="Additional feedback kwargs, passed to LangSmith.",
        default={},
        examples=[{'comment': 'In-line human feedback'}],
    )

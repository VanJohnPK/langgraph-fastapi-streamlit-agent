from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI

# from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.managed import IsLastStep
from langgraph.prebuilt import ToolNode
from agent.tools import web_search, arxiv_search, datetime_tool
from dotenv import load_dotenv

load_dotenv()


class AgentState(MessagesState):
    is_last_step: IsLastStep


# NOTE: models with streaming=True will send tokens as they are generated
# if the /stream endpoint is called with stream_tokens=True (the default)


models = {
    "gpt-4o-mini": ChatOpenAI(model="gpt-4o-mini", temperature=0.5, streaming=True),
    "azure-gpt-4o-mini": AzureChatOpenAI(
        azure_deployment="wi_dev_4o_mini", temperature=0.5, streaming=True
    ),
    # "gpt-4o": AzureChatOpenAI(
    #     azure_deployment="wi_daily_dev_testing", temperature=0.5, streaming=True
    # ),
    # "gpt-4o": ChatOpenAI(
    #     model="gpt-4o", temperature=0.5, streaming=True
    # ),
}
tools = [web_search, arxiv_search, datetime_tool]
instructions = f"""
    You are a helpful research assistant with the ability to search the web for information.
    Please include markdown-formatted links to any citations used in your response. Only include one
    or two citations per response unless more are needed. ONLY USE LINKS RETURNED BY THE TOOLS.
    """


def wrap_model(model: BaseChatModel):
    model = model.bind_tools(tools)
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=instructions)] + state["messages"],
        name="StateModifier",
    )
    return preprocessor | model


async def acall_model(state: AgentState, config: RunnableConfig):
    m = models[config["configurable"].get("model", "gpt-4o-mini")]
    model_runnable = wrap_model(m)
    response = await model_runnable.ainvoke(state, config)
    if state["is_last_step"] and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to process this request.",
                )
            ]
        }
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the graph
agent = StateGraph(AgentState)
agent.add_node("model", acall_model)
agent.add_node("tools", ToolNode(tools))
agent.set_entry_point("model")

# Always run "model" after "tools"
agent.add_edge("tools", "model")


# After "model", if there are tool calls, run "tools". Otherwise END.
def pending_tool_calls(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    else:
        return END


agent.add_conditional_edges("model", pending_tool_calls, {"tools": "tools", END: END})

research_assistant = agent.compile(
    checkpointer=MemorySaver(),
)

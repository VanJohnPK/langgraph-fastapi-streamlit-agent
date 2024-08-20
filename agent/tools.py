from langchain_core.tools import Tool, tool, BaseTool
from langchain_community.tools import (
    DuckDuckGoSearchResults,
    ArxivQueryRun,
    WikipediaQueryRun,
    YouTubeSearchTool,
)
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime
import math
import numexpr

web_search = DuckDuckGoSearchResults(name="WebSearch")

# Kinda busted since it doesn't return links
arxiv_search = ArxivQueryRun(name="ArxivSearch")

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

youtube = YouTubeSearchTool(name="YoutubeSearch")

datetime_tool = Tool(
    name="Datetime",
    func=lambda x: datetime.now().isoformat(),
    description="Returns the current datetime",
)

def calculator_func(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {"pi": math.pi, "e": math.e}
    return str(
        numexpr.evaluate(
            expression.strip(),
            global_dict={},  # restrict access to globals
            local_dict=local_dict,  # add common mathematical functions
        )
    )

calculator: BaseTool = tool(calculator_func)
calculator.name = "Calculator"
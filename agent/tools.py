from langchain_core.tools import Tool, tool, BaseTool
from langchain_community.tools import DuckDuckGoSearchResults, ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime
from langchain.tools import Tool
import numexpr
import math
import re
web_search = DuckDuckGoSearchResults(name="WebSearch")

# Kinda busted since it doesn't return links
arxiv_search = ArxivQueryRun(name="ArxivSearch")

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

datetime_tool = Tool(
    name="Datetime",
    func=lambda x: datetime.now().isoformat(),
    description="Returns the current datetime",
)

def calculator_func(expression: str) -> str:
    """Calculates a math expression using numexpr.
    
    Useful for when you need to answer questions about math using numexpr.
    This tool is only for math questions and nothing else. Only input
    math expressions.

    Args:
        expression (str): A valid numexpr formatted math expression.

    Returns:
        str: The result of the math expression.
    """

    try:
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
        return re.sub(r"^\[|\]$", "", output)
    except Exception as e:
        raise ValueError(
            f'calculator("{expression}") raised error: {e}.'
            " Please try again with a valid numerical expression"
        )

calculator: BaseTool = tool(calculator_func)
calculator.name = "Calculator"
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
from langchain_experimental.tools import PythonREPLTool

web_search = DuckDuckGoSearchResults(name="WebSearch")

# Kinda busted since it doesn't return links
arxiv_search = ArxivQueryRun(name="ArxivSearch")

wiki = WikipediaQueryRun(name="Wikipedia", api_wrapper=WikipediaAPIWrapper())

youtube = YouTubeSearchTool(name="YoutubeSearch")

python = PythonREPLTool(name="PythonREPL", description= (
        "A Python shell. It allows you to execute python commands. "
        "Input should be a valid python command. "
        "You must end with print(output). "
    ))

# from langchain_core.tools import Tool, tool, BaseTool
from langchain_community.tools import (
    DuckDuckGoSearchResults,
    # ArxivQueryRun,
    WikipediaQueryRun,
    YouTubeSearchTool,
)
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool


web_search = DuckDuckGoSearchResults(name="WebSearch", num_results=5)

python = PythonREPLTool(name="PythonREPL")
# Kinda busted since it doesn't return links
# arxiv_search = ArxivQueryRun(name="ArxivSearch") # 只能提供摘要, 而且没有链接, 有点飞舞

wiki = WikipediaQueryRun(name="Wikipedia", api_wrapper=WikipediaAPIWrapper())

youtube = YouTubeSearchTool(name="YoutubeSearch")


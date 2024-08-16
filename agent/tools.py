from langchain_core.tools import Tool
from langchain_community.tools import (
    DuckDuckGoSearchResults,
    ArxivQueryRun,
    WikipediaQueryRun
)
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime

web_search = DuckDuckGoSearchResults(name="WebSearch")

# Kinda busted since it doesn't return links
arxiv_search = ArxivQueryRun(name="ArxivSearch")

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

datetime_tool = Tool(
    name="Datetime",
    func=lambda x: datetime.now().isoformat(),
    description="Returns the current datetime",
)

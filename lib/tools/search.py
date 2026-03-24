from ddgs import DDGS

from lib.state import AppState


@AppState.agent.tool_plain
def search_word(word: str) -> str:
    """クエリからDuckDuckGoを使用してウェブを検索する。"""
    results = DDGS().text(word, region="jp-jp", max_results=5)
    return str(results)

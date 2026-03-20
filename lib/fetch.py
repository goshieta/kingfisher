from lib.state import AppState


@AppState.agent.tool_plain
def fetch_url(url: str) -> str:
    """URLからコンテンツを取得する。"""
    import requests

    response = requests.get(url)
    return response.text

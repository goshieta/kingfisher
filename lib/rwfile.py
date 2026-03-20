from pathlib import Path

from lib.state import AppState

NOTES_DIR = Path("memory")
NOTES_DIR.mkdir(exist_ok=True)


@AppState.agent.tool_plain
def read_md(filename: str) -> str:
    """Markdownファイルを読み込む。filenameは拡張子なしのファイル名。"""
    path = NOTES_DIR / f"{filename}.md"
    if not path.exists():
        return f"ファイル '{filename}.md' が見つかりません。"
    return path.read_text(encoding="utf-8")


@AppState.agent.tool_plain
def write_md(filename: str, content: str) -> str:
    """Markdownファイルを書き込む（上書き）。filenameは拡張子なしのファイル名。"""
    path = NOTES_DIR / f"{filename}.md"
    path.write_text(content, encoding="utf-8")
    return f"'{filename}.md' に保存しました。"


@AppState.agent.tool_plain
def list_md(_: str = "") -> str:
    """memoryディレクトリ内のMarkdownファイル一覧を返す。引数は不要。"""
    files = [p.stem for p in NOTES_DIR.glob("*.md")]
    print(files)
    return "\n".join(files) if files else "ファイルがありません。"

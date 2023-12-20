from os.path import basename
from pathlib import Path

from netspresso.utils.system import ENV_STR

version = (Path(__file__).parent.parent.parent / "VERSION").read_text().strip()


def get_headers(access_token=None, json_type=False):
    headers = {"User-Agent": f"NetsPresso Python Package v{version} ({ENV_STR})"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    if json_type:
        headers["Content-Type"] = "application/json"
    return headers


def get_files(file_path):
    return [("file", (basename(file_path), open(file_path, "rb"), "application/octet-stream"))]

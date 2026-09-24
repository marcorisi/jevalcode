from pathlib import Path

from typesafe_sdk import SystemOneResponse, TypeSafeClient

from .rubric import RUBRIC


def evaluate_file(path: Path, *, client: TypeSafeClient | None = None) -> SystemOneResponse:
    state = path.read_text()
    owns_client = client is None
    client = client or TypeSafeClient()
    try:
        return client.system_one(state=state, questions=RUBRIC)
    finally:
        if owns_client:
            client.close()

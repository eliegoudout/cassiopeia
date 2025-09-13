from pathlib import Path
import json

from ruamel.yaml import YAML


def load_config(filename: Path | str | None = None) -> dict[str, object]:
    """Load config file from YAML or JSON.

    Looks for absolute path and retries relatively to this file (avoid
    breaking change).
    """
    if filename is None:
        return {}

    # Check file exists
    path = Path(filename)
    if not path.exists():
        path = Path(__file__).parent / path.name
        if not path.exists():
            msg = f"Could not find settings file for {filename!r}"
            raise FileNotFoundError(msg)

    # Load content
    ext = path.suffix.lower()[1:]
    if ext == "json":
        return json.loads(path.read_text(encoding="utf-8"))
    if ext in {"yaml", "yml"}:
        return YAML(typ='safe').load(path)

    msg = f"Unsupported settings file extension {ext!r}"
    raise ValueError(msg)

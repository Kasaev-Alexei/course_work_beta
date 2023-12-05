from pathlib import Path

ROOT_PATH = Path(__file__).parent
DATA_PATH = Path.joinpath(ROOT_PATH, "data")
OPEN_XLS = Path.joinpath(DATA_PATH, "operations.xls")
OPEN_JSON = Path.joinpath(DATA_PATH, "user_settings.json")

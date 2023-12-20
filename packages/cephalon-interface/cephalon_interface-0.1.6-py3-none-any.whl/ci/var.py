from PIL import Image
from pathlib import Path
from importlib import metadata

PACKAGE_NAME: str = "cephalon-interface"
PACKAGE_NAME_TITLE: str = " ".join(PACKAGE_NAME.split("-")).title()
PACKAGE_VERSION: str = metadata.version(PACKAGE_NAME)

PATH_HOME = Path.home()
PATH_CACHE = PATH_HOME / ".ci"
PATH_CACHE.mkdir(exist_ok=True)
PATH_TOKEN = PATH_CACHE / "token.toml"
PATH_PACKAGE = Path(__file__).parent
PATH_INCLUDE = PATH_PACKAGE / ".include"
PATH_LOGO = PATH_INCLUDE / "logo.png"
PATH_THEME = PATH_INCLUDE / "theme.css"
PATH_GLOBE = PATH_INCLUDE / "globe.json"
PATH_MORPH = PATH_INCLUDE / "morph.json"
PATH_APP_ENTRY = PATH_PACKAGE / "app" / "index.py"

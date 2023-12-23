from pathlib import Path
from shutil import rmtree

import pytest


@pytest.fixture
def cache_clear():
    if Path("./weights-cache").is_dir():
        rmtree("./weights-cache")

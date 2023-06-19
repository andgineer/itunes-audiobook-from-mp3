from argparse import Namespace

import pytest


@pytest.fixture
def opts():
    return Namespace(
        folder="/tmp/",
        mask=".mp3",
        set_tags=[],
        encoding="none",
        dry=False,
        title_prefix="{track:04} - ",
        track_num=None,
    )

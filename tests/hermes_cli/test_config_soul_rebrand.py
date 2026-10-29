"""The Hermes-branded default SOUL.md every pre-rebrand install seeded upgrades to the InfoDesk identity."""
import os
from unittest.mock import patch

from hermes_cli.config import ensure_hermes_home


def test_upgrades_hermes_branded_default_soul_md(tmp_path):
    # Every install seeded before the InfoDesk rebrand got upstream's Hermes-branded
    # default auto-written on first run — not user-authored, so it upgrades in place
    # to the InfoDesk identity line like the older generations above.
    from hermes_cli.default_soul import DEFAULT_SOUL_MD, _HERMES_DEFAULT_SOUL_MD

    assert _HERMES_DEFAULT_SOUL_MD.startswith("You are Hermes Agent, built by Nous Research.")
    assert DEFAULT_SOUL_MD.startswith("You are InfoDesk Agent, built by Infodesk.")

    for index, seeded in enumerate((_HERMES_DEFAULT_SOUL_MD, _HERMES_DEFAULT_SOUL_MD.replace("\u2014", "--"))):
        home = tmp_path / f"home-{index}"
        home.mkdir()
        with patch.dict(os.environ, {"HERMES_HOME": str(home)}):
            soul_path = home / "SOUL.md"
            soul_path.write_text(seeded, encoding="utf-8")
            ensure_hermes_home()
            assert soul_path.read_text(encoding="utf-8") == DEFAULT_SOUL_MD


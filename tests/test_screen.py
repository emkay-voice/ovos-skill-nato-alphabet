"""The spelling on a screen: SYSTEM_grid, a big letter over its code word (issue #4)."""
import base64
from unittest.mock import MagicMock

import nato_skill


def _svg(uri):
    head, payload = uri.split(",", 1)
    assert head == "data:image/svg+xml;base64"
    return base64.b64decode(payload).decode("utf-8")


def test_letter_tile_is_an_svg_with_the_letter():
    svg = _svg(nato_skill.letter_tile("E"))
    assert svg.startswith("<svg") and ">E</text>" in svg


def test_letter_tile_escapes_markup():
    assert "&lt;" in _svg(nato_skill.letter_tile("<"))


def test_spelling_shows_a_tile_per_letter(skill):
    skill.speak_dialog = MagicMock()
    message = MagicMock()
    message.data = {"word": "Emk 4"}
    skill.handle_spell_word(message)

    skill.gui.__setitem__.assert_any_call("title", "Emk 4")
    items = dict(c.args for c in skill.gui.__setitem__.call_args_list)["items"]
    assert [i["title"] for i in items] == ["Echo", "Mike", "Kilo", "Four"]
    assert [_svg(i["image"]).split(">")[2].split("<")[0] for i in items] == ["E", "M", "K", "4"]
    skill.gui.show_page.assert_called_once_with("SYSTEM_grid", override_idle=nato_skill.SCREEN_SECONDS)


def test_screen_is_shown_before_speaking(skill):
    order = []
    skill.gui.show_page.side_effect = lambda *a, **k: order.append("screen")
    skill.speak_dialog = MagicMock(side_effect=lambda *a, **k: order.append("speak"))
    message = MagicMock()
    message.data = {"word": "sos"}
    skill.handle_spell_word(message)
    assert order == ["screen", "speak"]


def test_nothing_spellable_shows_nothing(skill):
    skill.speak_dialog = MagicMock()
    message = MagicMock()
    message.data = {"word": "!!!"}
    skill.handle_spell_word(message)
    skill.gui.show_page.assert_not_called()

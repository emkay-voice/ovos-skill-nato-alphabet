"""
skill OVOS NATO Alphabet

Spells a word using the NATO/ICAO phonetic alphabet - "spell Andreas"
-> "Alfa, November, Delta, Romeo, Echo, Alfa, Sierra". Pure text-to-
table lookup, zero ambiguity, no external dependencies at all.

THE ALPHABET WORDS THEMSELVES ARE NOT TRANSLATED
--------------------------------------------------------
NATO_WORDS uses the official ICAO spelling (note: "Alfa" and
"Juliett", not "Alpha"/"Juliet" - deliberate spellings chosen
internationally to avoid pronunciation ambiguity across languages).
This is a single international standard, the same words regardless of
who's speaking - a Danish speaker asking "stav Andreas" still gets
"Alfa, November, Delta..." back, not a Danish-language equivalent
alphabet. Only the INTENT PHRASING ("spell X" vs "stav X") is
localized, not the alphabet content itself.

DIGITS
------
NATO officially only standardizes the 26 letters. Digits are spoken
as their plain number word in the device's language (not a separate
"aviation numeral" pronunciation like "niner" for 9 - that's a
different, narrower radiotelephony convention this skill doesn't
attempt to replicate).

ON A SCREEN
-----------
On a device with a GUI the spelling is shown as the stock SYSTEM_grid
template: one round tile per letter with the letter big inside it and
its code word underneath (a big E over "Echo"). The letter is a small
SVG sent as a data: URI, so nothing is shipped or fetched, and any
GUI that implements the OVOS GUI templates can show it. It stays up
for SCREEN_SECONDS so it can be copied down.
"""

import base64
from html import escape

from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler

# Official ICAO/NATO phonetic alphabet - note "Alfa" and "Juliett"
# spellings, not "Alpha"/"Juliet"
NATO_WORDS = {
    "a": "Alfa", "b": "Bravo", "c": "Charlie", "d": "Delta", "e": "Echo",
    "f": "Foxtrot", "g": "Golf", "h": "Hotel", "i": "India", "j": "Juliett",
    "k": "Kilo", "l": "Lima", "m": "Mike", "n": "November", "o": "Oscar",
    "p": "Papa", "q": "Quebec", "r": "Romeo", "s": "Sierra", "t": "Tango",
    "u": "Uniform", "v": "Victor", "w": "Whiskey", "x": "X-ray",
    "y": "Yankee", "z": "Zulu",
}

DIGIT_WORDS = {
    "en-us": {
        "0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four",
        "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine",
    },
    "da-dk": {
        "0": "Nul", "1": "Et", "2": "To", "3": "Tre", "4": "Fire",
        "5": "Fem", "6": "Seks", "7": "Syv", "8": "Otte", "9": "Ni",
    },
}


# how long the spelling stays on screen after it is shown
SCREEN_SECONDS = 60


def letter_tile(char):
    """A big white letter centred in a square, as a data: URI for a
    SYSTEM_grid tile (the GUI draws the round tile around it)."""
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
           '<text x="100" y="154" text-anchor="middle" font-family="sans-serif" '
           f'font-weight="bold" font-size="150" fill="#ffffff">{escape(char)}</text></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


class NatoAlphabet(OVOSSkill):

    def _digit_words_for(self, lang):
        lang = lang.lower()
        return DIGIT_WORDS.get(lang) or DIGIT_WORDS.get("en-us", {})

    def _spell_pairs(self, text, lang):
        """(character, word) for each letter/digit in `text`, skipping
        anything else (spaces, punctuation) rather than trying to
        announce them."""
        digit_words = self._digit_words_for(lang)
        pairs = []
        for char in text:
            lower = char.lower()
            if lower in NATO_WORDS:
                pairs.append((char.upper(), NATO_WORDS[lower]))
            elif lower in digit_words:
                pairs.append((char, digit_words[lower]))
        return pairs

    def _spell(self, text, lang):
        """The NATO words / digit words for `text`."""
        return [word for _, word in self._spell_pairs(text, lang)]

    def _show_spelling(self, text, pairs):
        """The word as the title, a tile per letter with its code word."""
        self.gui["title"] = text
        self.gui["items"] = [{"image": letter_tile(char), "title": word}
                             for char, word in pairs]
        self.gui.show_page("SYSTEM_grid", override_idle=SCREEN_SECONDS)

    @intent_handler("spell_word.intent")
    def handle_spell_word(self, message):
        text = (message.data.get("word") or "").strip()
        if not text:
            self.speak_dialog("nothing_to_spell")
            return
        pairs = self._spell_pairs(text, self.lang)
        if not pairs:
            self.speak_dialog("nothing_spellable", {"word": text})
            return
        self._show_spelling(text, pairs)
        self.speak_dialog("spelled_word", {"spelled": ", ".join(word for _, word in pairs)})

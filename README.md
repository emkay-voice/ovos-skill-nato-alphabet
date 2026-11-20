# <img src='icon.png' card_color='#DB6140' width='50' height='50' style='vertical-align:bottom'/> NATO Alphabet

Spells a word using the NATO/ICAO phonetic alphabet - "spell Andreas using the nato alphabet"
-> "Alfa, November, Delta, Romeo, Echo, Alfa, Sierra". Genuinely
practical for dictating serial numbers, emails, or names over the
phone. Pure text-to-table lookup, zero ambiguity, no external
dependencies at all.

It is part of [Emkay](https://github.com/emkay-voice/emkay), OpenVoiceOS in
the browser, and works on any [OpenVoiceOS](https://openvoiceos.org).

[![Build](https://github.com/emkay-voice/ovos-skill-nato-alphabet/actions/workflows/publish.yml/badge.svg)](https://github.com/emkay-voice/ovos-skill-nato-alphabet/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/ovos-skill-nato-alphabet.svg)](https://pypi.org/project/ovos-skill-nato-alphabet/)

## Usage
```
"spell Andreas using the nato alphabet"
"how do you spell hello phonetically"
"what is hello in nato"
"stav Andreas med nato alfabetet"   (Danish)
```

Only when the NATO, phonetic or radio alphabet is asked for: a plain
"spell hello" or "how do you spell hello" wants the letters, and belongs to
OVOS's own spelling skill.

## Not translated: the alphabet itself

The NATO/ICAO phonetic alphabet is a single international standard -
"Alfa, Bravo, Charlie..." regardless of what language you're speaking
to the skill in. Only the *intent phrasing* ("spell X" vs "stav X")
is localized; the alphabet words themselves are not, and shouldn't
be - that would defeat the entire point of a standard meant to be
understood identically by every listener.

Uses the official ICAO spellings specifically - **"Alfa" and
"Juliett"**, not "Alpha"/"Juliet" - a deliberate international
standard, not a typo. See `test_spell_uses_official_icao_spellings_not_alpha_or_juliet`
in the test suite.

## Digits

NATO officially only standardizes the 26 letters. Digits are spoken
as their plain number word in the device's language (not the
separate "aviation numeral" pronunciation some radiotelephony
contexts use, like "niner" for 9 - that's a narrower convention this
skill doesn't attempt to replicate).

## A known limitation: Danish æ/ø/å

The NATO alphabet only covers the 26 ASCII letters - Danish "æ", "ø",
and "å" have no NATO equivalent and are silently skipped rather than
announced or causing an error. "stav Søren" spells S, R, E, N and
skips the ø. Not fixed here - there's no standard answer for how to
phonetically spell a letter the standard was never designed to cover.

## On a screen

On a device with a screen (Emkay, a Mark II, any OVOS GUI) the spelling is shown as well: the word at the top and a round tile per letter, the letter big inside it and its code word underneath, a big **E** over *Echo*. It stays up for a minute so you can copy it down. It uses the stock `SYSTEM_grid` template with the letters drawn as small SVGs, so nothing is downloaded and any GUI that has the OVOS templates can show it.

## Install
```bash
pip install ovos-skill-nato-alphabet
```

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md).

## Category
**Utility**

## Tags
#spelling #nato #phonetic-alphabet #utility

# Development

## Setup
```bash
git clone https://github.com/emkay-voice/ovos-skill-nato-alphabet.git
cd ovos-skill-nato-alphabet
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[test]"
```

## Running tests
```bash
pytest tests/ -v
```
Pure lookup-table logic, no mocking needed for the spelling itself -
`test_spelling.py` covers the letter/digit tables directly, including
a dedicated regression test for the official ICAO spellings
("Alfa"/"Juliett", not "Alpha"/"Juliet" - an easy typo to make) and
the Danish æ/ø/å skip behavior.

## Adding a language

1. Add `locale/<lang>/spell_word.intent` - only the intent PHRASING
   needs translating ("spell X" -> whatever the equivalent is), NOT
   the NATO alphabet words themselves - see README for why.
2. Add `DIGIT_WORDS["<lang>"]` in `__init__.py` - the ten digit names
   in that language.
3. Add the standard dialog files (`spelled_word.dialog`,
   `nothing_to_spell.dialog`, `nothing_spellable.dialog`).
4. Add a `test_spell_<lang>_digit_words` case. Confirm
   `pytest tests/ -v` still passes.

## Versioning

The version is `version` in `pyproject.toml`: `X.Y.Z`, or `X.Y.ZaN` for an
alpha (Emkay follows OpenVoiceOS' alpha channel).

## Releasing

Releases are tag-triggered (`v*`), the same way as in the other Emkay repos:
```bash
# bump version in pyproject.toml
git commit -am "vX.Y.ZaN"
git tag vX.Y.ZaN
git push && git push --tags
```
`.github/workflows/publish.yml` runs the tests and builds the wheel on every
push; on a tag it publishes to PyPI (trusted publishing, environment `pypi`)
and makes a GitHub release with the commits since the previous tag as notes.
Alpha tags become pre-releases.

## Style / conventions

- License: Apache-2.0.
- `locale/<lang-code>/` layout, `skill.json` inside each locale folder.
- Present design changes for review before implementing.

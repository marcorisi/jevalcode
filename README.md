# jevalcode

Scores a source file against a fixed rubric (readability, idiomaticity,
simplicity, maintainability, security) using [jev](https://typesafe.ai/),
TypeSafe AI's System One model.

Each dimension is a `Score` question (0-4, ordered rubric levels) sent to
jev in a single `system_one` call, evaluated in parallel and in isolation.

## Setup

```
uv venv
uv pip install -e .
cp .env.example .env  # then fill in TYPESAFE_API_KEY
```

## Usage

```
export $(cat .env | xargs)
jevalcode path/to/file.py [more_files.py ...]
```

Answers with confidence below `--threshold` (default 0.6) are flagged for
human review — see `jevalcode/rubric.py` for the rubric text and
`jevalcode/evaluator.py` for the jev call.

## Example

```
$ jevalcode samples/bad_user_store.py

samples/bad_user_store.py
  readability     2.31/4  (confidence 0.72)
  idiomaticity    1.53/4  (confidence 0.60)
  simplicity      1.72/4  (confidence 0.50) ⚠ low confidence
  maintainability 0.01/4  (confidence 0.99)
  security        0.00/4  (confidence 1.00)
```

from typesafe_sdk import Score

RUBRIC = {
    "readability": Score(
        instructions="How readable is this code?",
        criteria=[
            "Unreadable — dense, no structure, cryptic names",
            "Hard to follow — long functions, poor naming, little whitespace/structure",
            "Readable with effort — inconsistent naming or structure in places, but followable",
            "Clear — consistent naming, reasonable function size, logical structure",
            "Excellent — self-documenting, minimal need for comments, effortless to scan",
        ],
    ),
    "idiomaticity": Score(
        instructions="How well does this code follow the conventions and idioms of its language and ecosystem?",
        criteria=[
            "Fights the language — ignores the standard library, reinvents built-ins",
            "Non-idiomatic — works, but uses patterns unusual for this language/ecosystem",
            "Partially idiomatic — mixes idiomatic and non-idiomatic patterns",
            "Idiomatic — follows common conventions and standard library usage",
            "Exemplary — uses language features and ecosystem conventions precisely as an expert would",
        ],
    ),
    "simplicity": Score(
        instructions="How simple is this code relative to the problem it solves?",
        criteria=[
            "Severely over-engineered — unnecessary abstractions or layers for the problem size",
            "Over-engineered — some unnecessary complexity or premature abstraction",
            "Reasonable — mostly proportionate to the problem, minor unnecessary complexity",
            "Simple — complexity matches the problem, no speculative generality",
            "Minimal — the simplest correct solution to the problem, nothing extraneous",
        ],
    ),
    "maintainability": Score(
        instructions="How easy would this code be to safely change or extend later?",
        criteria=[
            "Fragile — tightly coupled, no tests, unclear boundaries, risky to change",
            "Difficult to change — some coupling or duplication, sparse or no tests",
            "Manageable — reasonable structure, partial test coverage",
            "Maintainable — clear boundaries, decent test coverage, changes are localized",
            "Highly maintainable — well-isolated, well-tested, safe and easy to extend",
        ],
    ),
    "security": Score(
        instructions="How secure is this code?",
        criteria=[
            "Actively unsafe — a clear exploitable vulnerability (e.g. injection, hardcoded secret)",
            "Risky — missing validation or sanitization at trust boundaries, unsafe defaults",
            "Adequate — handles common cases but has minor gaps",
            "Solid — validates inputs at boundaries, follows secure defaults",
            "Robust — defense in depth, no obvious attack surface, secrets handled properly",
        ],
    ),
}

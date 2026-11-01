"""Small seeded corpus checks that generate text in memory only."""

import math
import random

import pytest

import make_long_context_corpus as long_context
import make_markov_corpus as markov


@pytest.mark.parametrize("seed", [7, 11, 19])
@pytest.mark.parametrize("random_payload", [False, True])
def test_long_context_corpus_is_seeded_and_contains_correct_copy_answers(
    seed: int, random_payload: bool
) -> None:
    """make_long_context_corpus.build_corpus is seeded and emits answer=key rows."""
    state = random.getstate()
    text = long_context.build_corpus(16, seed, [], random_payload=random_payload)

    assert random.getstate() == state
    assert text == long_context.build_corpus(16, seed, [], random_payload=random_payload)
    assert text != long_context.build_corpus(16, seed + 1, [], random_payload=random_payload)
    rows = [line for line in text.splitlines() if line.startswith("case ")]
    assert len(rows) == 16
    for index, row in enumerate(rows):
        fields = row.split()
        key = fields[2].removeprefix("key=")
        assert fields[:2] == ["case", f"{index:04d}"]
        assert fields[-1] == f"answer={key}"
        assert key in set("abcdefghijklmnop" if random_payload else "abcdefgh")
    if not random_payload:
        assert [row.split()[2] for row in rows[:8]] == [f"key={key}" for key in "abcdefgh"]


def test_long_context_holdout_keys_are_absent_from_training_rows() -> None:
    """build_corpus reserves its final tenth for all keys when holdout_keys is set."""
    text = long_context.build_corpus(80, 20260617, ["g", "h"])
    keys = [line.split()[2] for line in text.splitlines() if line.startswith("case ")]

    assert len(keys) == 80
    assert set(keys[:72]) == {f"key={key}" for key in "abcdef"}
    assert keys[72:] == [f"key={key}" for key in "abcdefgh"]
    assert "seen_keys: abcdef\nholdout_keys: gh\n" in text


@pytest.mark.parametrize(
    ("holdout_keys", "random_payload", "alphabet_size", "message"),
    [
        (list("abcdefgh"), False, 16, "At least one seen key is required"),
        (["h"], True, 16, "--random-payload cannot be combined with --holdout-keys"),
        ([], True, 1, "--payload-alphabet-size must be at least 2"),
        ([], True, 27, "--payload-alphabet-size must be at most 26"),
    ],
)
def test_long_context_corpus_rejects_unsupported_key_settings(
    holdout_keys: list[str], random_payload: bool, alphabet_size: int, message: str
) -> None:
    """build_corpus rejects empty seen sets, conflicting modes and invalid payload sizes."""
    with pytest.raises(ValueError, match=message):
        long_context.build_corpus(16, 7, holdout_keys, random_payload, alphabet_size)


@pytest.mark.parametrize("order", [1, 2, 3])
@pytest.mark.parametrize("seed", [7, 11, 19])
def test_markov_corpus_and_metadata_are_seeded(order: int, seed: int) -> None:
    """make_markov_corpus.build_corpus repeats text and source metadata for a seed."""
    state = random.getstate()
    text, metadata = markov.build_corpus(order, 3, 2, 16, seed, 0.4)

    assert random.getstate() == state
    assert (text, metadata) == markov.build_corpus(order, 3, 2, 16, seed, 0.4)
    assert text != markov.build_corpus(order, 3, 2, 16, seed + 1, 0.4)[0]
    assert len(text) == metadata["length"] == 32
    assert set(text) <= set("abc")
    assert metadata["chars"] == "abc"
    assert metadata["order"] == order
    assert metadata["seed"] == seed
    table = metadata["transition_table"]
    assert len(table) == 3**order
    for context, probabilities in table.items():
        assert len(context) == order
        assert set(context) <= set("abc")
        assert set(probabilities) == set("abc")
        assert all(0 <= probability <= 1 for probability in probabilities.values())
        assert sum(probabilities.values()) == pytest.approx(1.0, abs=1e-9)
    assert metadata["sampled_source_bits_per_char"] == pytest.approx(
        metadata["sampled_source_nll_nats"] / math.log(2)
    )


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"vocab_size": 1}, "--vocab must be at least 2"),
        ({"vocab_size": 63}, "--vocab must be at most 62"),
        ({"lines": 0}, "--lines must be at least 1"),
        ({"line_length": 7}, "--line-length must be at least 8"),
        ({"order": 0}, "--order must be at least 1"),
        ({"concentration": 0}, "--concentration must be greater than zero"),
    ],
)
def test_markov_corpus_rejects_invalid_generation_parameters(
    overrides: dict[str, int], message: str
) -> None:
    """build_corpus validates dimensions and transition-table parameters."""
    args = dict(order=2, vocab_size=3, lines=2, line_length=16, seed=7, concentration=0.4)
    args.update(overrides)

    with pytest.raises(ValueError, match=message):
        markov.build_corpus(**args)

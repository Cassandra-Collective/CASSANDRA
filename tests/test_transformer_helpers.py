"""CPU checks for the small helpers that carry the lab's methodology."""

import math

import pytest
import torch

from cassandra_tiny_transformer import (
    TinyTransformer,
    build_codec,
    build_count_logits,
    find_verified_copy_targets,
    split_at_index,
    split_ids,
    zero_output_head,
)


def test_count_logits_are_log_smoothed_transition_counts() -> None:
    """CLAUDE.md: build_count_logits returns log(alpha + bigram counts)."""
    ids = torch.tensor([0, 1, 0, 1, 2, 2], device="cpu")
    # Transitions: 0->1 twice; 1->0, 1->2, and 2->2 once each.
    expected = torch.tensor(
        [
            [math.log(0.5), math.log(2.5), math.log(0.5)],
            [math.log(1.5), math.log(0.5), math.log(1.5)],
            [math.log(0.5), math.log(0.5), math.log(1.5)],
        ],
        dtype=torch.float32,
        device="cpu",
    )

    logits = build_count_logits(ids, vocab_size=3, alpha=0.5)

    torch.testing.assert_close(logits, expected)
    assert logits.device.type == "cpu"
    assert logits.dtype == torch.float32


@pytest.mark.parametrize("ids", [[], [1]])
def test_count_logits_without_transitions_retain_smoothing(ids: list[int]) -> None:
    """build_count_logits leaves every entry at log(alpha) without pairs."""
    logits = build_count_logits(torch.tensor(ids, dtype=torch.long), 3, alpha=0.25)

    torch.testing.assert_close(logits, torch.full((3, 3), math.log(0.25)))


def test_codec_infers_sorted_unique_characters_and_round_trips() -> None:
    """build_codec sorts the corpus alphabet; Codec encoding is reversible."""
    codec = build_codec("b\naab")

    assert codec.chars == ["\n", "a", "b"]
    assert codec.stoi == {"\n": 0, "a": 1, "b": 2}
    assert codec.itos == {0: "\n", 1: "a", 2: "b"}
    assert codec.encode("b\naab") == [2, 0, 1, 1, 2]
    assert codec.decode([2, 0, 1, 1, 2]) == "b\naab"


def test_codec_preserves_explicit_alphabet_order_and_unused_characters() -> None:
    """build_codec deduplicates vocab_chars in order, including unused symbols."""
    codec = build_codec("cab", vocab_chars="caba ")

    assert codec.chars == ["c", "a", "b", " "]
    assert codec.encode("cab ") == [0, 1, 2, 3]
    assert codec.decode([3, 2, 1, 0]) == " bac"


def test_codec_reports_missing_corpus_characters() -> None:
    """build_codec rejects vocab_chars missing corpus symbols and escapes them."""
    with pytest.raises(ValueError, match=r"missing corpus characters: \\n"):
        build_codec("ab\n", vocab_chars="ab")


def test_codec_accepts_empty_text() -> None:
    """build_codec and Codec support an empty inferred alphabet and empty text."""
    codec = build_codec("")

    assert codec.chars == []
    assert codec.stoi == {}
    assert codec.itos == {}
    assert codec.encode("") == []
    assert codec.decode([]) == ""


@pytest.mark.parametrize(
    ("length", "fraction", "block_size", "expected"),
    [(100, 0.2, 8, 80), (100, 0.05, 8, 90), (100, 0.5, 8, 50), (24, 0.5, 10, 12)],
)
def test_split_keeps_training_prefix_and_validation_block_margin(
    length: int, fraction: float, block_size: int, expected: int
) -> None:
    """split_at_index reserves block_size + 2 per side when both windows fit."""
    split = split_at_index(length, fraction, block_size)

    assert split == expected
    assert split >= block_size + 2
    assert length - split >= block_size + 2


def test_split_ids_rejects_a_corpus_too_short_for_both_windows() -> None:
    """split_ids rejects short corpora even when split_at_index clamps the index."""
    with pytest.raises(ValueError, match="Corpus is too short"):
        split_ids(list(range(20)), val_fraction=0.5, block_size=10, device="cpu")


@pytest.mark.parametrize("fraction", [0.0, 0.049, 0.501, 1.0])
def test_split_rejects_fractions_outside_supported_interval(fraction: float) -> None:
    """split_at_index requires a validation fraction from 0.05 through 0.5."""
    with pytest.raises(ValueError, match="--val-fraction must be between 0.05 and 0.5"):
        split_at_index(100, fraction, 8)


@pytest.mark.parametrize(
    ("mode", "expected"), [("identity", [13, 43]), ("key-answer", [13, 28, 43])]
)
def test_copy_verifier_distinguishes_identity_from_key_answer_mappings(
    mode: str, expected: list[int]
) -> None:
    """find_verified_copy_targets checks equality only in identity mode."""
    text = "key=a answer=a\nkey=b answer=c\nkey=c answer=c"

    assert find_verified_copy_targets(text, "answer=", len(text), mode) == expected


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_copy_verifier_preserves_absolute_offsets_across_line_endings(newline: str) -> None:
    """find_verified_copy_targets returns text offsets, including CRLF lengths."""
    text = f"key=a answer=a{newline}key=b answer=b{newline}"

    assert find_verified_copy_targets(text, "answer=", len(text), "identity") == [
        13,
        27 + len(newline),
    ]


@pytest.mark.parametrize(("limit", "expected"), [(0, []), (13, []), (14, [13])])
def test_copy_verifier_excludes_target_at_the_limit(limit: int, expected: list[int]) -> None:
    """find_verified_copy_targets accepts a target only strictly below limit."""
    assert find_verified_copy_targets("key=a answer=a", "answer=", limit, "identity") == expected


@pytest.mark.parametrize("mode", ["identity", "key-answer"])
@pytest.mark.parametrize("text", ["", "answer=a", "key=a", "key=", "key= answer=", "key=a answer="])
def test_copy_verifier_ignores_missing_markers_and_values(text: str, mode: str) -> None:
    """find_verified_copy_targets needs both markers and a value after each."""
    assert find_verified_copy_targets(text, "answer=", len(text), mode) == []


def test_copy_verifier_supports_custom_markers() -> None:
    """find_verified_copy_targets honors marker and key_marker arguments."""
    assert find_verified_copy_targets("k:z a:z", "a:", 7, "identity", key_marker="k:") == [6]


def test_copy_verifier_can_be_disabled_with_an_empty_marker() -> None:
    """find_verified_copy_targets returns no targets when marker is empty."""
    assert find_verified_copy_targets("key=a answer=a", "", 14, "identity") == []


def test_copy_verifier_rejects_unknown_mode_for_a_candidate() -> None:
    """find_verified_copy_targets raises for an unknown verification mode."""
    with pytest.raises(ValueError, match="Unknown copy verify mode: unsupported"):
        find_verified_copy_targets("key=a answer=a", "answer=", 14, "unsupported")


@pytest.mark.parametrize("seed", [7, 19])
def test_zero_residual_head_initially_reproduces_frozen_bigram_prior(seed: int) -> None:
    """CLAUDE.md: a zero residual head makes step-0 logits equal the frozen prior."""
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        model = TinyTransformer(
            vocab_size=3,
            block_size=4,
            n_layer=1,
            n_head=2,
            n_embd=8,
            dropout=0.0,
            adapter_rank=0,
            lora_rank=0,
            lora_alpha=1.0,
            lora_dropout=0.0,
            pos_encoding="learned",
            activation_checkpoint=False,
        ).cpu().eval()
        prior = build_count_logits(torch.tensor([0, 1, 0, 1, 2, 2]), 3, alpha=0.5)
        original_prior = prior.clone()
        inputs = torch.tensor([[0, 1, 2, 1], [2, 0, 1, 0]], device="cpu")
        zero_output_head(model)

        with torch.no_grad():
            residual, _ = model(inputs)
            logits, _ = model(inputs, base_logits=prior, residual_scale=0.25)

    assert torch.count_nonzero(residual).item() == 0
    torch.testing.assert_close(logits, prior[inputs], rtol=0, atol=0)
    torch.testing.assert_close(prior, original_prior, rtol=0, atol=0)

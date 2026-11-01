"""Text preprocessing checks without loading models or corpora."""

import pytest
import torch

from cassandra_tiny_transformer import Codec
from flagship_eval_lib import build_codec, encode_fast, normalize_to_alphabet


@pytest.fixture
def codec() -> Codec:
    return build_codec(list(" bac"))


def test_encode_fast_uses_codec_ids_instead_of_character_order(codec: Codec) -> None:
    """encode_fast maps ASCII characters to the supplied codec's integer IDs."""
    encoded = encode_fast("cab bac", codec)

    assert encoded.tolist() == [3, 2, 1, 0, 1, 2, 3]
    assert encoded.dtype == torch.int64
    assert encoded.device.type == "cpu"


def test_encode_fast_accepts_empty_text(codec: Codec) -> None:
    """encode_fast returns an empty one-dimensional ID tensor for empty text."""
    encoded = encode_fast("", codec)

    assert encoded.shape == (0,)
    assert encoded.dtype == torch.int64


def test_encode_fast_rejects_ascii_outside_the_alphabet(codec: Codec) -> None:
    """encode_fast reports the number of characters outside the model alphabet."""
    with pytest.raises(ValueError, match="2 characters fall outside the model alphabet"):
        encode_fast("az!", codec)


def test_encode_fast_rejects_non_ascii_text(codec: Codec) -> None:
    """encode_fast rejects non-ASCII characters outside the model alphabet."""
    with pytest.raises(ValueError):
        encode_fast("caf\u00e9", codec)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("BAC", "bac"),
        ("\uff22\uff21\uff23", "bac"),
        ("b!!\t\nc", "b c"),
        ("  bac  ", " bac "),
        ("", " "),
        ("!?", " "),
    ],
)
def test_normalization_decomposes_lowercases_and_collapses_spaces(
    codec: Codec, text: str, expected: str
) -> None:
    """normalize_to_alphabet mirrors corpus normalization within the codec alphabet."""
    normalized = normalize_to_alphabet(text, codec)

    assert normalized == expected
    assert normalize_to_alphabet(normalized, codec) == normalized
    assert codec.decode(encode_fast(normalized, codec).tolist()) == expected


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason=(
        "Issue #27: normalize_to_alphabet replaces combining marks with "
        "spaces; corpus normalizers drop them"
    ),
)
def test_normalization_drops_combining_marks_like_corpus_builders(codec: Codec) -> None:
    """normalize_to_alphabet should drop combining marks, as the corpus builders do."""
    assert normalize_to_alphabet("\u00c1b", codec) == "ab"

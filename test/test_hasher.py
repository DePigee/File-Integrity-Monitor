import hashlib

import pytest

from integrity_monitor.hasher import hash_file


def test_known_value(tmp_path):
    file = tmp_path / "a.txt"
    file.write_text("hello")
    expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    assert hash_file(str(file)) == expected


def test_same_content_same_hash(tmp_path):
    first = tmp_path / "a.txt"
    second = tmp_path / "b.txt"
    first.write_text("same content")
    second.write_text("same content")
    assert hash_file(str(first)) == hash_file(str(second))


def test_different_content_different_hash(tmp_path):
    first = tmp_path / "a.txt"
    second = tmp_path / "b.txt"
    first.write_text("hello")
    second.write_text("hellp")
    assert hash_file(str(first)) != hash_file(str(second))


def test_empty_file(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("")
    result = hash_file(str(file))
    assert len(result) == 64


def test_large_file_spans_multiple_chunks(tmp_path):
    file = tmp_path / "big.txt"
    data = "a" * 100_000
    file.write_text(data)
    expected = hashlib.sha256(data.encode()).hexdigest()
    assert hash_file(str(file)) == expected


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        hash_file(str(tmp_path / "does_not_exist.txt"))
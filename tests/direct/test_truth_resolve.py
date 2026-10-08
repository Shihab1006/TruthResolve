import json
import pytest


def test_initial_state(direct_deploy):
    contract = direct_deploy("contracts/truth_resolve.py")
    assert contract.get_claim() == ""
    assert contract.get_result() == ""
    assert json.loads(contract.get_sources()) == {
        "source_a": "",
        "source_b": "",
    }


def test_rejects_empty_claim(direct_deploy):
    contract = direct_deploy("contracts/truth_resolve.py")
    with pytest.raises(Exception):
        contract.verify_claim(
            "",
            "https://example.com/a",
            "https://example.com/b",
        )


def test_rejects_invalid_url(direct_deploy):
    contract = direct_deploy("contracts/truth_resolve.py")
    with pytest.raises(Exception):
        contract.verify_claim(
            "Example claim",
            "not-a-url",
            "https://example.com/b",
        )

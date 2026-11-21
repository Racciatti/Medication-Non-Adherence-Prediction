import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import utils  # noqa: E402


def test_every_module_has_selected_vars_with_seqn():
    assert set(utils.MODULE_FILENAMES) == set(utils.SELECTED_VARS_PER_MODULE)
    for module, cols in utils.SELECTED_VARS_PER_MODULE.items():
        assert cols[0] == "SEQN", module


def test_load_module_unknown_name_raises():
    with pytest.raises(ValueError):
        utils.load_module("does_not_exist")


def test_verify_variables_detects_missing(capsys):
    df = pd.DataFrame({"SEQN": [1], "DLQ010": [1]})
    assert utils.verify_variables(df, "disability") is False
    assert "Missing variables" in capsys.readouterr().out


def test_verify_variables_ok():
    cols = utils.SELECTED_VARS_PER_MODULE["sleep_disorders"]
    assert utils.verify_variables(pd.DataFrame({c: [1] for c in cols}), "sleep_disorders", verbose=False)

import os.path
import shutil

import joblib

from mesmer.calibrate_mesmer import _calibrate_and_draw_realisations

from .utils import _check_dict


def test_calibrate_mesmer(test_data_root_dir, tmpdir, update_expected_files):
    expected_output_file = os.path.join(test_data_root_dir, "test-mesmer-bundle.pkl")

    test_esms = ["IPSL-CM6A-LR"]
    test_scenarios_to_train = ["h-ssp126"]
    test_target_variable = "tas"
    test_reg_type = "srex"
    test_threshold_land = 1 / 3
    test_output_file = os.path.join(tmpdir, "test_calibrate_mesmer_output.pkl")
    test_scen_seed_offset_v = 0
    test_cmip_generation = 6
    test_cmip_data_root_dir = os.path.join(
        test_data_root_dir,
        "calibrate-coarse-grid",
        f"cmip{test_cmip_generation}-ng",
    )
    test_observations_root_dir = os.path.join(
        test_data_root_dir,
        "calibrate-coarse-grid",
        "observations",
    )
    test_auxiliary_data_dir = os.path.join(
        test_data_root_dir,
        "calibrate-coarse-grid",
        "auxiliary",
    )

    _calibrate_and_draw_realisations(
        esms=test_esms,
        scenarios_to_train=test_scenarios_to_train,
        target_variable=test_target_variable,
        reg_type=test_reg_type,
        threshold_land=test_threshold_land,
        output_file=test_output_file,
        scen_seed_offset_v=test_scen_seed_offset_v,
        cmip_data_root_dir=test_cmip_data_root_dir,
        cmip_generation=test_cmip_generation,
        observations_root_dir=test_observations_root_dir,
        auxiliary_data_dir=test_auxiliary_data_dir,
    )

    res = joblib.load(test_output_file)

    if update_expected_files:
        shutil.copyfile(test_output_file, expected_output_file)
    else:
        exp = joblib.load(expected_output_file)

        assert isinstance(res, dict)
        assert type(res) == type(exp)
        assert res.keys() == exp.keys()

        # check all keys of res match exp
        _check_dict(res, exp, "result", "expected")
        # check all keys of exp match res
        _check_dict(exp, res, "expected", "result")

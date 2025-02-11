import numpy as np
import pytest
import xarray as xr

import mesmer.core.utils


@pytest.mark.parametrize("obj", (None, xr.DataArray()))
def test_check_dataset_form_wrong_type(obj):

    with pytest.raises(TypeError, match="Expected obj to be an xr.Dataset"):
        mesmer.core.utils._check_dataset_form(obj)

    with pytest.raises(TypeError, match="Expected test to be an xr.Dataset"):
        mesmer.core.utils._check_dataset_form(obj, name="test")


def test_check_dataset_form_required_vars():

    ds = xr.Dataset()

    with pytest.raises(ValueError, match="obj is missing the required data_vars"):
        mesmer.core.utils._check_dataset_form(ds, required_vars="missing")

    with pytest.raises(ValueError, match="test is missing the required data_vars"):
        mesmer.core.utils._check_dataset_form(ds, "test", required_vars="missing")

    # no error
    mesmer.core.utils._check_dataset_form(ds)
    mesmer.core.utils._check_dataset_form(ds, required_vars=set())
    mesmer.core.utils._check_dataset_form(ds, required_vars=None)

    ds = xr.Dataset(data_vars={"var": ("x", [0])})

    # no error
    mesmer.core.utils._check_dataset_form(ds)
    mesmer.core.utils._check_dataset_form(ds, required_vars="var")
    mesmer.core.utils._check_dataset_form(ds, required_vars={"var"})


def test_check_dataset_form_requires_other_vars():

    ds = xr.Dataset()

    with pytest.raises(ValueError, match="Expected additional variables on obj"):
        mesmer.core.utils._check_dataset_form(ds, requires_other_vars=True)

    with pytest.raises(ValueError, match="Expected additional variables on test"):
        mesmer.core.utils._check_dataset_form(ds, "test", requires_other_vars=True)

    with pytest.raises(ValueError, match="Expected additional variables on obj"):
        mesmer.core.utils._check_dataset_form(
            ds, optional_vars="var", requires_other_vars=True
        )

    ds = xr.Dataset(data_vars={"var": ("x", [0])})

    with pytest.raises(ValueError, match="Expected additional variables on obj"):
        mesmer.core.utils._check_dataset_form(
            ds, required_vars="var", requires_other_vars=True
        )

    with pytest.raises(ValueError, match="Expected additional variables on obj"):
        mesmer.core.utils._check_dataset_form(
            ds, optional_vars="var", requires_other_vars=True
        )


@pytest.mark.parametrize("obj", (None, xr.Dataset()))
def test_check_dataarray_form_wrong_type(obj):

    with pytest.raises(TypeError, match="Expected obj to be an xr.DataArray"):
        mesmer.core.utils._check_dataarray_form(obj)

    with pytest.raises(TypeError, match="Expected test to be an xr.DataArray"):
        mesmer.core.utils._check_dataarray_form(obj, name="test")


@pytest.mark.parametrize("ndim", (0, 1, 3))
def test_check_dataarray_form_ndim(ndim):

    da = xr.DataArray(np.ones((2, 2)))

    with pytest.raises(ValueError, match=f"obj should be {ndim}-dimensional"):
        mesmer.core.utils._check_dataarray_form(da, ndim=ndim)

    with pytest.raises(ValueError, match=f"test should be {ndim}-dimensional"):
        mesmer.core.utils._check_dataarray_form(da, ndim=ndim, name="test")

    # no error
    mesmer.core.utils._check_dataarray_form(da, ndim=2)


@pytest.mark.parametrize("required_dims", ("foo", ["foo"], ["foo", "bar"]))
def test_check_dataarray_form_required_dims(required_dims):

    da = xr.DataArray(np.ones((2, 2)), dims=("x", "y"))

    with pytest.raises(ValueError, match="obj is missing the required dims"):
        mesmer.core.utils._check_dataarray_form(da, required_dims=required_dims)

    with pytest.raises(ValueError, match="test is missing the required dims"):
        mesmer.core.utils._check_dataarray_form(
            da, required_dims=required_dims, name="test"
        )

    # no error
    mesmer.core.utils._check_dataarray_form(da, required_dims="x")
    mesmer.core.utils._check_dataarray_form(da, required_dims="y")
    mesmer.core.utils._check_dataarray_form(da, required_dims=["x", "y"])
    mesmer.core.utils._check_dataarray_form(da, required_dims={"x", "y"})


def test_check_dataarray_form_shape():

    da = xr.DataArray(np.ones((2, 2)), dims=("x", "y"))

    for shape in ((), (1,), (1, 2), (2, 1), (1, 2, 3)):
        with pytest.raises(ValueError, match="obj has wrong shape"):
            mesmer.core.utils._check_dataarray_form(da, shape=shape)

    with pytest.raises(ValueError, match="test has wrong shape"):
        mesmer.core.utils._check_dataarray_form(da, name="test", shape=())

    # no error
    mesmer.core.utils._check_dataarray_form(da, shape=(2, 2))

import copy
from pathlib import Path
from typing import Callable

import numpy as np
import pytest


@pytest.fixture
def minimum_config(tmp_path: Path) -> dict:
    """Create a minimum configuration.

    Parameters
    ----------
    tmp_path : Path
        Temporary path for testing.

    Returns
    -------
    dict
        A minumum configuration example.
    """
    # create dictionary
    configuration = {
        "experiment_name": "LevitatingFrog",
        "working_directory": str(tmp_path),
        "algorithm": {
            "loss": "n2v",
            "model": "UNet",
            "is_3D": False,
        },
        "training": {
            "num_epochs": 666,
            "batch_size": 42,
            "patch_size": [64, 64],
            "optimizer": {
                "name": "Adam",
            },
            "lr_scheduler": {"name": "ReduceLROnPlateau"},
            "augmentation": True,
        },
        "data": {
            "in_memory": True,
            "data_format": "tif",
            "axes": "SYX",
        },
    }

    return configuration


@pytest.fixture
def complete_config(minimum_config: dict) -> dict:
    """Create a complete configuration.

    This configuration should not be used for testing an Engine.

    Parameters
    ----------
    minimum_config : dict
        A minimum configuration.

    Returns
    -------
    dict
        A complete configuration example.
    """
    # add to configuration
    complete_config = copy.deepcopy(minimum_config)

    complete_config["algorithm"]["masking_strategy"] = "median"

    complete_config["algorithm"]["masked_pixel_percentage"] = 0.6
    complete_config["algorithm"]["roi_size"] = 13
    complete_config["algorithm"]["model_parameters"] = {
        "depth": 8,
        "num_channels_init": 32,
    }

    complete_config["training"]["optimizer"]["parameters"] = {
        "lr": 0.00999,
    }
    complete_config["training"]["lr_scheduler"]["parameters"] = {
        "patience": 22,
    }
    complete_config["training"]["use_wandb"] = True
    complete_config["training"]["num_workers"] = 6
    complete_config["training"]["amp"] = {
        "use": True,
        "init_scale": 512,
    }
    complete_config["data"]["in_memory"] = False
    complete_config["data"]["mean"] = 666.666
    complete_config["data"]["std"] = 42.420

    return complete_config


@pytest.fixture
def ordered_array() -> Callable:
    """A function that returns an array with ordered values."""

    def _ordered_array(shape: tuple, dtype=int) -> np.ndarray:
        """An array with ordered values.

        Parameters
        ----------
        shape : tuple
            Shape of the array.

        Returns
        -------
        np.ndarray
            Array with ordered values.
        """
        return np.arange(np.prod(shape), dtype=dtype).reshape(shape)

    return _ordered_array


@pytest.fixture
def array_2D(ordered_array) -> np.ndarray:
    """A 2D array with shape (1, 10, 9).

    Returns
    -------
    np.ndarray
        2D array with shape (1, 10, 9).
    """
    return ordered_array((1, 10, 9))


@pytest.fixture
def array_3D(ordered_array) -> np.ndarray:
    """A 3D array with shape (1, 5, 10, 9).

    Returns
    -------
    np.ndarray
        3D array with shape (1, 5, 10, 9).
    """
    return ordered_array((1, 8, 16, 16))

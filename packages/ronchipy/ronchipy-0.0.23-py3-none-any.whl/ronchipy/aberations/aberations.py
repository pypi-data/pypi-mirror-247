from __future__ import annotations

import numpy as np
from scipy import constants


def abberations_2D(
    rho: np.ndarray,
    phi: np.ndarray,
    wavelength: float,
    parameters: dict[str, float],
) -> np.ndarray:
    out = np.zeros(shape=rho.shape, dtype=np.complex64)

    array_1 = (
        1
        / 2
        * rho**2
        * (
            parameters["C10"]
            + parameters["C12"] * np.cos(2 * (phi - parameters["phi12"]))
        )
    )

    array_2 = (
        1
        / 3
        * rho**3
        * (
            parameters["C21"] * np.cos(phi - parameters["phi21"])
            + parameters["C23"] * np.cos(3 * (phi - parameters["phi23"]))
        )
    )

    array_3 = (
        1
        / 4
        * rho**4
        * (
            parameters["C30"]
            + parameters["C32"] * np.cos(2 * (phi - parameters["phi32"]))
            + parameters["C34"] * np.cos(4 * (phi - parameters["phi34"]))
        )
    )

    array_4 = (
        1
        / 5
        * rho**5
        * (
            parameters["C41"] * np.cos((phi - parameters["phi41"]))
            + parameters["C43"] * np.cos(3 * (phi - parameters["phi43"]))
            + parameters["C45"] * np.cos(5 * (phi - parameters["phi45"]))
        )
    )

    array_5 = (
        1
        / 6
        * rho**6
        * (
            parameters["C50"]
            + parameters["C52"] * np.cos(2 * (phi - parameters["phi52"]))
            + parameters["C54"] * np.cos(4 * (phi - parameters["phi54"]))
            + parameters["C56"] * np.cos(6 * (phi - parameters["phi56"]))
        )
    )

    out += array_1 + array_2 + array_3 + array_4 + array_5

    out *= np.float32(2 * np.pi / (wavelength / constants.angstrom))

    out = np.exp(1.0j * -out)

    # out = np.cos(out) + 1.j * np.sin(out)

    return out


def abberations_2D_array(
    rho: np.ndarray,
    phi: np.ndarray,
    wavelength: float,
    parameters: np.ndarray,
) -> np.ndarray:
    out = np.zeros(shape=rho.shape, dtype=np.complex64)

    array_1 = (
        1
        / 2
        * rho**2
        * (parameters[0] + parameters[1] * np.cos(2 * (phi - parameters[2])))
    )

    array_2 = (
        1
        / 3
        * rho**3
        * (
            parameters[3] * np.cos(phi - parameters[4])
            + parameters[5] * np.cos(3 * (phi - parameters[6]))
        )
    )

    array_3 = (
        1
        / 4
        * rho**4
        * (
            parameters[7]
            + parameters[8] * np.cos(2 * (phi - parameters[9]))
            + parameters[10] * np.cos(4 * (phi - parameters[11]))
        )
    )

    array_4 = (
        1
        / 5
        * rho**5
        * (
            parameters[12] * np.cos((phi - parameters[13]))
            + parameters[14] * np.cos(3 * (phi - parameters[15]))
            + parameters[16] * np.cos(5 * (phi - parameters[17]))
        )
    )

    array_5 = (
        1
        / 6
        * rho**6
        * (
            parameters[18]
            + parameters[19] * np.cos(2 * (phi - parameters[20]))
            + parameters[21] * np.cos(4 * (phi - parameters[22]))
            + parameters[23] * np.cos(6 * (phi - parameters[24]))
        )
    )

    out += array_1 + array_2 + array_3 + array_4 + array_5

    out *= np.float32(2 * np.pi / (wavelength / constants.angstrom))

    out = np.exp(1.0j * -out)

    # out = np.cos(out) + 1.j * np.sin(out)

    return out


parameters = {
    "C10": 1e6,
    "C12": -0.849 * 1e-4 / constants.angstrom,
    "phi12": np.deg2rad(30) / 1e3,
    "C21": 1.38 * 10,
    "phi21": np.deg2rad(0),
    "C23": 1.59 * 1e7,
    "phi23": np.deg2rad(-120),
    "C30": 325 * 10,
    "C32": -118 * 5e6,
    "phi32": np.deg2rad(50),  # np.deg2rad(),
    "C34": 65.1 * 10,
    "phi34": 0.0,
    "C41": 2.23 * 1e-6 / constants.angstrom,
    "phi41": 0.0,
    "C43": -6.13 * 1e-6 / constants.angstrom,
    "phi43": 0.0,
    "C45": -7.44 * 1e-6 / constants.angstrom,
    "phi45": 0.0,
    "C50": -0.201 * 1e-3 / constants.angstrom,
    "C52": 0.131 * 1e-3 / constants.angstrom,
    "phi52": 0.0,
    "C54": -0.001 * 1e-3 / constants.angstrom,
    "phi54": 0.0,
    "C56": -223 * 1e-2 / constants.angstrom,
    "phi56": np.deg2rad(180),
}

params_array = np.array([*parameters.values()])

from __future__ import annotations

import numpy as np
from scipy import constants


def calculate_wavelength(
    keV: float,
) -> float:
    """
    Calculates the relitivisically corrected wavelength of the electron
    """
    # convert to energy in J
    energy_J = keV * 1_000 * constants.electron_volt

    # calculat the relitivisticly corrected wavelength of the electon
    wavelength = constants.h / np.sqrt(
        2
        * constants.electron_mass
        * energy_J
        * (1 + energy_J / (2 * constants.electron_mass * constants.c**2))
    )
    return wavelength


def calculate_relativistic_mass_correction(
    keV: float,
) -> float:
    """ """
    return 1 + constants.electron_volt * keV * 1e3 / (
        constants.electron_mass * constants.c**2
    )


def calculate_electron_mass_from_energy(keV: float) -> float:
    """
    calculates in kg
    """

    return constants.electron_mass * calculate_relativistic_mass_correction(keV)


def calculate_sigma(
    keV: float,
) -> float:
    sigma = (
        2
        * np.pi
        * calculate_electron_mass_from_energy(keV)
        * constants.elementary_charge
        * calculate_wavelength(keV)
        / constants.h**2
    )

    return sigma


def polar_to_cart(rho, phi):
    x, y = rho * np.cos(phi), rho * np.sin(phi)
    return x, y


def cart_to_polar(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi


def spatial_frequencies(
    im_size: tuple[int, int], sampling: tuple[int, int], return_grid: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    # out = ()
    # for n, d in zip(im_size, sampling, strict=True):
    #     out += np.fft.fftfreq(n,d)
    kx = np.fft.fftfreq(im_size[0], sampling[0])
    ky = np.fft.fftfreq(im_size[1], sampling[1])
    if return_grid:
        return np.meshgrid(kx, ky, indexing="ij")
    else:
        return (ky, ky)


def polar_spatial_frequencies(
    im_size: tuple[int, int],
    sampling: tuple[int, int],
) -> tuple[np.ndarray, np.ndarray]:
    kx, ky = np.fft.fftshift(
        spatial_frequencies(im_size=im_size, sampling=sampling, return_grid=False)
    )
    rho = np.sqrt(kx[:, None] ** 2 + ky[None] ** 2)
    phi = np.arctan2(ky[None], kx[:, None])

    return (rho, phi)

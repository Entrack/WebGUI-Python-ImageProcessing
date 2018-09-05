# coding=utf-8
# rgb2lab([0..255]), borrowed https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python
from math import pow, sqrt, atan2, degrees, radians, cos, sin, exp

import numpy as np


def rgb2lab(input_color):
    num = 0
    RGB = [0, 0, 0]
    for value in input_color:
        value = float(value) / 255
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92
        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]
    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)
    XYZ[0] = float(XYZ[0]) / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[1] = float(XYZ[1]) / 100.0  # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883
    num = 0
    for value in XYZ:
        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)
        XYZ[num] = value
        num = num + 1
    Lab = [0, 0, 0]
    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])
    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)
    return Lab


def CIEDERGB(RGB1, RGB2):
    return CIEDE2000(rgb2lab(RGB1), rgb2lab(RGB2))

# https://en.wikipedia.org/wiki/Color_difference#CIEDE2000
def CIEDE2000((L1, a1, b1), (L2, a2, b2)):
    kl = 1.
    kc = 1.
    kh = 1.
    dL_ = L2 - L1
    C1 = sqrt(pow(a1, 2) + pow(b1, 2))
    C2 = sqrt(pow(a2, 2) + pow(b2, 2))
    Lline = (L1 + L2) / 2
    Cline = (C1 + C2) / 2
    a1_ = a1 + a1 / 2 * (1 - sqrt(pow(Cline, 7) / (pow(Cline, 7) + pow(25, 7))))
    a2_ = a2 + a2 / 2 * (1 - sqrt(pow(Cline, 7) / (pow(Cline, 7) + pow(25, 7))))
    C1_ = sqrt(pow(a1_, 2) + pow(b1, 2))
    C2_ = sqrt(pow(a2_, 2) + pow(b2, 2))
    Cline_ = (C1_ + C2_) / 2
    dC_ = C2_ - C1_
    h1_ = degrees(atan2(b1, a1_)) % 360
    h2_ = degrees(atan2(b2, a2_)) % 360
    if abs(h1_ - h2_) <= 180:
        dh_ = h2_ - h1_
    elif h2_ <= h1_:
        dh_ = h2_ - h1_ + 360
    else:
        dh_ = h2_ - h1_ - 360
    dH_ = 2 * sqrt(C1_ * C2_) * sin(radians(dh_ / 2))
    if abs(h1_ - h2_) <= 180:
        H_ = (h1_ + h2_) / 2
    elif h1_ + h2_ < 360:
        H_ = (h1_ + h2_ + 360) / 2
    else:
        H_ = (h1_ + h2_ - 360) / 2
    T = 1 - 0.17 * cos(radians(H_ - 30)) + 0.24 * cos(radians(2 * H_)) + 0.32 * cos(radians(3 * H_ + 6)) - 0.20 * cos(
        radians(4 * H_ - 63))
    Sl = 1 + 0.015 * pow(Lline - 50, 2) / sqrt(20 + pow(Lline - 50, 2))
    Sc = 1 + 0.045 * Cline_
    Sh = 1 + 0.015 * Cline_ * T
    Rt = -2 * sqrt(pow(Cline, 7) / (pow(Cline, 7) + pow(25, 7))) * sin(radians(60 * exp(-pow((H_ - 275) / 25, 2))))
    dE00 = sqrt(pow(dL_ / (kl * Sl), 2) + pow(dC_ / (kc * Sc), 2) + pow(dH_ / (kh * Sh), 2) + Rt * (dC_ / (kc * Sc)) * (
            dH_ / (kh * Sh)))
    return dE00


def _cart2polar_2pi(x, y):
    """convert cartesian coordiantes to polar (uses non-standard theta range!)

    NON-STANDARD RANGE! Maps to ``(0, 2*pi)`` rather than usual ``(-pi, +pi)``
    """
    r, t = np.hypot(x, y), np.arctan2(y, x)
    t += np.where(t < 0., 2 * np.pi, 0)
    return r, t


def deltaE_ciede2000(lab1, lab2, kL=1, kC=1, kH=1):
    """Color difference as given by the CIEDE 2000 standard.
    CIEDE 2000 is a major revision of CIDE94.  The perceptual calibration is
    largely based on experience with automotive paint on smooth surfaces.
    Parameters
    ----------
    lab1 : array_like
        reference color (Lab colorspace)
    lab2 : array_like
        comparison color (Lab colorspace)
    kL : float (range), optional
        lightness scale factor, 1 for "acceptably close"; 2 for "imperceptible"
        see deltaE_cmc
    kC : float (range), optional
        chroma scale factor, usually 1
    kH : float (range), optional
        hue scale factor, usually 1
    Returns
    -------
    deltaE : array_like
        The distance between `lab1` and `lab2`
    Notes
    -----
    CIEDE 2000 assumes parametric weighting factors for the lightness, chroma,
    and hue (`kL`, `kC`, `kH` respectively).  These default to 1.
    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Color_difference
    .. [2] http://www.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf
           (doi:10.1364/AO.33.008069)
    .. [3] M. Melgosa, J. Quesada, and E. Hita, "Uniformity of some recent
           color metrics tested with an accurate color-difference tolerance
           dataset," Appl. Opt. 33, 8069-8077 (1994).
    """
    lab1 = np.asarray(lab1)
    lab2 = np.asarray(lab2)
    unroll = False
    if lab1.ndim == 1 and lab2.ndim == 1:
        unroll = True
        if lab1.ndim == 1:
            lab1 = lab1[None, :]
        if lab2.ndim == 1:
            lab2 = lab2[None, :]
    L1, a1, b1 = np.rollaxis(lab1, -1)[:3]
    L2, a2, b2 = np.rollaxis(lab2, -1)[:3]

    # distort `a` based on average chroma
    # then convert to lch coordines from distorted `a`
    # all subsequence calculations are in the new coordiantes
    # (often denoted "prime" in the literature)
    Cbar = 0.5 * (np.hypot(a1, b1) + np.hypot(a2, b2))
    c7 = Cbar ** 7
    G = 0.5 * (1 - np.sqrt(c7 / (c7 + 25 ** 7)))
    scale = 1 + G
    C1, h1 = _cart2polar_2pi(a1 * scale, b1)
    C2, h2 = _cart2polar_2pi(a2 * scale, b2)
    # recall that c, h are polar coordiantes.  c==r, h==theta

    # cide2000 has four terms to delta_e:
    # 1) Luminance term
    # 2) Hue term
    # 3) Chroma term
    # 4) hue Rotation term

    # lightness term
    Lbar = 0.5 * (L1 + L2)
    tmp = (Lbar - 50) ** 2
    SL = 1 + 0.015 * tmp / np.sqrt(20 + tmp)
    L_term = (L2 - L1) / (kL * SL)

    # chroma term
    Cbar = 0.5 * (C1 + C2)  # new coordiantes
    SC = 1 + 0.045 * Cbar
    C_term = (C2 - C1) / (kC * SC)

    # hue term
    h_diff = h2 - h1
    h_sum = h1 + h2
    CC = C1 * C2

    dH = h_diff.copy()
    dH[h_diff > np.pi] -= 2 * np.pi
    dH[h_diff < -np.pi] += 2 * np.pi
    dH[CC == 0.] = 0.  # if r == 0, dtheta == 0
    dH_term = 2 * np.sqrt(CC) * np.sin(dH / 2)

    Hbar = h_sum.copy()
    mask = np.logical_and(CC != 0., np.abs(h_diff) > np.pi)
    Hbar[mask * (h_sum < 2 * np.pi)] += 2 * np.pi
    Hbar[mask * (h_sum >= 2 * np.pi)] -= 2 * np.pi
    Hbar[CC == 0.] *= 2
    Hbar *= 0.5

    T = (1 -
         0.17 * np.cos(Hbar - np.deg2rad(30)) +
         0.24 * np.cos(2 * Hbar) +
         0.32 * np.cos(3 * Hbar + np.deg2rad(6)) -
         0.20 * np.cos(4 * Hbar - np.deg2rad(63))
         )
    SH = 1 + 0.015 * Cbar * T

    H_term = dH_term / (kH * SH)

    # hue rotation
    c7 = Cbar ** 7
    Rc = 2 * np.sqrt(c7 / (c7 + 25 ** 7))
    dtheta = np.deg2rad(30) * np.exp(-((np.rad2deg(Hbar) - 275) / 25) ** 2)
    R_term = -np.sin(2 * dtheta) * Rc * C_term * H_term

    # put it all together
    dE2 = L_term ** 2
    dE2 += C_term ** 2
    dE2 += H_term ** 2
    dE2 += R_term
    ans = np.sqrt(dE2)
    if unroll:
        ans = ans[0]
    return ans

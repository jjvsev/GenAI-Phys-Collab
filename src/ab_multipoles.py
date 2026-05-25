from typing import Literal

import mph


M = 4
MULTIPOLES_TE = [
    "a10_te", "a11_te", "a1m1_te",
    "a20_te", "a21_te", "a2m1_te", "a22_te", "a2m2_te",
    "a30_te", "a31_te", "a3m1_te", "a32_te", "a3m2_te", "a33_te", "a3m3_te",
    "a40_te", "a41_te", "a4m1_te", "a42_te", "a4m2_te", "a43_te", "a4m3_te", "a44_te", "a4m4_te",

    "b10_te", "b11_te", "b1m1_te",
    "b20_te", "b21_te", "b2m1_te", "b22_te", "b2m2_te",
    "b30_te", "b31_te", "b3m1_te", "b32_te", "b3m2_te", "b33_te", "b3m3_te",
    "b40_te", "b41_te", "b4m1_te", "b42_te", "b4m2_te", "b43_te", "b4m3_te", "b44_te", "b4m4_te",
]
MULTIPOLES_TM = [
    "a10_tm", "a11_tm", "a1m1_tm",
    "a20_tm", "a21_tm", "a2m1_tm", "a22_tm", "a2m2_tm",
    "a30_tm", "a31_tm", "a3m1_tm", "a32_tm", "a3m2_tm", "a33_tm", "a3m3_tm",
    "a40_tm", "a41_tm", "a4m1_tm", "a42_tm", "a4m2_tm", "a43_tm", "a4m3_tm", "a44_tm", "a4m4_tm",

    "b10_tm", "b11_tm", "b1m1_tm",
    "b20_tm", "b21_tm", "b2m1_tm", "b22_tm", "b2m2_tm",
    "b30_tm", "b31_tm", "b3m1_tm", "b32_tm", "b3m2_tm", "b33_tm", "b3m3_tm",
    "b40_tm", "b41_tm", "b4m1_tm", "b42_tm", "b4m2_tm", "b43_tm", "b4m3_tm", "b44_tm", "b4m4_tm",
]


def eval_ab(
    model: mph.Model,
    pol: Literal["te", "tm"],
    multipoles: list[str],
) -> dict[str, dict[int, dict[int, complex]]]:
    """Evaluates the multipole coefficients from the model and organizes them in a dictionary"""
    ab_eval = {}
    for multipole in multipoles:
        ab_eval[multipole] = model.evaluate(multipole)
    
    Midx = {m: idx for idx, m in enumerate(range(-M, M+1))}
    result = {
        "a": {n: {m: 0 + 0j for m in range(-n, n+1)} for n in range(1, M+1)},
        "b": {n: {m: 0 + 0j for m in range(-n, n+1)} for n in range(1, M+1)},
    }

    for n in range(1, M + 1):
        for m in range(-n, n+1):
            fmt_a = f'a{n}{m}_{pol}' if m >= 0 else f'a{n}m{-m}_{pol}'
            fmt_b = f'b{n}{m}_{pol}' if m >= 0 else f'b{n}m{-m}_{pol}'
            result["a"][n][m] = ab_eval[fmt_a][Midx[m]]
            result["b"][n][m] = ab_eval[fmt_b][Midx[m]]
    
    return result
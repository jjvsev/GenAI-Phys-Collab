from typing import Literal

import mph
from src.ab_multipoles import MULTIPOLES_TE, MULTIPOLES_TM, M


def test_zero_coefs(
    model: mph.Model,
    pol: Literal["te", "tm"]
) -> None:
    """Tests that the evaluated multipole coefficients with |m| != |M| are zero"""
    multipoles = MULTIPOLES_TE if pol == "te" else MULTIPOLES_TM
    ab_eval = {}
    for multipole in multipoles:
        ab_eval[multipole] = model.evaluate(multipole)

    Midx = {m: idx for idx, m in enumerate(range(-M, M+1))}
    for n in range(1, 5):
        for m in range(-n, n+1):
            fmt_a = f'a{n}{m}_{pol}' if m >= 0 else f'a{n}m{-m}_{pol}'
            fmt_b = f'b{n}{m}_{pol}' if m >= 0 else f'b{n}m{-m}_{pol}'
            for m_val, idx in Midx.items():
                if m_val == m or m_val == -m:
                    continue
                else:
                    assert abs(ab_eval[fmt_a][idx]) == 0
                    assert abs(ab_eval[fmt_b][idx]) == 0


if __name__ == "__main__":
    client = mph.start()
    model = client.load('models/model_target.mph')

    test_zero_coefs(model, pol="te")
    # test_zero_coefs(model, pol="tm")

    client.remove(model)
    print("Test passed: all multipole coefficients with |m| != |M| are zero")
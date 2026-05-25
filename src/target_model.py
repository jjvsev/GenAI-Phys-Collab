import mph
from src.ab_multipoles import MULTIPOLES_TE, eval_ab
from src.cylinder import SingleCylinder, build_cylinders
import numpy as np
import pickle

from src.prepare_model import N_CYL, CYL_DIAMETER, CYL_HEIGHT


def prepare_target_model() -> None:
    client = mph.start()
    model = client.load('models/model.mph')

    rng = np.random.default_rng(seed=24)
    r = (CYL_DIAMETER - CYL_DIAMETER / 3 * (rng.random(N_CYL) - 0.5)) / 2
    cylinders = [SingleCylinder(h=CYL_HEIGHT / N_CYL, r=ri) for ri in r]

    build_cylinders(model, cylinders)

    model.solve()
    
    result_te = eval_ab(model=model, pol='te', multipoles=MULTIPOLES_TE)

    with open("target.pkl", "wb") as f:
        pickle.dump(result_te, f)
    
    model.save("models/model_target.mph")
    client.remove(model)


if __name__ == "__main__":
    prepare_target_model()

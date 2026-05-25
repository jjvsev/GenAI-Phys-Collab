from typing import Literal
import numpy as np

import mph

from src.cylinder import SingleCylinder, build_cylinders


# all lengths are in nm
CYL_HEIGHT = 800
CYL_DIAMETER = 600
N_CYL = 10



def setup_full_fields(model: mph.Model) -> None:
    comp = model.java.component("comp1")

    var_tag = "var_full_fields"

    comp.variable().create(var_tag)
    var = comp.variable(var_tag)
    var.label("full fields")

    variables = {
        "Er_full":   "sum(withsol('sol1', ewfd.Er, setval(M,mm))*exp(i*mm*phi_cut), mm, -4, 4)",
        "Ephi_full": "sum(withsol('sol1', ewfd.Ephi, setval(M,mm))*exp(i*mm*phi_cut), mm, -4, 4)",
        "Ez_full":   "sum(withsol('sol1', ewfd.Ez, setval(M,mm))*exp(i*mm*phi_cut), mm, -4, 4)",
        "Ex_full":   "Er_full*cos(phi_cut) - Ephi_full*sin(phi_cut)",
        "Ey_full":   "Er_full*sin(phi_cut) + Ephi_full*cos(phi_cut)",
        "Eabs_full": "sqrt(abs(Ex_full)^2 + abs(Ey_full)^2 + abs(Ez_full)^2)",

        "E2r_full":    "sum(withsol('sol1', ewfd2.Er, setval(M,mm))*exp(i*mm*phi_cut), mm, -4, 4)",
        "E2phi_full": "sum(withsol('sol1', ewfd2.Ephi, setval(M,mm))*exp(i*mm*phi_cut), mm, -4, 4)",
        "E2z_full":    "sum(withsol('sol1', ewfd2.Ez, setval(M,mm))*exp(i*mm*phi_cut), mm, -4, 4)",
        "E2x_full":    "E2r_full*cos(phi_cut) - E2phi_full*sin(phi_cut)",
        "E2y_full":    "E2r_full*sin(phi_cut) + E2phi_full*cos(phi_cut)",
        "E2abs_full":  "sqrt(abs(E2x_full)^2 + abs(E2y_full)^2 + abs(E2z_full)^2)",
    }

    for name, expr in variables.items():
        var.set(name, expr)
        var.descr(name, "")



def prepare_model(
    polarization: Literal["TM", "TE"] | None = None,
    delete_plots: bool = True,
) -> None:
    # load model
    client = mph.start()  # type: ignore
    model = client.load('models/2d_mult_dec.mph')

    # clear model
    model.clear()

    # remove results
    model.java.result().table().remove('tbl1')
    if delete_plots:
        model.java.result().remove('pg1')
        model.java.result().remove('pg2')

    # set up parameters
    model.parameter('cyl_h', str(CYL_HEIGHT) + '[nm]')
    model.parameter('diam_cyl', str(CYL_DIAMETER) + '[nm]')
    model.parameter('phi_cut', '0[rad]')

    # set up full fields variables
    setup_full_fields(model)

    # remove geometry
    model.remove(model / "geometries" / "Geometry 1" / "Rectangle 1")

    # create initial polygon
    h = CYL_HEIGHT / N_CYL
    rng = np.random.default_rng(seed=42)
    r = (CYL_DIAMETER - CYL_DIAMETER / 3 * (rng.random(N_CYL) - 0.5)) / 2
    cylinders = [SingleCylinder(h=h, r=ri) for ri in r]
    build_cylinders(model, cylinders, create_new=True)

    # leave one polarization
    if polarization:
        pol_to_delete = "TE" if polarization == "TM" else "2 TM"
        (model / 'physics' / f'Electromagnetic Waves, Frequency Domain {pol_to_delete}').toggle('off')

    # set up parametric sweep
    sweep = model / "studies" / "Scattering" / "Parametric Sweep"
    sweep.property("pname", ["M"])
    sweep.property("plistarr", ["range(-4,1,4)"])

    # save model
    model.save("models/model.mph")


if __name__ == "__main__":
    prepare_model(
        delete_plots=False,
        polarization="TE",
    )

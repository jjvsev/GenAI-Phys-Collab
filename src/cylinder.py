from dataclasses import dataclass
import re
import matplotlib.pyplot as plt
import numpy as np

import mph


@dataclass(eq=True, frozen=True)
class SingleCylinder:
    h: float
    r: float


def polygon_dots(cylinders: list[SingleCylinder]) -> np.ndarray:
    """Returns the coordinates of the dots that define the polygon for the given list of cylinders"""
    dots = [(0., 0.)]
    H = 0
    for cylinder in cylinders:
        dots.append((cylinder.r, H))
        H += cylinder.h
        dots.append((cylinder.r, H))
    dots.append((0., H))
    dots = np.array(dots)
    dots[:, 1] = dots[:, 1] - H/2
    return dots


def build_cylinders(
    model: mph.Model,
    cylinders: list[SingleCylinder],
    create_new: bool = False
) -> None:
    """Builds the polygon from cylinders in the model using the given list of SingleCylinder objects"""
    dots = polygon_dots(cylinders)
    
    if create_new:
        model.java.component("comp1").geom("geom1").create("pol1", "Polygon")

    model.java.component("comp1").geom("geom1").feature("pol1").set("source", "table")
    for i in range(dots.shape[0]):
        model.java.component("comp1").geom("geom1").feature("pol1").setIndex("table", str(dots[i, 0])+"[nm]", i, 0)
        model.java.component("comp1").geom("geom1").feature("pol1").setIndex("table", str(dots[i, 1])+"[nm]", i, 1)
    
    model.java.component("comp1").geom("geom1").runPre("fin")
    model.java.component("comp1").geom("geom1").run("pol1")


def plot_shape(model: mph.Model) -> None:
    """Plots the shape of the geometry in the model"""
    polygon = model.java.component("comp1").geom("geom1").feature("pol1")
    table = polygon.getStringMatrix("table")

    dots = np.array([
        [
            float(re.sub(r"\[.*?\]", "", str(row[0]))),
            float(re.sub(r"\[.*?\]", "", str(row[1]))),
        ]
        for row in table
    ])

    dots_closed = np.vstack([dots, dots[0]])

    plt.figure(figsize=(5, 5))
    plt.plot(dots_closed[:, 0], dots_closed[:, 1], "-o")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("x, nm")
    plt.ylabel("y, nm")
    plt.show()
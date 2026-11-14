"""Assemble the Danish curriculum in CEFR progression order."""

from app.data.da.curriculum_a1 import A1_UNITS
from app.data.da.curriculum_a2 import A2_UNITS
from app.data.da.curriculum_b1 import B1_UNITS
from app.data.da.curriculum_b2 import B2_UNITS
from app.data.da.curriculum_c1 import C1_UNITS
from app.data.da.curriculum_c2 import C2_UNITS

CURRICULUM = {
    "A1": A1_UNITS,
    "A2": A2_UNITS,
    "B1": B1_UNITS,
    "B2": B2_UNITS,
    "C1": C1_UNITS,
    "C2": C2_UNITS,
}

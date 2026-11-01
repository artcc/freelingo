"""Polish phrasebook — assembler module."""

from app.data._types import PhrasebookCategory, PhrasebookEntry  # noqa: F401
from app.data.pl.phrasebook_a1 import A1_CATEGORIES
from app.data.pl.phrasebook_a2 import A2_CATEGORIES
from app.data.pl.phrasebook_b1 import B1_CATEGORIES
from app.data.pl.phrasebook_b2 import B2_CATEGORIES
from app.data.pl.phrasebook_c1 import C1_CATEGORIES
from app.data.pl.phrasebook_c2 import C2_CATEGORIES

PHRASEBOOK_CATEGORIES: list[PhrasebookCategory] = (
    A1_CATEGORIES
    + A2_CATEGORIES
    + B1_CATEGORIES
    + B2_CATEGORIES
    + C1_CATEGORIES
    + C2_CATEGORIES
)

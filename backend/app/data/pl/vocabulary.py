"""Polish vocabulary sets — assembler module."""

from app.data._types import VocabularyEntry, VocabularySet  # noqa: F401
from app.data.pl.vocabulary_a1 import A1_SETS
from app.data.pl.vocabulary_a2 import A2_SETS
from app.data.pl.vocabulary_b1 import B1_SETS
from app.data.pl.vocabulary_b2 import B2_SETS
from app.data.pl.vocabulary_c1 import C1_SETS
from app.data.pl.vocabulary_c2 import C2_SETS

VOCABULARY_SETS: list[VocabularySet] = A1_SETS + A2_SETS + B1_SETS + B2_SETS + C1_SETS + C2_SETS

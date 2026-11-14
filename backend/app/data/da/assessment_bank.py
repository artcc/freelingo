"""Assemble Danish placement questions in their authored option order."""

from app.data.da.assessment_a1 import A1_QUESTIONS
from app.data.da.assessment_a2 import A2_QUESTIONS
from app.data.da.assessment_b1 import B1_QUESTIONS
from app.data.da.assessment_b2 import B2_QUESTIONS
from app.data.da.assessment_c1 import C1_QUESTIONS
from app.data.da.assessment_c2 import C2_QUESTIONS

ASSESSMENT_BANK = [
    *A1_QUESTIONS,
    *A2_QUESTIONS,
    *B1_QUESTIONS,
    *B2_QUESTIONS,
    *C1_QUESTIONS,
    *C2_QUESTIONS,
]

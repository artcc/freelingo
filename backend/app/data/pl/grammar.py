"""Polish grammar topics — assembler module."""

from app.data._types import GrammarTopic
from app.data.pl.grammar_a1 import A1_GRAMMAR_TOPICS
from app.data.pl.grammar_a2 import A2_GRAMMAR_TOPICS
from app.data.pl.grammar_b1 import B1_GRAMMAR_TOPICS
from app.data.pl.grammar_b2 import B2_GRAMMAR_TOPICS
from app.data.pl.grammar_c1 import C1_GRAMMAR_TOPICS
from app.data.pl.grammar_c2 import C2_GRAMMAR_TOPICS

GRAMMAR_TOPICS: list[GrammarTopic] = (
    A1_GRAMMAR_TOPICS
    + A2_GRAMMAR_TOPICS
    + B1_GRAMMAR_TOPICS
    + B2_GRAMMAR_TOPICS
    + C1_GRAMMAR_TOPICS
    + C2_GRAMMAR_TOPICS
)

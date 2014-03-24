from maths.questions import markov_chain
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_MarkovChain():
    q1 = markov_chain.MarkovChainBinomial()
    question_tester(QuestionTree(part=q1))
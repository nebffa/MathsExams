from .. import relationships, matrix_linear_transformation
from .question_tester import question_tester


def test_matrix_linear_transformation():
    question = relationships.parse_structure(matrix_linear_transformation)
    question_tester(question)
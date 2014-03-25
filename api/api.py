from ..questions import relationships, prob_table_known
from ..latex import latex, questions



def question():
    """
    The first attempt at an API, so that our flask app can request questions.

    """



    tree = relationships.parse_structure(prob_table_known)


    return tree.show_question()


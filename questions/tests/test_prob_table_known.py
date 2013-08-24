from maths.questions import questions, prob_table_known


def test_Antiderivative():

    q = prob_table_known.ProbTableKnown()
    question = questions.new_question(1, q)

    q_a = prob_table_known.Property(part=q)
    q_b = prob_table_known.Multinomial(part=q)
    q_c = prob_table_known.Conditional(part=q)
    q_d = prob_table_known.Cumulative(part=q)

    questions.add_part(question, 1, part=q_a)
    questions.add_part(question, 2, part=q_b)
    questions.add_part(question, 3, part=q_c)
    questions.add_part(question, 4, part=q_d)

    questions.test_question_new(question)
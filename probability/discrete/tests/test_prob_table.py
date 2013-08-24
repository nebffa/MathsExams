from maths.probability.discrete import prob_table
import pytest
import itertools



def test_expectation_x():
    test_prob_table = {0: 0.1, 1: 0.3, 2: 0.2, 3: 0.1, 4: 0.3}

    assert prob_table.expectation_x(test_prob_table) == 0.3 + 0.4 + 0.3 + 1.2
    assert prob_table.expectation_x(test_prob_table, power=2) == 0.3*1**2 + 0.2*2**2 + 0.1*3**2 + 0.3*4**2


def test_mode():
    alt_prob_table = {0: 0.1, 1: 0.3, 2: 0.2, 3: 0.2, 4: 0.2}

    assert prob_table.mode(alt_prob_table) == 1


def test_prob_sum():
    test_prob_table = {0: 0.1, 1: 0.3, 2: 0.2, 3: 0.1, 4: 0.3}

    assert prob_table.prob_sum(test_prob_table, 5, 2) == 2*(0.3*0.3 + 0.2*0.1)
                                                            #024            123           222              114              033
    assert prob_table.prob_sum(test_prob_table, 6, 3) == 6*(0.1*0.2*0.3 + 0.3*0.2*0.1) + 0.2*0.2*0.2 + 3*(0.3*0.3*0.3+ 0.1*0.1*0.1)


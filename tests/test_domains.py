from .. import domains


def test_integer_domain():
    interval = domains.integer_domain()

    assert interval.left < interval.right
def int_to_nth(n):
    if not 1 <= n <= 10:
        raise ValueError('An n of value: {0} is not supported'.format(n))

    english = {
        1: 'first',
        2: 'second',
        3: 'third',
        4: 'fourth',
        5: 'fifth',
        6: 'sixth',
        7: 'seventh',
        8: 'eighth',
        9: 'ninth'
    }

    return english[n]
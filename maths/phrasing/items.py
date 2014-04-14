def list_numbers(items):
    """Return an English-readable listing of a set of numbers.
    """
    head = items[:-1]
    tail = items[-1]

    head_text = ', '.join([str(i) for i in head])
    return head_text + ' and ' + str(tail)

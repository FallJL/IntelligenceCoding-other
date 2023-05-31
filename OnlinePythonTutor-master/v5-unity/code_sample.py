def reverse(l):
    if not l:
        return []
    return [l[-1]] + reverse(l[:-1])


reverse([1, 2, 3])

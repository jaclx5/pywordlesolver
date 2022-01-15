def compute_response(solution, guess):
    """
    Given a solution and guess words, return a response in the "gyx" notation.

    For each position of the guess word, the i-th position of the response is a:
        - "g" - if the i-th letter of `guess` occurs in the i-th position `solution`.
        - "y" - if the i-th letter of `guess` occurs in `solution` but not in the i-th position.
        - "x" - if the i-th letter of `guess` does not occur in `solution`

    Example:
        >>> compute_response("VIDEO", "OLDEN")
        "yxggy"

    Parameters
    ----------
    solution : str
        the solution word.
    guess : str
        the guess word

    Returns
    -------
    string
        the coded response.
    """

    resp = ""

    for cw, cg in zip(solution, guess):
        if cw == cg:
            resp += "g"
        elif cg in solution:
            resp += "y"
        else:
            resp += "x"

    return resp
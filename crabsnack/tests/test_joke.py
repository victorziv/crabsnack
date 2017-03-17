from crabsnack import joke, jokem


def test_joke():
    assert isinstance(joke(), str)


def test_jokem():
    assert isinstance(jokem(), str)

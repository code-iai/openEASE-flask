from webrob.utility.path_exists_checker import exists as path_exists

EXISTING_PATH = '../utility'
NOT_EXISTING_PATH = '../nothing'


def test_path_exists():
    assert path_exists(EXISTING_PATH) is True


def test_path_does_not_exist():
    assert path_exists(NOT_EXISTING_PATH) is False

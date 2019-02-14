from webrob.test.utility.testbase_file_io import TEMP_DIR
from webrob.utility.directory_handler import rm_nonempty_dir, mk_dir
from webrob.utility.path_builder import join_paths
from webrob.utility.path_exists_checker import path_exists

EXISTING_PATH = TEMP_DIR
NOT_EXISTING_PATH = join_paths(TEMP_DIR, 'nothing')


# cannot use testbase_file_io.create_temp() as it uses functionality of this module
# instead use directory_handler and create and delete temp_dir manually
def setup_module():
    mk_dir(EXISTING_PATH)
    return


def teardown_module():
    rm_nonempty_dir(EXISTING_PATH)
    return


# -------------------------------TESTS---------------------------------


def test_path_exists():
    assert path_exists(EXISTING_PATH) is True


def test_path_does_not_exist():
    assert path_exists(NOT_EXISTING_PATH) is False

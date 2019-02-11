import os
import shutil
import pytest

from webrob.test.utility.testbase_file_io import TEMP_DIR_PATH
from webrob.utility.path_builder import join as join_paths
from webrob.utility.path_exists_checker import exists as path_exists
from webrob.utility.directory_handler import rm_nonempty_dir, make_dirs, rm_empty_dir, mk_dir

TEST_DIR = join_paths(TEMP_DIR_PATH, 'test')
TEST_DIR_NESTED = join_paths(TEST_DIR, 'test')


# both setup_module() and teardown_module() have to use the os-module
# instead of the directory_handler as it's being tested in this module
def setup_module():
    remove_directory_if_exists(TEMP_DIR_PATH)
    os.mkdir(TEMP_DIR_PATH)


def remove_directory_if_exists(path):
    if path_exists(path):
        shutil.rmtree(path)


def teardown_module():
    shutil.rmtree(TEMP_DIR_PATH)


# -------------------------------TESTS---------------------------------


def test_mk_dir():
    mk_dir(TEST_DIR)
    assert path_exists(TEST_DIR) is True


def test_make_dirs():
    make_dirs(TEST_DIR_NESTED)
    assert path_exists(TEST_DIR_NESTED) is True


def test_rm_empty_dir():
    assert_remove_function(TEST_DIR, rm_empty_dir)
    assert_remove_function(TEST_DIR, rm_nonempty_dir)


def assert_remove_function(path, remove_function, check_path = None):
    remove_directory_if_exists(path)
    make_dirs(path)

    if check_path is None:      # path created and to check are the same
        remove_function(path)
        assert path_exists(path) is False
    else:                       # path created and to check are different
        remove_function(check_path)
        assert path_exists(check_path) is False


def test_rm_nonempty_dir():
    with pytest.raises(OSError):
        assert_remove_function(TEST_DIR_NESTED, rm_empty_dir, TEST_DIR)
    assert_remove_function(TEST_DIR_NESTED, rm_nonempty_dir, TEST_DIR)

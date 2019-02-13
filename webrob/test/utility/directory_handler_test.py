import os
import shutil
import pytest

from webrob.test.utility.testbase_file_io import TEMP_DIR
from webrob.utility.path_builder import join as join_paths
from webrob.utility.path_exists_checker import exists as path_exists
from webrob.utility.directory_handler import rm_nonempty_dir, make_dirs, rm_empty_dir, mk_dir

TEST_DIR = join_paths(TEMP_DIR, 'test')
TEST_DIR_NESTED = join_paths(TEST_DIR, 'test')


# both setup_function() and teardown_function() have to use the os-module
# instead of the directory_handler as it's being tested in this module
def setup_function():
    os.mkdir(TEMP_DIR)


def remove_directory_if_exists(path):
    if path_exists(path):
        shutil.rmtree(path)


def teardown_function():
    remove_directory_if_exists(TEMP_DIR)


# -------------------------------TESTS---------------------------------


def test_making_simple_directory():
    assert_make_dir_function(TEST_DIR, mk_dir)
    assert_make_dir_function(TEST_DIR, make_dirs)


def assert_make_dir_function(path, make_dir_function):
    make_dir_function(path)
    assert path_exists(path) is True
    remove_directory_if_exists(path)


def test_making_nested_directory():
    with pytest.raises(OSError):
        assert_make_dir_function(TEST_DIR_NESTED, mk_dir)
    assert_make_dir_function(TEST_DIR_NESTED, make_dirs)


def test_make_existing_directory():
    os.mkdir(TEST_DIR)
    with pytest.raises(OSError):
        assert_make_dir_function(TEST_DIR, mk_dir)
    with pytest.raises(OSError):
        assert_make_dir_function(TEST_DIR, make_dirs)


def test_remove_empty_dir():
    assert_remove_function(TEST_DIR, rm_empty_dir)
    assert_remove_function(TEST_DIR, rm_nonempty_dir)


def assert_remove_function(path, remove_function, check_path = None):
    setup_for_remove_test(path)

    if check_path is None:      # path created and to check are the same
        execute_and_check_remove(path, remove_function)
    else:                       # path created and to check are different
        execute_and_check_remove(check_path, remove_function)


def setup_for_remove_test(path):
    # deleting the old directory (if it exists) and make a new one
    # not doing this might cause errors
    remove_directory_if_exists(path)
    make_dirs(path)


def execute_and_check_remove(path, remove_function):
    remove_function(path)
    assert path_exists(path) is False


def test_rm_nonempty_dir():
    with pytest.raises(OSError):
        assert_remove_function(TEST_DIR_NESTED, rm_empty_dir, TEST_DIR)
    assert_remove_function(TEST_DIR_NESTED, rm_nonempty_dir, TEST_DIR)

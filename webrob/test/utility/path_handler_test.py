import os

from webrob.test.utility.testbase_file_io import TEMP_DIR, EMPTY_TEMP_FILE, TEMP_FILE_WITH_CONTENT, \
    create_empty_temp_file, create_temp_file_with_content, remove_file
from webrob.utility.directory_handler import mk_dir, rm_nonempty_dir
from webrob.utility.path_handler import join_paths, path_exists, absolute_path, get_parent_dir_name, \
    get_path_basename, get_unix_style_path_basename, is_directory, get_path_size

EXISTING_PATH = TEMP_DIR
NOT_EXISTING_PATH = join_paths(TEMP_DIR, 'nothing')

BASENAME = 'base'
BASENAME_TEST_DIR = join_paths(EXISTING_PATH, BASENAME)
BASENAME_TEST_DIR_UNIX_STLYE = join_paths(BASENAME_TEST_DIR, '')


# cannot use testbase_file_io.create_temp() as it uses functionality of this module
# instead use directory_handler and create and delete temp_dir manually
def setup_module():
    if os.path.exists(EXISTING_PATH):  # for the case that due to debugging errors teardown wasn't executed
        rm_nonempty_dir(EXISTING_PATH)
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


def test_join_paths():
    path1 = 'first'
    path2 = 'second'
    path3 = 'third'

    join_paths_and_assert_correctness(path1)
    join_paths_and_assert_correctness(path1, path2)
    join_paths_and_assert_correctness(path1, path2, path3)


def join_paths_and_assert_correctness(*args):
    template_string = build_template_string(len(args))
    expected_result_path = template_string.format(*args)
    builder_result_path = join_paths(*args)
    # replace is needed so tests run on uniformly on all OS
    assert builder_result_path.replace(os.sep, '/') == expected_result_path


def build_template_string(number_of_placeholders):
    template = ''
    for x in xrange(number_of_placeholders):
        template += '{' + str(x) + '}'
        if x < number_of_placeholders - 1:
            template += '/'

    return template


# Figure out why this runs locally but not on Travis, https://github.com/code-iai/openEASE-flask/issues/2
# def test_absolute_path():
#    return absolute_path(TEMP_DIR) == os.path.abspath(TEMP_DIR)


def test_get_parent_dir_name():
    assert get_parent_dir_name(NOT_EXISTING_PATH) == TEMP_DIR


def test_get_path_basename():
    assert get_path_basename(BASENAME_TEST_DIR) == BASENAME
    assert get_path_basename(BASENAME_TEST_DIR_UNIX_STLYE) == ''


def test_get_unix_style_path_basename():
    # replace is needed so tests run on uniformly on all OS
    assert get_unix_style_path_basename(BASENAME_TEST_DIR.replace(os.sep, '/')) == BASENAME
    assert get_unix_style_path_basename(BASENAME_TEST_DIR_UNIX_STLYE.replace(os.sep, '/')) == ''


def test_is_directory():
    assert is_directory(NOT_EXISTING_PATH) is False
    create_empty_temp_file()
    assert is_directory(EMPTY_TEMP_FILE) is False
    assert is_directory(TEMP_DIR) is True
    remove_file(EMPTY_TEMP_FILE)


def test_get_size():
    create_temp_file_with_content()
    assert get_path_size(TEMP_FILE_WITH_CONTENT) == os.path.getsize(TEMP_FILE_WITH_CONTENT)
    remove_file(TEMP_FILE_WITH_CONTENT)

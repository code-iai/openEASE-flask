import pytest

from webrob.test.utility.testbase_file_io import delete_temp_dir, EMPTY_TEMP_FILE, TEMP_DIR, \
    create_temp_dir, create_empty_temp_file
from webrob.utility.dir_name_getter import get_parent_dir_name
from webrob.utility.file_handler import read_file, write_to_file
from webrob.utility.path_builder import join as join_paths
from webrob.utility.path_exists_checker import exists as path_exists
from webrob.utility.template_file_copyer import __copy_file_and_replace_keywords, __create_parent_dir, \
    copy_template_file, __get_number_of_template_fillers

BUILD_DESTINATION = join_paths(TEMP_DIR, 'copy.txt')
PARENT_DIR = get_parent_dir_name(BUILD_DESTINATION)
TEMPLATE_FILE = EMPTY_TEMP_FILE
TEMPLATE_CONTENT = '{0} and {1}'
KEYWORDS = ['apples', 'oranges']
TOO_FEW_KEYWORDS = list(KEYWORDS).pop(1)
TOO_MANY_KEYWORDS = list(KEYWORDS)
TOO_MANY_KEYWORDS.append('pears')      # for some reason cannot do list(...).append(object), returns None
EXPECTED_RESULT = '{0} and {1}'.format(KEYWORDS[0], KEYWORDS[1])


def setup_function():
    create_temp_dir()
    create_empty_temp_file()
    write_to_file(TEMPLATE_FILE, TEMPLATE_CONTENT)


def teardown_function():
    delete_temp_dir()


# -------------------------------TESTS---------------------------------


def test_copy_template_file():
    copy_template_file(TEMPLATE_FILE, BUILD_DESTINATION, KEYWORDS)
    assert path_exists(BUILD_DESTINATION) is True
    assert read_file(BUILD_DESTINATION) == EXPECTED_RESULT


def test_create_parent_dir():
    # run twice, to see if errors are thrown if parent directory already exists
    for x in xrange(2):
        __create_parent_dir(BUILD_DESTINATION)
        assert path_exists(PARENT_DIR) is True


def test_copy_file_and_replace_keywords():
    template = read_file(TEMPLATE_FILE)

    __copy_file_and_replace_keywords(BUILD_DESTINATION, template, KEYWORDS)

    assert path_exists(BUILD_DESTINATION) is True
    assert read_file(BUILD_DESTINATION) == EXPECTED_RESULT


def test_keyword_amount_does_not_match_template_fillers():
    template = read_file(TEMPLATE_FILE)

    with pytest.raises(IndexError):
        __copy_file_and_replace_keywords(BUILD_DESTINATION, template, TOO_FEW_KEYWORDS)
    with pytest.raises(IndexError):
        __copy_file_and_replace_keywords(BUILD_DESTINATION, template, TOO_MANY_KEYWORDS)


def test_get_number_of_template_fillers():
    assert __get_number_of_template_fillers('{}') == 0
    assert __get_number_of_template_fillers('{0}') == 1
    assert __get_number_of_template_fillers('{0} and {1}') == 2
    assert __get_number_of_template_fillers('{}{0} and {123}') == 2
    assert __get_number_of_template_fillers('{}{0} and }{ {123}') == 2

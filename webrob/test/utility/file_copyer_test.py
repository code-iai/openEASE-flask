import os
import pytest

from webrob.test.utility.testbase_file_io import delete_temp_dir, delete_temp_file_with_content, \
    TEMP_FILE_WITH_CONTENT_PATH, TEMP_DIR_PATH, create_temp_dir, create_temp_file_with_content
from webrob.utility.path_builder import join as join_paths
from webrob.utility.path_exists_checker import exists as path_exists
from webrob.utility.file_handler import read_file, write_to_file, remove_file
from webrob.utility.template_file_copyer import copy_file_and_replace_keywords

TEMPLATE_CONTENT = '{0} and {1}'
KEYWORDS = ['apples', 'oranges']
EXPECTED_RESULT = '{0} and {1}'.format(KEYWORDS[0], KEYWORDS[1])


def setup_module():
    create_temp_dir()


def teardown_module():
    delete_temp_dir()


def setup_function():
    create_temp_file_with_content()
    write_to_file(TEMP_FILE_WITH_CONTENT_PATH, TEMPLATE_CONTENT)


def teardown_function():
    try:                # need try-except because some unit-tests may remove the temp-file
        delete_temp_file_with_content()
    except OSError:
        return


# -------------------------------TESTS---------------------------------


def test_copy_template_file():
    return


def test_create_parent_dir():
    return


def test_copy_file_and_replace_keywords():
    dst = join_paths(TEMP_DIR_PATH, 'copy.txt')
    template = read_file(TEMP_FILE_WITH_CONTENT_PATH)

    copy_file_and_replace_keywords(dst, template, KEYWORDS)

    assert path_exists(dst) is True
    assert read_file(dst) == EXPECTED_RESULT

    remove_file(dst)

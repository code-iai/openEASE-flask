import os
import pytest

from webrob.test.utility.testbase_file_io import delete_temp_dir, TEMP_FILE_WITH_CONTENT_PATH, create_temp_dir, \
    TEMP_FILE_CONTENT, EMPTY_TEMP_FILE_PATH, NOT_EXISTING_FILE
from webrob.utility.path_exists_checker import exists as path_exists
from webrob.utility.file_handler import create_file, remove_file, read_file, write_to_file


def setup_module():
    create_temp_dir()


def teardown_module():
    delete_temp_dir()


# both setup_function() and teardown_function() have to use python
# file read/write-functions instead of the file_handler as it's
# being tested in this module
def setup_function():
    create_file(EMPTY_TEMP_FILE_PATH)


def create_file(path, content=None):
    dst_f = open(path, 'w+')
    if content is not None:
        dst_f.write(content)
    dst_f.close()


def teardown_function():
    try:                # need try-except because some unit-tests remove the temp-file
        os.remove(EMPTY_TEMP_FILE_PATH)
    except OSError:
        return


# -------------------------------TESTS---------------------------------


def test_read_existing_file():
    create_file(TEMP_FILE_WITH_CONTENT_PATH, TEMP_FILE_CONTENT)
    assert read_file(TEMP_FILE_WITH_CONTENT_PATH) == TEMP_FILE_CONTENT
    remove_file(TEMP_FILE_WITH_CONTENT_PATH)


def test_read_not_existing_file():
    with pytest.raises(IOError):
        read_file(NOT_EXISTING_FILE)


def test_write_to_existing_file():
    write_to_file(EMPTY_TEMP_FILE_PATH, TEMP_FILE_CONTENT)
    assert read_file(EMPTY_TEMP_FILE_PATH) == TEMP_FILE_CONTENT


def test_write_to_not_existing_file():
    with pytest.raises(IOError):
        write_to_file(NOT_EXISTING_FILE, TEMP_FILE_CONTENT)


def test_create_file():
    create_file(TEMP_FILE_WITH_CONTENT_PATH, TEMP_FILE_CONTENT)
    assert path_exists(TEMP_FILE_WITH_CONTENT_PATH) is True
    assert read_file(TEMP_FILE_WITH_CONTENT_PATH) == TEMP_FILE_CONTENT
    remove_file(TEMP_FILE_WITH_CONTENT_PATH)


def test_create_existing_file():
    with pytest.raises(IOError):
        create_file(EMPTY_TEMP_FILE_PATH, TEMP_FILE_CONTENT)


def test_remove_existing_file():
    remove_file(EMPTY_TEMP_FILE_PATH)
    assert path_exists(EMPTY_TEMP_FILE_PATH) is False


def test_remove_not_existing_file():
    with pytest.raises(OSError):
        remove_file(NOT_EXISTING_FILE)

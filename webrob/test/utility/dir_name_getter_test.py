from testbase_file_io import TEMP_DIR_PATH, TEMP_FILE_WITH_CONTENT_PATH
from webrob.utility.dir_name_getter import get_parent_dir_name

def test_get_parent_dir_name():
    assert get_parent_dir_name(TEMP_FILE_WITH_CONTENT_PATH) == TEMP_DIR_PATH

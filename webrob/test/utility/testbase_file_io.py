import webrob.utility.directory_handler as dir_handler
import webrob.utility.file_handler as file_handler

TEMP_DIR_PATH = ''
TEMP_FILE_PATH = ''


def setup_module():
    dir_handler.mk_dir(TEMP_DIR_PATH)


def teardown_module():
    dir_handler.rm_dir(TEMP_DIR_PATH)


def setup_function():
    file_handler.create_file(TEMP_FILE_PATH)


def teardown_function():
    file_handler.remove_file(TEMP_FILE_PATH)

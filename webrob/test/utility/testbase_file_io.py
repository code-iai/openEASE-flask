from webrob.utility.directory_handler import rm_nonempty_dir, mk_dir
from webrob.utility.file_handler import create_file, remove_file

TEMP_DIR_PATH = '../temp'
TEMP_FILE_WITH_CONTENT_PATH = '../temp/not-empty.txt'
TEMP_FILE_CONTENT = 'something'
EMPTY_TEMP_FILE_PATH = '../temp/empty.txt'
NOT_EXISTING_FILE = '../temp/nothing.txt'


def create_temp_dir():
    mk_dir(TEMP_DIR_PATH)


def delete_temp_dir():
    rm_nonempty_dir(TEMP_DIR_PATH)


def create_empty_temp_file():
    create_file(EMPTY_TEMP_FILE_PATH)


def delete_empty_temp_file():
    remove_file(EMPTY_TEMP_FILE_PATH)


def create_temp_file_with_content():
    create_file(TEMP_FILE_WITH_CONTENT_PATH, TEMP_FILE_CONTENT)


def delete_temp_file_with_content():
    remove_file(TEMP_FILE_WITH_CONTENT_PATH)

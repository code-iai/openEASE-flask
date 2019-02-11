import os

from webrob.utility.path_builder import join as join_paths


def test_join_paths():
    path1 = 'first'
    path2 = 'second'
    path3 = 'third'

    result_path1 = '{0}'.format(path1)
    result_path2 = '{0}/{1}'.format(path1, path2)
    result_path3 = '{0}/{1}/{2}'.format(path1, path2, path3)

    builder_result_path1 = join_paths(path1)
    builder_result_path2 = join_paths(path1, path2)
    builder_result_path3 = join_paths(path1, path2, path3)

    # replace is needed so tests run on uniformly on all OS
    assert builder_result_path1.replace(os.sep, '/') == result_path1
    assert builder_result_path2.replace(os.sep, '/') == result_path2
    assert builder_result_path3.replace(os.sep, '/') == result_path3

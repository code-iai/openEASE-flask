import os

from webrob.utility.path_builder import join as join_paths


def test_join_paths():
    path1 = 'first'
    path2 = 'second'
    path3 = 'third'

    join_paths_and_assert_correctness(path1)
    join_paths_and_assert_correctness(path1, path2)
    join_paths_and_assert_correctness(path1, path2, path3)


def join_paths_and_assert_correctness(*args):
    template_string = build_template_string(len(args))
    result_path = template_string.format(*args)
    builder_result_path = join_paths(*args)
    assert builder_result_path.replace(os.sep, '/') == result_path  # replace is needed so tests run on uniformly on all OS


def build_template_string(number_of_placeholders):
    template = ''
    for x in xrange(number_of_placeholders):
        template += '{{0}}/'.format(str(x))
    return template[0:len(template)-1]  # removes final slash

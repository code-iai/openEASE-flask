from webrob.startup.init_app import __password_criteria_fulfilled, __has_six_or_more_chars, \
    __contains_number, __contains_lowercase_letter, __contains_uppercase_letter

import pytest


# test for length > 6, containing a number, a lower- and a uppercase letter together
def test_password_criteria():
    assert __password_criteria_fulfilled('') is False
    assert __password_criteria_fulfilled('a') is False
    assert __password_criteria_fulfilled('A') is False
    assert __password_criteria_fulfilled('1') is False
    assert __password_criteria_fulfilled('aA') is False
    assert __password_criteria_fulfilled('a1') is False
    assert __password_criteria_fulfilled('1A') is False
    assert __password_criteria_fulfilled('Aa1') is False
    assert __password_criteria_fulfilled('AAAAAA') is False
    assert __password_criteria_fulfilled('aaaaaa') is False
    assert __password_criteria_fulfilled('111111') is False
    assert __password_criteria_fulfilled('aaa111') is False
    assert __password_criteria_fulfilled('AAA111') is False
    assert __password_criteria_fulfilled('AAAaaa') is False
    assert __password_criteria_fulfilled('AAaa11') is True


def test_has_six_or_more_character():
    assert __has_six_or_more_chars('') is False
    assert __has_six_or_more_chars('a') is False
    assert __has_six_or_more_chars('abcde') is False
    assert __has_six_or_more_chars('abcdef') is True
    assert __has_six_or_more_chars('abcdefgh') is True


def test_contains_number():
    assert __contains_number('') is False
    assert __contains_number('abc') is False
    assert __contains_number('1') is True
    assert __contains_number('abc1') is True


def test_contains_lowercase():
    assert __contains_lowercase_letter('') is False
    assert __contains_lowercase_letter('1') is False
    assert __contains_lowercase_letter('ABC') is False
    assert __contains_lowercase_letter('a') is True
    assert __contains_lowercase_letter('AbC') is True


def test_contains_uppercase():
    assert __contains_uppercase_letter('') is False
    assert __contains_uppercase_letter('1') is False
    assert __contains_uppercase_letter('abc') is False
    assert __contains_uppercase_letter('A') is True
    assert __contains_uppercase_letter('AbC') is True

from datetime import timedelta

from solidlab_perftest_common.util import (
    count_none,
    count_not_none,
    is_single_not_none,
    is_single_none,
    datetime_now,
    convert_dict_datetimes_to_rfc3339,
    dump_rfc3339,
)


def test_count_none_1():
    assert count_none(1, "s", ["a"], {"foo": "bar"}) == 0


def test_count_none_2():
    assert count_none(1, "s", None, 3, None) == 2


def test_count_none_3():
    assert count_none(None, "", [], {}, 0) == 1


def test_count_none_4():
    assert count_none(1) == 0


def test_count_none_5():
    assert count_none(0) == 0


def test_count_none_6():
    assert count_none(None) == 1


def test_count_none_7():
    assert count_none() == 0


def test_count_not_none_1():
    assert count_not_none(1, "s", ["a"], {"foo": "bar"}) == 4


def test_count_not_none_2():
    assert count_not_none(1, "s", None, 3, None) == 3


def test_count_not_none_3():
    assert count_not_none(None, "", [], {}, 0) == 4


def test_count_not_none_4():
    assert count_not_none(1) == 1


def test_count_not_none_5():
    assert count_not_none(0) == 1


def test_count_not_none_6():
    assert count_not_none(None) == 0


def test_count_not_none_7():
    assert count_not_none() == 0


def test_is_single_not_none_1():
    assert is_single_not_none(1, "s", ["a"], {"foo": "bar"}) is False


def test_is_single_not_none_1b():
    assert is_single_not_none(None, None, None, {"foo": "bar"}) is True


def test_is_single_not_none_2():
    assert is_single_not_none(1, "s", None, 3, None) is False


def test_is_single_not_none_2b():
    assert is_single_not_none(None, None, None, 3, None) is True


def test_is_single_not_none_3():
    assert is_single_not_none(None, "", [], {}, 0) is False


def test_is_single_not_none_3b():
    assert is_single_not_none("", None, None) is True


def test_is_single_not_none_4():
    assert is_single_not_none(1) is True


def test_is_single_not_none_5():
    assert is_single_not_none(0) is True


def test_is_single_not_none_6():
    assert is_single_not_none(None) is False


def test_is_single_not_none_7():
    assert is_single_not_none() is False


def test_is_single_none_1():
    assert is_single_none(1, "s", ["a"], {"foo": "bar"}) is False


def test_is_single_none_2():
    assert is_single_none(1, "s", None, 3, None) is False


def test_is_single_none_3():
    assert is_single_none(None, "", [], {}, 0) is True


def test_is_single_none_4():
    assert is_single_none(1) is False


def test_is_single_none_5():
    assert is_single_none(0) is False


def test_is_single_none_6():
    assert is_single_none(None) is True


def test_is_single_none_7():
    assert is_single_none() is False


def test_convert_dict_datetimes_to_rfc3339():
    test_date_1 = datetime_now() - timedelta(hours=10)
    test_date_2 = datetime_now() - timedelta(minutes=5)
    test_date_3 = datetime_now() - timedelta(seconds=2)

    test_input = {
        "num": 5,
        "str": "foo",
        "date": test_date_1,
        "list": [
            8,
            test_date_2,
            {"num": 55, "str": "foo5", "date": test_date_3},
            [8, test_date_3, {"num": 51, "str": "foo1", "date": test_date_1}],
        ],
        "dic": {
            "num4": 4,
            "str4": "bar",
            "date4": test_date_2,
            "list4": [
                4,
                test_date_1,
                {"num": 7, "str": "foo5", "date": test_date_2},
                [9, test_date_1, {"num": 0, "str": "bar0", "date": test_date_2}],
            ],
        },
    }
    expected = {
        "num": 5,
        "str": "foo",
        "date": dump_rfc3339(test_date_1),
        "list": [
            8,
            dump_rfc3339(test_date_2),
            {"num": 55, "str": "foo5", "date": dump_rfc3339(test_date_3)},
            [
                8,
                dump_rfc3339(test_date_3),
                {"num": 51, "str": "foo1", "date": dump_rfc3339(test_date_1)},
            ],
        ],
        "dic": {
            "num4": 4,
            "str4": "bar",
            "date4": dump_rfc3339(test_date_2),
            "list4": [
                4,
                dump_rfc3339(test_date_1),
                {"num": 7, "str": "foo5", "date": dump_rfc3339(test_date_2)},
                [
                    9,
                    dump_rfc3339(test_date_1),
                    {"num": 0, "str": "bar0", "date": dump_rfc3339(test_date_2)},
                ],
            ],
        },
    }
    actual = convert_dict_datetimes_to_rfc3339(test_input)
    assert actual == expected

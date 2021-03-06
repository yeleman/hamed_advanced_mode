#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import random
import datetime

import pytest

from hamed_advanced import (alphabet, aget, get, adeget, deget,
                            cipher, decipher,
                            get_doy, get_code,
                            get_adavanced_request_code,
                            decode_request_code,
                            get_acception_code,
                            validate_acceptation_code)


@pytest.fixture()
def cercle_id():
    return "33"


@pytest.fixture()
def date():
    return datetime.datetime(2017, 2, 1, 15, 22, 0)


@pytest.fixture()
def request_code():
    return "PIIGMFHFG"


@pytest.fixture()
def acceptation_code():
    return "FIHII"


def test_no_boundaries():
    assert aget(alphabet, 'a', 0) == 'a'
    assert aget(alphabet, 'a', 1) == 'b'

    letter = "a"
    pad = 1
    cil = aget(alphabet, letter, pad)
    assert adeget(alphabet, cil, pad) == letter

    pad = random.randint(0, 24)
    original = "b c d e f g h 5 6 7 8"
    assert decipher(cipher(original, pad), pad) == original


def test_boundaries():
    pad = random.randint(0, 36)
    original = "a b c d e f g h 5 6 7 8 9"
    assert decipher(cipher(original, pad), pad) == original


def test_alphabet():
    assert len(alphabet) == 36


def test_get():
    assert get(alphabet, 0, 0) == "a"


def test_aget():
    assert aget(alphabet, "a", 0) == "a"
    assert aget(alphabet, "z", 0) == "z"
    assert aget(alphabet, "a", 10) == "k"
    assert aget(alphabet, "z", 10) == "9"


def test_deget():
    assert deget(alphabet, "a", 0) == 0


def test_adeget():
    assert adeget(alphabet, "a", 0) == "a"
    assert adeget(alphabet, "z", 0) == "z"
    assert adeget(alphabet, "a", 10) == "0"
    assert adeget(alphabet, "z", 10) == "p"


def test_cipher():
    assert cipher("hello world", 5) == "mjqqt 1twqi"
    assert cipher("hello world", 20) == "1y558 g8b5x"


def test_decipher():
    assert decipher("bonjour", 4) == "7kjfkqn"


def test_cipher_decipher():
    for value in ("hello", "bonjour", "21", "hello monde"):
        pad = random.randint(0, len(alphabet))
        assert decipher(cipher(value, pad), pad) == value


def test_get_doy():
    assert get_doy(datetime.date(2017, 1, 1)) == "001"
    assert get_doy(datetime.date(1982, 11, 21)) == "325"


def test_get_code(cercle_id, date):
    assert get_code(date, cercle_id) == "33170201"


def test_get_adavanced_request_code(cercle_id, date, request_code):
    assert get_adavanced_request_code(cercle_id, date) == request_code


def test_decode_request_code(cercle_id, date, request_code):
    dcercle_id, ddate, dpad = decode_request_code(request_code)
    assert dcercle_id == cercle_id
    assert ddate == date.date()
    assert dpad == date.hour


def test_get_acception_code(request_code, acceptation_code):
    dacception_code = get_acception_code(request_code)
    assert dacception_code == acceptation_code


def test_validate_acceptation_code(request_code, acceptation_code):
    assert validate_acceptation_code(request_code, acceptation_code)
    assert not validate_acceptation_code(request_code + "A", acceptation_code)
    assert not validate_acceptation_code(request_code, acceptation_code + "A")


def test_full(cercle_id, date):
    request_code = get_adavanced_request_code(cercle_id, date)
    dcercle_id, ddate, dpad = decode_request_code(request_code)
    assert dcercle_id == cercle_id
    assert ddate == date.date()
    assert dpad == date.hour
    acceptation_code = get_acception_code(request_code)
    assert validate_acceptation_code(request_code, acceptation_code)

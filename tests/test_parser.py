import pytest
from email_header_analyzer.core.parser import EmailHeaderParser

def test_parser_initialization():
    assert EmailHeaderParser()

def test_parse_basic_headers():
    h = """From: a@b.com
Subject: Hi
Date: Mon, 1 Jan 2024 12:00:00 +0000"""
    res = EmailHeaderParser().parse_headers(h)
    assert res["From"] == "a@b.com"
    assert res["Subject"] == "Hi"

def test_empty():
    with pytest.raises(ValueError):
        EmailHeaderParser().parse_headers("")

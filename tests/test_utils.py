# tests/test_utils.py
import pytest
from app.vk_api import extract_id_from_link

def test_extract_id_from_link_with_id():
    assert extract_id_from_link("https://vk.com/id123")  == "123"

def test_extract_id_from_link_with_short_name():
    assert extract_id_from_link("https://vk.com/dima")  == "dima"

def test_extract_id_from_link_with_garbage():
    assert extract_id_from_link("randomstring") == "randomstring"

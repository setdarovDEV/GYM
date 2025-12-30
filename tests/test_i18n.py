import pytest
from src.infrastructure.i18n.loader import i18n_loader
from src.infrastructure.i18n.service import i18n_service


def test_loader_initialization():
    assert hasattr(i18n_loader, 'default_language')
    assert i18n_loader.default_language == 'ru'
    assert i18n_loader.has_language('ru')


def test_service_translation():
    text = i18n_service.get('welcome.message', 'ru')
    assert isinstance(text, str)
    assert text != 'welcome.message'

a = test_service_translation()
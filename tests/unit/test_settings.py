"""
Unit tests for Django settings configuration
"""
import pytest
from django.conf import settings


@pytest.mark.unit
class TestDjangoSettings:
    """Test Django settings configuration"""

    def test_debug_setting(self):
        """Test DEBUG setting exists"""
        assert hasattr(settings, 'DEBUG')

    def test_installed_apps(self):
        """Test required apps are installed"""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'AppClassificationOfLD',
        ]
        for app in required_apps:
            assert app in settings.INSTALLED_APPS

    def test_middleware_configuration(self):
        """Test middleware is properly configured"""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ]
        for middleware in required_middleware:
            assert middleware in settings.MIDDLEWARE

    def test_database_configuration(self):
        """Test database is configured"""
        assert hasattr(settings, 'DATABASES')
        assert 'default' in settings.DATABASES

    def test_templates_configuration(self):
        """Test templates are configured"""
        assert hasattr(settings, 'TEMPLATES')
        assert len(settings.TEMPLATES) > 0

    def test_static_url_configured(self):
        """Test static URL is configured"""
        assert hasattr(settings, 'STATIC_URL')

    def test_media_configuration(self):
        """Test media settings are configured"""
        assert hasattr(settings, 'MEDIA_URL')
        assert hasattr(settings, 'MEDIA_ROOT')

    def test_secret_key_exists(self):
        """Test SECRET_KEY is set"""
        assert hasattr(settings, 'SECRET_KEY')
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) > 0

    def test_allowed_hosts(self):
        """Test ALLOWED_HOSTS is configured"""
        assert hasattr(settings, 'ALLOWED_HOSTS')

    def test_root_urlconf(self):
        """Test ROOT_URLCONF is set"""
        assert hasattr(settings, 'ROOT_URLCONF')
        assert 'ClassificationOfLD.urls' in settings.ROOT_URLCONF

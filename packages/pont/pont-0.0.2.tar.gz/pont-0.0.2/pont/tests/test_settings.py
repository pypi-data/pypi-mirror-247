import os

import pytest

from pont.settings import Settings, SettingsError


@pytest.fixture
def empty_yaml_settings(tmp_path):
    pont_yaml_path = tmp_path / "pont.yml"
    return pont_yaml_path


@pytest.fixture
def minimal_yaml_settings():
    return """host: 192.168.1.1
port: 8888
proxies:
    - protocol: http
      remote_host: 127.0.0.1
      local_host: 127.0.0.1
      remote_port: 8889
      local_port: 8887
"""


@pytest.fixture
def yaml_path(empty_yaml_settings, minimal_yaml_settings):
    empty_yaml_settings.write_text(minimal_yaml_settings)
    return empty_yaml_settings


@pytest.fixture
def change_cwd(request, tmp_path):
    """
    Change the current working directory to the directory where the yaml file is
    going to be created
    """
    os.chdir(tmp_path)
    yield
    os.chdir(request.config.invocation_params.dir)


@pytest.fixture
def chang_cwd_to_test_dir(request):
    """
    Allow to make sure their is no pont.yml file in the current directory
    """
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_params.dir)


def test_no_config_file(chang_cwd_to_test_dir):
    settings = Settings()
    settings.load()
    assert settings.config_file is None


def test_load_user_directory(mocker, chang_cwd_to_test_dir, yaml_path, tmp_path):
    mocker.patch("platformdirs.user_config_dir", return_value=str(tmp_path))
    settings = Settings()
    settings.load()
    assert settings.config_file == yaml_path


def test_load_current_directory(change_cwd, yaml_path):
    settings = Settings()
    settings.load()
    assert settings.config_file == yaml_path


def test_load_settings(yaml_path):
    settings = Settings()
    settings.load_file(yaml_path)
    assert settings.config_file == yaml_path
    assert settings.host == "192.168.1.1"
    assert settings.port == 8888
    assert len(settings.proxies) == 1
    assert settings.proxies[0].protocol == "http"
    assert settings.proxies[0].remote_host == "127.0.0.1"
    assert settings.proxies[0].remote_port == 8889
    assert settings.proxies[0].local_host == "127.0.0.1"
    assert settings.proxies[0].local_port == 8887


def test_load_settings_no_file(empty_yaml_settings):
    settings = Settings()
    with pytest.raises(SettingsError):
        settings.load_file(empty_yaml_settings)


def test_load_settings_broken_file(empty_yaml_settings):
    empty_yaml_settings.write_text("broken: yaml")
    settings = Settings()
    with pytest.raises(SettingsError):
        settings.load_file(empty_yaml_settings)

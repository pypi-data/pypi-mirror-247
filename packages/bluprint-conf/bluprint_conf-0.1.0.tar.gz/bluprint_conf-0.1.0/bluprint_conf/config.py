"""Code for manipulating YAML configuration files."""

from pathlib import Path, PurePath
from typing import Any
from urllib.parse import urlparse

from importlib_resources import files
from omegaconf import DictConfig, ListConfig, OmegaConf


def load_config_yaml(
    config_file: str | Path = 'conf/config.yaml',
    use_package_path: bool = True,
) -> DictConfig | ListConfig:
    """Load project configuration yaml

    Parses relative paths and opens yaml configuration using OmegaConf.

    Args:
        config_file (str | Path, optional): Relative or absolute path to the
          yaml configuration. Defaults to 'conf/config.yaml'.
        use_package_path (bool, optional): If this is True, then relative paths
          are parsed with respect to the project root and not with respect to
          the path of the calling script. Defaults to True.

    Returns:
        DictConfig | ListConfig: Return value of OmegaConf.create().
    """
    if not Path(config_file).is_absolute() and use_package_path:
        config_file = absolute_package_path(config_file)
    return OmegaConf.load(config_file)


def load_data_yaml(
    config_file: str | Path = 'conf/data.yaml',
    data_dir: str = 'data',
) -> DictConfig | ListConfig:
    """Load data configuration yaml

    Load yaml configuration with file paths and parses file paths relative to
      the project root directory.

    Args:
        config_file (str | Path, optional): Relative or absolute path to the
          yaml configuration. Defaults to 'conf/data.yaml'.
        data_dir (str, optional): Directory with local data. Defaults to
          'data'.

    Returns:
        DictConfig | ListConfig: Return value of OmegaConf.create().
    """
    conf = load_config_yaml(config_file)
    data_path = str(absolute_package_path(data_dir))
    return add_prefix_to_nested_config(conf, prefix=data_path)


def absolute_package_path(path_to_file: str | Path) -> Path:
    dir_name = str(Path(path_to_file).parent)
    if dir_name == '.':
        return Path(files(path_to_file).joinpath('_').parent)
    dir_as_module = dir_name.strip('/').replace('/', '.')
    file_basename = Path(path_to_file).name
    return Path(files(dir_as_module).joinpath(file_basename))


def add_prefix_to_nested_config(
    conf: DictConfig | ListConfig,
    prefix: str,
) -> DictConfig | ListConfig:

    def recurse_or_add_suffix(conf_value: Any) -> Any:  # noqa: WPS430
        if isinstance(conf_value, DictConfig | ListConfig):
            return add_prefix_to_nested_config(conf_value, prefix)
        if _is_abs_path(conf_value) or _is_uri(conf_value):
            return conf_value
        return str(Path(prefix) / str(conf_value))

    if isinstance(conf, ListConfig):
        return OmegaConf.create([
            recurse_or_add_suffix(conf_value)
            for conf_value in conf
        ])
    elif isinstance(conf, DictConfig):
        return OmegaConf.create({
            conf_key: recurse_or_add_suffix(conf_values)
            for conf_key, conf_values in conf.items()
        })


def _is_abs_path(conf_value: Any) -> bool:
    return PurePath(str(conf_value)).is_absolute()


def _is_uri(conf_value: Any) -> bool:
    parsed_url = urlparse(str(conf_value))
    return all([parsed_url.scheme, parsed_url.netloc])

![logo](docs/source/images/bluprintconf_logo.png)

# Bluprint_conf

Bluprint_conf is a Python package for loading YAML configurations in your Python
code or Jupyter notebooks, that automatically resolves YAML file paths, so
there is no need to think about absolute or relative paths.

See [documentation](http://igor-sb.github.io/bluprint-conf) for usage.

## Installation

Bluprint_conf is automatically added and installed by Bluprint, but if you wish
to use it as a standalone package, it can be installed with:

```sh
pip install bluprint_conf
```

Bluprint_conf uses [OmegaConf](https://omegaconf.readthedocs.io/en/) to read and
parse YAML configuration files.

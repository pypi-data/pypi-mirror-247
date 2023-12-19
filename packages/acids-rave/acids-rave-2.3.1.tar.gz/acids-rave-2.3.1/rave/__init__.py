from pathlib import Path

import cached_conv as cc
import gin
import torch


BASE_PATH: Path = Path(__file__).parent

gin.add_config_file_search_path(BASE_PATH)
gin.add_config_file_search_path(BASE_PATH.joinpath('configs'))
gin.add_config_file_search_path(BASE_PATH.joinpath('configs', 'augmentations'))


def __safe_configurable(name):
    try: 
        setattr(cc, name, gin.get_configurable(f"cc.{name}"))
    except ValueError:
        setattr(cc, name, gin.external_configurable(getattr(cc, name), module="cc"))

# cc.get_padding = gin.external_configurable(cc.get_padding, module="cc")
# cc.Conv1d = gin.external_configurable(cc.Conv1d, module="cc")
# cc.ConvTranspose1d = gin.external_configurable(cc.ConvTranspose1d, module="cc")

__safe_configurable("get_padding")
__safe_configurable("Conv1d")
__safe_configurable("ConvTranspose1d")

from .blocks import *
from .discriminator import *
from .model import RAVE, BetaWarmupCallback
from .pqmf import *
from .balancer import *

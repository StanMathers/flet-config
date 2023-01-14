from typing import Type
from flet import Page
from .metaconfig import BaseConfig

def set_class_config(page: Type[Page], config: Type[BaseConfig]):
    config._set_page_attrs(page, config.__name__)



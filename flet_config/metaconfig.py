import pandas as pd
from typing import List, Any, Dict, Tuple


class Meta(type):

    _exclude_attrs: List[str] = ["__module__", "__qualname__"]
    _include_attrs: Dict[Dict[str, Any], Any] = {}

    _filename: str = "filename"
    _allowed_extensions: List[str] = ["json"]

    def __new__(cls, name: str, bases: Tuple[type], attrs: Dict[str, Any]) -> type:
        class_attributes = {i: attrs[i] for i in attrs if i not in cls._exclude_attrs}
        cls._include_attrs[name] = class_attributes

        return super().__new__(cls, name, bases, attrs)

    def __init__(self, name: str, bases: Tuple[type], attrs: Dict[str, Any]) -> None:
        self.name = name
        self.bases = bases
        self.attrs = attrs

        self._from_filename(self._include_attrs)
        setattr(
            self, "_set_page_attrs", self._set_page_attrs
        )  # Add _set_page_attrs method to every child class to be called from Page class

    def _set_page_attrs(self, obj: Any, config: str) -> None:
        """
        This function is set to all the child classes of BaseConfig class.\n
        This function sets all the attributes from `config` class to `obj` instance of any class. This case Page instance\n
        """
        for key, value in self._include_attrs[config].items():
            if key not in self._exclude_attrs:
                setattr(obj, key, value)

    def _from_filename(self, include_attrs: Any) -> str:
        """
        This function is used to locate a file config attribute. e.g. filename, config_file, etc.\n
        Which is defined in initial _filename attribute.\n
        
        Note: Only Json is supported at this point as a test case
        """

        for key, value in include_attrs.items():
            if self._filename in value:
                df = pd.read_json(value[self._filename]) # Only Json is supported at this point as a test case
                data = df.to_dict(orient="records")
                
                self._include_attrs[self.name] = data[0]
    
    


class BaseConfig(metaclass=Meta):
    pass

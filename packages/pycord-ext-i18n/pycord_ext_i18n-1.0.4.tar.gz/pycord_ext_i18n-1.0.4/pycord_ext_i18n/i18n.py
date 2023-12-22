import json

from discord import ContextMenuCommand, SlashCommand, utils

from pathlib import Path
from typing import Dict, TypedDict, TypeVar, Union, Callable

from .errors import PathNoexists
from .utils import as_valid_locale
from .enums import Locale


class OptionLocalization(TypedDict, total=False):
    name: str
    description: str


class CommandLocalization(OptionLocalization, total=False):
    options: Dict[str, OptionLocalization]


class Internationalization(TypedDict, total=False):
    strings: Dict[str, str]
    commands: Dict[str, CommandLocalization]

Localizable = Union[SlashCommand, ContextMenuCommand]
CommandT = TypeVar("CommandT", bound=Localizable)

class I18n:
    
    instance: "I18n"
    
    def __init__(self, path: str = './locale' ,**internalizations: Internationalization):
        self.path = path
        self._dict = {}
        self._paths = set()
        self.localizations: Dict[Locale, Dict[str, CommandLocalization]] = {  # type: ignore
            k.replace("_", "-"): commands
            for k, v in internalizations.items()
            if (commands := v)
        }
        
        I18n.instance = self

    def load(self):
        self._dict = {}
        self._paths = set()
        path = Path(self.path)
        
        if path.is_file():
            self._load_file(path)
        elif path.is_dir():
            for file in path.glob("*.json"):
                if not file.is_file():
                    continue
                self._load_file(file)
        else:
            raise PathNoexists("Path does not exist or is not a directory/file. Did you enter it correctly?")
        
        self._paths.add(path)
    
    def _load_file(self, path: Path) -> None:
        try:
            if path.suffix != ".json":
                raise ValueError("not a .json file")
            locale = path.stem

            if not (api_locale := as_valid_locale(locale)):
                raise ValueError(f"invalid locale '{locale}'")
            locale = api_locale

            data: dict = json.loads(path.read_text("utf-8"))

            for k, v in data.items():
                parts = k.split(".")
                command = parts[1]
                if self.localizations.get(locale) is None:
                    self.localizations[locale] = {command: {}}
                parameter = parts[2]
                self.localizations[locale][command].update({parameter: v})

        except Exception as e:
            raise RuntimeError(f"Unable to load '{path}': {e}") from e
    
    def _localize_command(
        self,
        locale: str | Locale,
        localizations: CommandLocalization  
    ) -> None:
        name_localizations = {}
        description_localizations = {}
        if name := localizations.get('name'):
            if name_localizations is None:
                name_localizations = {locale: name}
            else:
                name_localizations[locale] = name
        if description := localizations.get("description"):
            if description_localizations is None:
                description_localizations = {locale: description}
            else:
                description_localizations[locale] = description

        return name_localizations, description_localizations
    
    def localize_slash_command(self, **kwargs) -> CommandT:
        self.load()
        """A decorator to apply name and description localizations to a command."""
        return self._localize_commands(**kwargs)
    
    def _localize_commands(self, **attrs):
        def decorator(func: Callable) -> SlashCommand:
            name_localizations = {}
            for locale, localized in self.localizations.items():
                if localizations := localized.get(func.__name__):
                    name_localizations, description_localizations = self._localize_command(
                        locale,
                        localizations,
                    )
            return SlashCommand(func, name_localizations=name_localizations, description_localizations=description_localizations, **attrs)
        
        return decorator
        
    
    def get(self, key: str):
        """Returns localizations for the specified key.

        Parameters
        ----------
        key: :class:`str`
            The lookup key.

        Returns
        -------
        Optional[Dict[:class:`str`, :class:`str`]]
            The localizations for the provided key.
            Returns ``None`` if no localizations could be found and :attr:`strict` is disabled.
        """
        data = self._dict.get(key)
        if data is None:
            return None
        return data 
        
    def get_text(self, key: str, locale: str, default = None):
        """
        Gets a text from i18n files by key
        :param key: The key of the text
        :param locale: The locale of the text
        :param default: The default value to return if the text is not found
        :return: The text
        """ 
        return self.get(key).get(locale, default) 
    
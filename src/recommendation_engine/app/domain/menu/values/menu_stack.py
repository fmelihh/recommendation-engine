from dataclasses import dataclass
from .menu import MenuValue


@dataclass(frozen=True)
class MenuStack:
    _menu_list = []

    def retrieve_menu_list(self) -> list[MenuValue]:
        return self._menu_list

    def add_menu(self, menu_value: MenuValue):
        self._menu_list.append(menu_value)

    def __len__(self) -> int:
        return len(self._menu_list)

    def clean_menu_list(self):
        self._menu_list.clear()

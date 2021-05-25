# Copyright (C) 2021 BlueDrink9
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

from autokey.model.helpers import JSON_FILE_PATTERN, get_safe_path
from autokey.model.abstract_abbreviation import AbstractAbbreviation
from autokey.model.abstract_window_filter import AbstractWindowFilter
from autokey.model.abstract_hotkey import AbstractHotkey

def get_json_path(itempath):
    path_without_extension = os.path.splitext(itempath)[0]
    directory, base_name = os.path.split(path_without_extension)
    return JSON_FILE_PATTERN.format(directory, base_name)

def build_path(item, extension, base_name=None):
    if base_name is None:
        base_name = item.description
    else:
        base_name = os.path.splitext(base_name)[0]
    item.path = get_safe_path(item.parent.path, base_name, extension)

def get_serializable_scriptphrase(item):
    d = get_serializable_base(item)
    d2 = {
        "description": item.description,
        "prompt": item.prompt,
        "omitTrigger": item.omitTrigger,
        }
    return d


def get_serializable_base(item):
    d = {
        "modes": [mode.value for mode in item.modes],  # Store the enum value for compatibility with old user data.
        "usageCount": item.usageCount,
        "showInTrayMenu": item.show_in_tray_menu,
        "abbreviation": AbstractAbbreviation.get_serializable(item),
        "hotkey": AbstractHotkey.get_serializable(item),
        "filter": AbstractWindowFilter.get_serializable(item),
        }
    return d

def load(item, parent):
    item.parent = parent

    with open(item.path, "r") as in_file:
        text = in_file.read()
        # Set both code and phrase to allow this function to service both script and phrase.
        # More elegant than passing in the type, but probably not the cleanest.
        item.code = text
        item.phrase = text

    if os.path.exists(item.get_json_path()):
        item.load_from_serialized()
    else:
        base_name = os.path.basename(item.path)
        item.description = os.path.splitext(base_name)[0]

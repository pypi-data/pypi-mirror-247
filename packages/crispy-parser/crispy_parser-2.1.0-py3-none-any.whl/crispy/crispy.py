#
#   This file is part of the crispy-parser library.
#   Copyright (C) 2023  Ferit Yiğit BALABAN
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#   
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#   
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#   USA.


from typing import List, Dict, Type, Union, Tuple

from crispy.duplicate_name_exception import DuplicateNameException
from crispy.missing_value_exception import MissingValueException
from crispy.no_arguments_exception import NoArgumentsException
from crispy.parsing_exception import ParsingException
from crispy.unexpected_argument_exception import UnexpectedArgumentException
from crispy.too_many_subcommands_exception import TooManySubcommandsException


class Crispy:
    def __init__(self, accept_shortform=True, accept_longform=True):
        """
        Initializes a Crispy class with the default rules of accepting both short and long form of arguments.
        :param accept_shortform: Sets whether to allow short form of arguments (e.g., -a, -e, -A, -E)
        :param accept_longform: Sets whether to allow long form of arguments (e.g., --argument, --example)
        """
        self.accepted_keys: Dict[str, str] = {}
        self.variables: Dict[str, Type[Union[str, bool, int, float]]] = {}
        self.lookup: Dict[int, str] = {}
        self.subcommands: Dict[str, str] = {}

        if not (accept_shortform or accept_longform):
            raise ValueError("crispy: At least one form must be accepted!")
        self.accept_shortform = accept_shortform
        self.accept_longform = accept_longform

    def add_positional(self, name: str, var_type: Type[Union[str, bool, int, float]], position: int):
        """
        Adds a positional argument to the parser.
        
        :param name: Name of the positional argument
        :param var_type: Type of the positional argument
        :param position: Position of the positional argument
        :return: None
        """
        if name in self.variables:
            raise DuplicateNameException(f"crispy: variable with name '{name}' is present! Choose something else.")
        if position < 0 or position in self.lookup:
            raise ValueError(f"crispy: invalid position '{position}'!")
        self.variables[name] = var_type
        self.lookup[position] = name

    def add_subcommand(self, name: str, description: str):
        """Adds a subcommand to the parser.

        :param name: Name of the subcommand
        :param description: Description of the subcommand
        :return: None
        """
        if name in self.subcommands:
            raise DuplicateNameException(f"crispy: subcommand with name '{name}' is present! Choose something else.")
        self.subcommands[name] = description

    def add_variable(self, name: str, var_type: Type[Union[str, bool, int, float]]):
        """
        Adds a variable to the parser.
        :param name: Name of the variable
        :param var_type: Type of the variable
        :return: None
        """
        if name in self.variables:
            raise DuplicateNameException(f"crispy: variable with name '{name}' is present! Choose something else.")
        if self.accept_shortform:
            short_lower = f"-{name[0].lower()}"
            short_upper = f"-{name[0].upper()}"
            if short_lower not in self.accepted_keys:
                self.variables[name] = var_type
                self.accepted_keys[short_lower] = name
            elif short_upper not in self.accepted_keys:
                self.variables[name] = var_type
                self.accepted_keys[short_upper] = name
            else:
                raise ValueError(f"crispy: cannot add variable due to unavailable shortform!'-{short_lower}' "
                                 f"and '-{short_upper}' is reserved for other variables.")
        if self.accept_longform:
            self.variables[name] = var_type
            self.accepted_keys[f"--{name}"] = name

    def show_keys(self) -> str:
        """
        Creates a string showing and listing accepted forms of arguments
        :return: Returns the string of the assembled message
        """
        keys: List[str] = list(self.accepted_keys.keys())
        twice = self.accept_shortform and self.accept_longform
        i = 0
        text = ""
        move = 2 if twice else 1

        while i < len(keys):
            name = self.accepted_keys[keys[i]]
            text += f"{keys[i]}, {keys[i + 1]}: {name}\n" if twice else f"{keys[i]}: {name}\n"
            i += move
        return text

    def parse_arguments(self, args: List[str]) -> Tuple[str, Dict[str, Union[str, bool, int, float]]]:
        """
        Parses a list of arguments to a dictionary of variables and values.
        :param args: List of the arguments, containing each token as a list element
        :return: Returns the dictionary object of parsed variable with the value
        """
        if not args:
            raise NoArgumentsException("crispy: no argument was given!")

        subcommand: str = ""
        keys: Dict[str, Union[str, bool, int, float]] = {}
        i, j, len_args = 0, 0, len(args)
        while i < len_args:
            key = args[i]

            if key.strip() == "":
                i += 1
                continue

            if not key.startswith("-"):
                if key in self.subcommands:
                    if subcommand != "":
                        raise TooManySubcommandsException(f"crispy: too many subcommands! '{key}' is unexpected!")
                    subcommand = key
                else:
                    name = self.lookup[j]
                    expected_type, found_type = self.variables[name], self.deduce_type(key)
                    if expected_type != found_type:
                        raise ParsingException(f"crispy: type mismatch! '{key}' is not of type '{expected_type}'", expected_type, j, found_type)
                    
                    keys[name] = self.try_parse(key, expected_type)
                    j += 1
                i += 1
                continue
                
            elif "=" not in key:
                if key not in self.accepted_keys:
                    raise UnexpectedArgumentException(f"crispy: unexpected argument: '{key}'")
                if ((i + 1 < len_args) and 
                    (args[i + 1] not in self.accepted_keys) and 
                    ("=" not in args[i + 1]) and
                    (self.variables[self.accepted_keys[key]] != bool)):
                    value = args[i + 1]
                    i += 2
                else:
                    expected_type = self.variables[self.accepted_keys[key]]
                    if expected_type == bool:
                        value = "True"
                        i += 1
                    else:
                        raise MissingValueException(f"crispy: missing value for variable '{self.accepted_keys[key]}'!")
            else:
                key, value = key.split("=", 1)
                i += 1

            accepted_key = self.accepted_keys.get(key)
            if accepted_key:
                keys[accepted_key] = self.try_parse(value, self.variables[accepted_key])

        for key, value in self.variables.items():
            if value == bool and key not in keys:
                keys[key] = False

        return (subcommand, keys)

    def parse_string(self, string: str, seperator=" ") -> Tuple[str, Dict[str, Union[str, bool, int, float]]]:
        """
        Splits a string into a list of tokens, and parses the token list.
        :param string: String of the text to be parsed
        :param seperator: Seperator character to tokenize the input string
        :return: Returns the dictionary of parsed variables and values
        """
        string = string.strip()
        tokens = string.split(seperator)
        return self.parse_arguments(tokens)

    @staticmethod
    def try_parse(value: str, expected_type: type) -> Union[str, bool, int, float]:
        """
        Trys to convert a value in a string object to the target type.
        :param value: Value in string type
        :param expected_type: Target type
        :return: Returns the value in target type
        """
        if expected_type == bool:
            if value.lower() == "true":
                return True
            if value.lower() == "false":
                return False
        if expected_type == int:
            return int(value)
        if expected_type == float:
            return float(value)
        return value

    @staticmethod
    def deduce_type(value: str):
        """
        Deduces the type of the value.
        :param value: Value in string type
        :return: Returns the deduced type of value in string representation
        """
        if value.lower() == "true" or value.lower() == "false":
            return bool
        if value.isdigit():
            return int
        if value.replace(".", "", 1).isdigit():
            return float
        return str

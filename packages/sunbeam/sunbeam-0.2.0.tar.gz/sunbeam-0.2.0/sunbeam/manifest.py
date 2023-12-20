from typing import TypedDict, NotRequired, Literal

class TextInput(TypedDict):
    default: NotRequired[str]
    placeholder: NotRequired[str]

class TextAreaInput(TypedDict):
    default: NotRequired[str]
    placeholder: NotRequired[str]

class CheckboxInput(TypedDict):
    default: NotRequired[bool]

class PasswordInput(TypedDict):
    placeholder: NotRequired[str]

class NumberInput(TypedDict):
    default: NotRequired[int]
    placeholder: NotRequired[str]

class Input(TypedDict):
    label: str
    type: str
    name: str
    optional: NotRequired[bool]
    text: NotRequired[TextInput]
    textarea: NotRequired[TextAreaInput]
    checkbox: NotRequired[CheckboxInput]
    password: NotRequired[PasswordInput]
    number: NotRequired[NumberInput]

CommandMode = Literal["silent", "tty", "filter", "search", "detail"]

class Command:
    name: str
    title: str
    params: list[Input]

class Manifest(TypedDict):
    title: str
    description: str
    preferences: NotRequired[list[Input]]


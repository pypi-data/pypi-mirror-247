import json
import re
from dataclasses import fields, is_dataclass
from typing import Any, Dict, Iterable, List, Set


def is_key_set(obj: Any, property: str) -> bool:
    return property in obj and obj[property] is not None


def flatten_list(xs: Iterable[Iterable[Any]]) -> List[Any]:
    return [item for sublist in xs for item in sublist]


def get_required_parameters(input: Any) -> Set[str]:
    if is_dataclass(input):
        result = set()
        for field in fields(input):
            for param in get_required_parameters(getattr(input, field.name)):
                result.add(param)
        return result

    if isinstance(input, list):
        required_parameters_list = map(get_required_parameters, input)
        return set(flatten_list(required_parameters_list))
    elif isinstance(input, dict):
        return set(flatten_list([get_required_parameters(v) for v in input.values()]))
    elif isinstance(input, str):
        result = set(re.findall(r"{{(.*?)}}", input))
        return result
    else:
        return set()


def get_ancestors_for_instance_path(instance_path: str) -> List[str]:
    # a/b:123/c:456 -> [a, a/b:123]. Does not include the instance path itself.
    parts = instance_path.split("/")
    ancestors = []
    for i in range(len(parts) - 1):
        ancestors.append("/".join(parts[: i + 1]))
    return ancestors


def convert_parameterized_path_to_structural_path(parameterized_path: str) -> str:
    # Use a regular expression to replace :{{user}} with an empty string
    structural_path = re.sub(r":{{\w+}}", "", parameterized_path)
    return structural_path


def convert_instance_path_to_structural_path(instance_path: str) -> str:
    # Replace liability/user:123/friend:abc with liability/user/friend
    structural_path = re.sub(r":\w+", "", instance_path)
    return structural_path


def get_instance_value_by_path(parameterized_path: str) -> Dict[str, str | None]:
    # Converts a/b:123/c:456 to {a: None, a/b: 123, a/b:123/c: 456}
    parts = parameterized_path.split("/")
    for part in parts:
        if part.count(":") > 1:
            raise Exception(f"Invalid instance path: {parameterized_path}")

    instanceValueByPath = {}
    for i in range(len(parts)):
        path = "/".join(parts[: i + 1])
        kv = parts[i].split(":")
        if len(kv) == 1:
            value = None
        else:
            value = kv[1]
        instanceValueByPath[path] = value

    return instanceValueByPath


def fill_params_in_str(input: str, params: Dict[str, str]) -> str:
    for key, value in params.items():
        input = input.replace(f"{{{{{key}}}}}", value)

    return input


# TODO: Figure out a way to use generics instead of Any here.
def fill_object_params(input: Any, params: Dict[str, str]) -> Any:
    if is_dataclass(input):
        newObject = {}
        for field in fields(input):
            newObject[field.name] = fill_object_params(
                getattr(input, field.name), params
            )
        return input.__class__(**newObject)
    elif isinstance(input, dict):
        newObject = {}
        for key, value in input.items():
            newObject[key] = fill_object_params(value, params)
        return newObject
    elif isinstance(input, list):
        for i in range(len(input)):
            input[i] = fill_object_params(input[i], params)
        return input
    elif isinstance(input, str):
        return fill_params_in_str(input, params)
    else:
        return input


def read_file_as_json(filePath: str) -> Any:
    with open(filePath) as f:
        data = json.load(f)
        return data

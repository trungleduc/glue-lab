import json
from inspect import getfullargspec
from typing import List, Dict
from glue.main import load_plugins
from glue.config import link_function, link_helper

load_plugins()


def get_function_info(function_or_helper):
    item_info: Dict[str, Dict] = {}
    attributes = ["description", "labels1", "labels2", "display"]

    item = function_or_helper[0]

    if hasattr(function_or_helper, "function"):
        try:
            item_info["description"] = function_or_helper.info
            item_info["labels1"] = getfullargspec(item)[0]
            item_info["labels2"] = function_or_helper.output_labels
            item_info["display"] = function_or_helper.function.__name__
        except Exception as e:
            print(f"The link function {function_or_helper} is not loaded\n{e.args}")
    else:
        for attr in attributes:
            item_info[attr] = getattr(item, attr, "")

    item_info["function"] = item.__name__
    if not item_info["display"]:
        item_info["display"] = item.__name__

    return item_info


def get_advanced_links():
    advanced_links: Dict[str, List] = {}

    for function in link_function.members:
        if len(function.output_labels) == 1:
            if function.category not in advanced_links:
                advanced_links[function.category]: List[Dict] = []
            advanced_info = get_function_info(function)
            advanced_links[function.category].append(advanced_info)

    for helper in link_helper.members:
        if helper.category not in advanced_links:
            advanced_links[helper.category]: List[Dict] = []
        advanced_info = get_function_info(helper)
        try:
            json.dumps(advanced_info)
            advanced_links[helper.category].append(advanced_info)
        except TypeError:
            advanced_links[helper.category].append(
                {
                    "display": str(advanced_info["display"]),
                    "description": "This link is not available",
                }
            )

    # Reordering the dict
    categories = ["General"] + sorted(set(advanced_links.keys()) - set(["General"]))
    advanced_links = {k: advanced_links[k] for k in categories}
    return advanced_links
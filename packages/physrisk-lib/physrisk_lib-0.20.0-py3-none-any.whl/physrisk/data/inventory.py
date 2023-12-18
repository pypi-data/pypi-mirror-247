# flake8: noqa: E501
import hashlib
import importlib.resources
import json
import logging
from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, List, Tuple

from pydantic import TypeAdapter, parse_obj_as

import physrisk.data.colormap_provider as colormap_provider
import physrisk.data.static.hazard
from physrisk.data.inventory_reader import HazardModels

from ..api.v1.hazard_data import HazardResource, Period

# from physrisk.kernel.hazards import ChronicHeat


class Inventory:
    def __init__(self, hazard_resources: Iterable[HazardResource]):
        """Store the hazard resources with look up via:
        - key: combination of path and model identifier which is unique, or
        - type and model identifier: (requires choice of provider/version)

        Args:
            hazard_resources (Iterable[HazardResource]): list of resources
        """
        self.resources: Dict[str, HazardResource] = {}
        self.resources_by_type_id: DefaultDict[Tuple[str, str], List[HazardResource]] = defaultdict(list)
        for resource in hazard_resources:
            self.resources[resource.key()] = resource
            self.resources_by_type_id[(resource.hazard_type, resource.indicator_id)].append(resource)

    def json_ordered(self):
        sorted_resources = sorted(self.resources_by_type_id.items())
        resource_list = []
        for _, resources in sorted_resources:
            resource_list.extend(resources)
        models = HazardModels(resources=resource_list)
        return json.dumps(models.dict(), indent=4)


class EmbeddedInventory(Inventory):
    """Load up inventory embedded in file src/physrisk/data/static/hazard/inventory.json.
    This file is automatically generated by the hazard repo. In general the inventory of
    hazard resources used by physrisk is a combination of embedded and non-embedded inventories

    """

    def __init__(self):
        with importlib.resources.open_text(physrisk.data.static.hazard, "inventory.json") as f:
            models = TypeAdapter(HazardModels).validate_python(json.load(f)).resources
            expanded_models = expand(models)
            super().__init__(expanded_models)

    def colormaps(self):
        """Color maps. Key can be identical to a model identifier or more descriptive (if shared by many models)."""
        return colormap_provider.colormaps


def alphanumeric(text):
    """Return alphanumeric hash from supplied string."""
    hash_int = int.from_bytes(hashlib.sha1(text.encode("utf-8")).digest(), "big")
    return base36encode(hash_int)


def base36encode(number, alphabet="0123456789abcdefghijklmnopqrstuvwxyz"):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        raise TypeError("number must be an integer")

    base36 = ""

    if number < 0:
        raise TypeError("number must be positive")

    if 0 <= number < len(alphabet):
        return alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return base36


def expand(resources: List[HazardResource]) -> List[HazardResource]:
    expanded_models = [e for model in resources for e in model.expand()]
    # we populate map_id hashes programmatically
    for model in expanded_models:
        if model.map and model.map.source == "mapbox" and model.map.path:
            for scenario in model.scenarios:
                test_periods = scenario.periods
                scenario.periods = []
                for year in scenario.years:
                    name_format = model.map.path
                    path = name_format.format(scenario=scenario.id, year=year, return_period=1000)
                    id = alphanumeric(path)[0:6]
                    scenario.periods.append(Period(year=year, map_id=id))
                # if a period was specified explicitly, we check that hash is the same: a build-in check
                if test_periods is not None:
                    for period, test_period in zip(scenario.periods, test_periods):
                        if period.map_id != test_period.map_id:
                            raise Exception(
                                f"validation error: hash {period.map_id} different to specified hash {test_period.map_id}"  # noqa: E501
                            )
    return expanded_models

from typing import Any, Dict

import pytest

from src.quantcerebro.nodeset import NodeSetConfig
from src.quantcerebro.utils import load_yaml


class TestNodeSetConfig:

    @pytest.fixture(autouse=True)
    def setup(self):
        # self.scenario_a_b_dict: Dict[str, Any]= load_yaml("/Users/zeyutian/Documents/GitHub/quantcerebro/tests/resources/scenario_a_b.yml")
        ...

    def test_from_file(self):
        ...
import os
from enum import Enum
from platform import python_version

from bbconf import __version__ as bbconf_v

from ._version import __version__ as SERVER_VERSION

PKG_NAME = "bedhost"
LOG_FORMAT = "%(levelname)s in %(funcName)s: %(message)s"

# for now bedstat version is hard coded
ALL_VERSIONS = {
    "bedhost_version": SERVER_VERSION,
    "bbconf_version": bbconf_v,
    "python_version": python_version(),
}
TEMPLATES_DIRNAME = "templates"
TEMPLATES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIRNAME
)
STATIC_DIRNAME = "../docs"
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), STATIC_DIRNAME)

UI_PATH = os.path.join(os.path.dirname(__file__), "static", "bedhost-ui")

BEDFILE_API_ENDPOINT = "bedfile"
BEDSET_API_ENDPOINT = "bedset"
TYPES_MAPPING = {"integer": "integer", "number": "double", "string": "string"}
VALIDATIONS_MAPPING = {
    "integer": {"min": 0, "step": 1},
    "number": {"min": 0, "step": 0.01},
    "string": None,
}
NUMERIC_OPERATORS = [
    "equal",
    "not_equal",
    "greater",
    "greater_or_equal",
    "between",
    "less",
    "less_or_equal",
    "is_null",
    "is_not_null",
]
TEXT_OPERATORS = ["equal", "not_equal", "in", "not_in", "is_null", "is_not_null"]
OPERATORS_MAPPING = {
    "string": TEXT_OPERATORS,
    "number": NUMERIC_OPERATORS,
    "integer": NUMERIC_OPERATORS,
}
INIT_POSTGRES_CONDITION = "gc_content>0.5"
INIT_QUERYBUILDER = {
    "condition": "AND",
    "rules": [
        {
            "id": "gc_content",
            "field": "gc_content",
            "type": "double",
            "input": "number",
            "operator": "greater",
            "value": 0.5,
        }
    ],
    "valid": True,
}
CUR_RESULT = "current_result"
CUR_RULES = "current_rules"


class FIG_FORMAT(str, Enum):
    png = "png"
    pdf = "pdf"


class TABLE_NAME(str, Enum):
    bedfiles = "bedfiles"
    bedsets = "bedsets"
    bedset_bedfiles = "bedset_bedfiles"

import os as _os
import sys as _sys
import json

import dash as _dash

if not hasattr(_dash, "__plotly_dash") and not hasattr(_dash, "development"):
    print(
        "Dash was not successfully imported. "
        "Make sure you don't have a file "
        'named \n"dash.py" in your current directory.',
        file=_sys.stderr,
    )
    _sys.exit(1)

from ._imports_ import *  # noqa: E402, F401, F403
from ._imports_ import __all__ as _components
from . import Format  # noqa: F401, E402
from . import FormatTemplate  # noqa: F401, E402

__all__ = _components + ["Format", "FormatTemplate"]

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, "package-info.json"))
with open(_filepath) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")
__version__ = package["version"]

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]


async_resources = ["export", "table", "highlight"]

_js_dist = [
    {
        "relative_package_path": f"dash_table/async-{async_resource}.js",
        "external_url": f"https://unpkg.com/dash-table@{__version__}/dash_table/async-{async_resource}.js",
        "namespace": "dash",
        "async": True,
    }
    for async_resource in async_resources
]

_js_dist.extend(
    [
        {
            "relative_package_path": f"dash_table/async-{async_resource}.js.map",
            "external_url": f"https://unpkg.com/dash-table@{__version__}/dash_table/async-{async_resource}.js.map",
            "namespace": "dash",
            "dynamic": True,
        }
        for async_resource in async_resources
    ]
)

_js_dist.extend(
    [
        {
            "relative_package_path": "dash_table/bundle.js",
            "external_url": f"https://unpkg.com/dash-table@{__version__}/dash_table/bundle.js",
            "namespace": "dash",
        },
        {
            "relative_package_path": "dash_table/bundle.js.map",
            "external_url": f"https://unpkg.com/dash-table@{__version__}/dash_table/bundle.js.map",
            "namespace": "dash",
            "dynamic": True,
        },
    ]
)

_css_dist = []


for _component in __all__:
    setattr(locals()[_component], "_js_dist", _js_dist)
    setattr(locals()[_component], "_css_dist", _css_dist)

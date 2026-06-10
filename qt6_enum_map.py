#!/usr/bin/env python3
"""Map unscoped enum usages to fully-scoped canonical forms using QGIS introspection."""
import enum as enum_mod
import re
import sys
from pathlib import Path

from qgis.core import *  # noqa
from qgis.gui import *  # noqa
import qgis.core, qgis.gui
from qgis.PyQt import QtCore, QtGui, QtWidgets

NAMESPACES = [qgis.core, qgis.gui, QtCore, QtGui, QtWidgets]

def find_class(name):
    for ns in NAMESPACES:
        if hasattr(ns, name):
            return getattr(ns, name)
    return None

def is_enum_member(obj):
    if isinstance(obj, enum_mod.Enum):
        return True
    # sip int-based enum: type is a class whose qualname contains a dot (nested in a Q class)
    t = type(obj)
    return isinstance(obj, int) and not t is int and not t is bool and "." in getattr(t, "__qualname__", "")

def canonical(obj, attr):
    t = type(obj)
    qual = t.__qualname__
    if isinstance(obj, enum_mod.Enum):
        return f"{qual}.{obj.name}"
    return f"{qual}.{attr}"

chain_re = re.compile(r"\b(Q[A-Za-z0-9]+)((?:\.[A-Za-z_][A-Za-z0-9_]*)+)")
pairs = {}
files = [p for p in Path("fireanalyticstoolbox").rglob("*.py") if p.name != "resources.py"]
for f in files:
    for m in chain_re.finditer(f.read_text()):
        cls_name, rest = m.group(1), m.group(2).lstrip(".").split(".")
        cls = find_class(cls_name)
        if cls is None or not isinstance(cls, type):
            continue
        # walk the chain
        attr = rest[0]
        try:
            obj = getattr(cls, attr)
        except AttributeError:
            pairs.setdefault(f"{cls_name}.{attr}", "!!! MISSING")
            continue
        old = f"{cls_name}.{attr}"
        if is_enum_member(obj):
            new = canonical(obj, attr)
            if new != old:
                pairs[old] = new
            else:
                pairs.setdefault(old, "(already canonical)")
        elif isinstance(obj, type) and (issubclass(obj, enum_mod.Enum) or "." in obj.__qualname__):
            # enum type or nested class accessed; if chain continues it's already scoped
            if len(rest) > 1:
                pairs.setdefault(f"{old}.{rest[1]}", "(already scoped)")
            else:
                pairs.setdefault(old, f"(type ref: {obj.__qualname__})")
        else:
            pairs.setdefault(old, f"(non-enum: {type(obj).__name__})")

for old, new in sorted(pairs.items()):
    print(f"{old:55s} -> {new}")

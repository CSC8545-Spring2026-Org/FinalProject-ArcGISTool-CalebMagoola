import sys
import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pyt_path = os.path.join(BASE_DIR, "GriddedClimatologyTool.pyt")

spec = importlib.util.spec_from_file_location("toolbox", pyt_path)
toolbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toolbox)

Tool = toolbox.Tool

def test_import_works():
    assert Tool is not None

    
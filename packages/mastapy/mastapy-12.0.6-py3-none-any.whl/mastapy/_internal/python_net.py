﻿"""python_net.py

Utility module for importing python net modules.
"""


import sys
import os
from typing import Optional


utility_dll = None


def initialise_python_net_importing(utility_dll_path: str):
    """ Initialising the Python.NET importing.

    By providing the path to the MASTA API Utility assembly, we can ensure
    we are importing from the correct assembly.

    Args:
        utility_dll_path (str): Path to the MASTA API Utility assembly
    """

    global utility_dll

    if not os.path.exists(utility_dll_path):
        raise FileNotFoundError(
            'Failed to find the MASTA API Utility assembly.')

    utility_dll = utility_dll_path


def python_net_import(module: str, class_name: Optional[str] = None):
    """ Dynamically imports a Python.NET module

    Args:
        module (str): Module path
        class_name (str, optional): class name
    """

    try:
        # PythonNet only works if you use __import__ for dynamic imports.
        # It does not work for importlib.import_module.
        path = list(filter(None, module.split('.')))
        m = __import__(path[0])

        for p in path[1:]:
            m = getattr(m, p)

        if class_name:
            m = getattr(m, class_name)
    except ImportError:
        raise ImportError((
            'MastaPy has not been initialised. Call \'mastapy.init()\' '
            'with the path to your SMT.MastaAPI.dll file.')) from None
    except Exception:
        raise ImportError(
            'Failed to load {} from {}.'.format(class_name, module)) from None

    return m

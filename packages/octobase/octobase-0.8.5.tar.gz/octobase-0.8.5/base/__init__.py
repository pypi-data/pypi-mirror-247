#!/usr/bin/env python3
''' OctoBase -- The First Building Block For Any Python Project

    Licensed under the Apache License, Version 2.0
    http://www.apache.org/licenses/LICENSE-2.0

    Created and maintained by Octoboxy
    https://octoboxy.com/octobase/
'''

VERSION             = '0.8.5'


# Any exceptions we raise should be defined here
from .              import errors

# Massive library of helper functions
from .              import utils

# Simple dictionary of names to objects
from .registry      import Registry
registry            = Registry()        # singleton

# High-level class with some useful thunking methods
from .things        import Thing

# Our version of unittests
from .testing       import TestCase, TestContext, TestModuleContext, TestRunner
utils.ImportTests()

# Named constants
from .enums         import Enum, Option

# Dynamic downcasting
from .controllers   import Controller, ControllerMixin, ControllerNamespace

# Atomic constants
from .              import consts

# Regular Expressions
from .              import regexp

# DateTime replacement
from .whens         import When
from .commonera     import CommonEra

# Legacy classes, on their way out
from .              import legacy
utils.ParseTimestamp          = legacy.ParseTimestamp
utils.SplitPathToTextAndTime  = legacy.SplitPathToTextAndTime

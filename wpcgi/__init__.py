#!/data/project/nullzero/python/bin/python

import os
import sys

sys.path.append(os.path.abspath(os.path.split(__file__)[0]))
sys.path.append(os.path.abspath(os.path.split(__file__)[0]) + "/package")

from app import create_app
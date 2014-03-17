#!/data/project/nullzerobot/python/bin/python

import os
import sys

sys.path.append(os.path.abspath(os.path.split(__file__)[0]))
sys.path.append(os.path.abspath(os.path.join(os.path.split(__file__)[0], "..")))
os.environ['WPCGI_PATH'] = os.path.abspath(os.path.join(os.path.split(__file__)[0], ".."))
sys.path.append(os.path.abspath(os.path.join(os.path.split(__file__)[0], "package")))

from flask import Flask
app = Flask(__name__)
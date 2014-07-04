import imp
import os

tools = []

for name in os.listdir(os.path.dirname(__file__)):
    file = os.path.join(os.path.dirname(__file__), name)
    if os.path.isdir(file):
        file = os.path.join(file, name + '.py')
        tool = imp.load_source(name, file)
        tools.append(getattr(tool, name))
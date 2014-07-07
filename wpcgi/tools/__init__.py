import imp
import os

tools = []

for name in os.listdir(os.path.dirname(__file__)):
    if not name.startswith('_'): # _ in the front indicates that this tool is disabled
        directory = os.path.join(os.path.dirname(__file__), name)
        if os.path.isdir(directory):
            file = os.path.join(directory, name + '.py')
            tool = imp.load_source(name, file)
            tools.append(getattr(tool, name))
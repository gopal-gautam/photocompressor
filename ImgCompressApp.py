from distutils.core import setup
import py2exe

# setup(console=['ICGui.py'])

# setup(
#     options = {'py2exe': {'bundle_files': 1}},
#     windows = [{'script': "ICGui.py"}],
#     zipfile = None,
# )


setup(
    options = {'py2exe': {'optimize': 2}},
    windows = [{'script': "ICGui.py"}],
    zipfile = "shared.lib",
)
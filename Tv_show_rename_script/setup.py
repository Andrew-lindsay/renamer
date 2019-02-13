from distutils.core import setup
import py2exe

setup(
    # options={'py2exe': {'bundle_files': 2}},
    # zipfile=None,
    windows=[
        {
        "script": "app.py",
        "icon_resources": [(0, "renamer.ico")]
        }
    ],
)

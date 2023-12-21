# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scfile',
 'scfile.exceptions',
 'scfile.files',
 'scfile.files.output',
 'scfile.files.source',
 'scfile.reader',
 'scfile.utils',
 'scfile.utils.dds',
 'scfile.utils.mcsa',
 'scfile.utils.ol']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0', 'lz4>=4.3.2,<5.0.0']

entry_points = \
{'console_scripts': ['build = build:build']}

setup_kwargs = {
    'name': 'sc-file',
    'version': '2.0.0',
    'description': '',
    'long_description': 'SC FILES\n==========================\n\nLibrary and Utility for converting encrypted ``stalcraft`` game files, such as models and textures into well-known formats.\n\nYou can use compiled cli utility from `Releases <https://github.com/onejeuu/sc-file/releases>`_ page.\n\n\n⚠️ Disclaimer\n-------------\n\n**Do not use game assets folder directly.**\n\nYou can get banned for any changes in game client.\n\nCopy files you need to another folder and work there.\n\n\n📁 Formats\n----------\n\n.. list-table::\n   :widths: 20 20 20\n\n   * - Type\n     - Source format\n     - Output format\n   * - Model\n     - .mcsa\n     - .obj\n   * - Texture\n     - .mic\n     - .png\n   * - Texture\n     - .ol\n     - .dds\n\n\n💻 CLI Utility\n--------------\n\nUsage\n~~~~~\n\nYou can drag and drop one or multiple files to ``scfile.exe``.\n\nFrom bash:\n\n.. code:: bash\n\n    scfile [OPTIONS] [FILES]...\n\nArguments\n~~~~~~~~~\n\n- ``FILES``: **List of file paths to be converted**. Multiple files should be separated by **spaces**. Accepts both full and relative paths. **Does not accept directory**.\n\nOptions\n~~~~~~~\n\n- ``-O``, ``--output``: **One path to output file or directory**. Can be specified multiple times for different output files or directories. If not specified, file will be saved in the same directory with a new suffix. You can specify multiple ``FILES`` and a single ``--output`` directory.\n\nExamples\n~~~~~~~~\n\n1. Convert a single file:\n\n    .. code:: bash\n\n        scfile file.mcsa\n\n    Will be saved in the same directory with a new suffix.\n\n2. Convert a single file with a specified path or name:\n\n    .. code:: bash\n\n        scfile file.mcsa --output path/to/file.obj\n\n3. Convert multiple files to a specified directory:\n\n    .. code:: bash\n\n        scfile file1.mcsa file2.mcsa --output path/to/folder\n\n4. Convert multiple files with explicitly specified output files:\n\n    .. code:: bash\n\n        scfile file1.mcsa file2.mcsa -O 1.obj -O 2.obj\n\n    If the count of ``FILES`` and ``-O`` is different, as many files as possible will be converted.\n\n5. Convert all ``.mcsa`` files in the current directory:\n\n    .. code:: bash\n\n        scfile *.mcsa\n\n    In this case, ``-O`` accepts only a directory. Subfolders are not included.\n\n6. Convert all ``.mcsa`` files with subfolders to a specified directory:\n\n    .. code:: bash\n\n        scfile **/*.mcsa -O path/to/folder\n\n    In this case, ``-O`` accepts only a directory. With ``-O`` specified, the folder structure is not duplicated.\n\n\n📚 Library\n----------\n\nInstall\n~~~~~~~\n\nPip\n~~~\n\n.. code:: bash\n\n    pip install sc-file -U\n\nManual\n~~~~~~\n\n.. code:: bash\n\n    git clone git@github.com:onejeuu/sc-file.git\n\n.. code:: bash\n\n    cd sc-file\n\n.. code:: bash\n\n    poetry install\n\nUsage\n~~~~~\n\nSimple\n^^^^^^\n\n.. code:: python\n\n    from scfile import convert\n\n    # Output path is optional.\n    # Defaults to source path with new suffix.\n    convert.mcsa_to_obj("path/to/file.mcsa", "path/to/file.obj")\n    convert.mic_to_png("path/to/file.mic", "path/to/file.png")\n    convert.ol_to_dds("path/to/file.ol", "path/to/file.dds")\n\nAdvanced\n^^^^^^^^\n\n.. code:: python\n\n    from scfile import McsaFile\n\n    with McsaFile("path/to/file.mcsa") as mcsa:\n        obj: bytes = mcsa.to_obj()\n\n    with open("path/to/file.obj", "wb") as fp:\n        fp.write(obj)\n\nBuild\n~~~~~\n\n.. code:: bash\n\n    poetry install\n\n.. code:: bash\n\n    poetry run build\n',
    'author': 'onejeuu',
    'author_email': 'bloodtrail@beber1k.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)

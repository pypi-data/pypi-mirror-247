# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dirstuff', 'dirstuff.cli', 'dirstuff.lib', 'dirstuff.os']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0', 'colorama>=0.4.6,<0.5.0']

entry_points = \
{'console_scripts': ['dirsum = dirstuff.cli.cli:main']}

setup_kwargs = {
    'name': 'dirstuff',
    'version': '0.1.2',
    'description': 'Directory summary tool.',
    'long_description': '# DirStuff\n\n## Summarization\n\nSummarize a directory recursively by file size. This tool can be used to quickly search a drive for large files taking up too much space.\n\n## Installation\n\nInstall the current PyPI release:\n\n```bash\npip install dirstuff\n```\n\n## Usage\n\n```bash\n# Run the tree command to summarize a directory\n$ dirstuff tree <root-dir>\n\n# Specify the minimum file size (default is 10MB)\n$ dirstuff tree <root-dir> --size 750MB\n$ dirstuff tree <root-dir> --size 50KB\n\n# Print full absolute paths to directories instead of directory names\n$ dirstuff tree <root-dir> --absolute\n```\n\n```bash\n# Run the list command to find all directories with a matching name\n$ dirstuff list <root-dir> <dir-name>\n\n# Specify the minimum file size (default is 10MB)\n$ dirstuff list <root-dir> <dir-name> --size 750MB\n$ dirstuff list <root-dir> <dir-name> --size 50KB\n```\n\n```bash\nfrom dirstuff.os import Path\n```\n\n## Examples\n\n### Tree\n\n```bash\n# Summarize the /home/user/my_documents directory\n# showing only directories greater than 20MB in size\n$ dirstuff tree /home/user/my_documents --size 20MB\n```\n\n```python\n|->  69.0 GB > my_documents\n    |->  67.8 GB > movies\n        |->  62.0 GB > from_the_internet\n        |->   5.8 GB > home_movies\n    |-> 638.1 MB > photos\n        |-> 368.2 MB > rock_concert\n        |-> 251.6 MB > vacation_2019\n        |->  18.4 MB > family_photos\n    |-> 521.6 MB > work\n        |-> 263.8 MB > boring_docs\n        |-> 257.7 MB > reports\n    |->  22.5 MB > games\n```\n\n### List\n\n```bash\n# List all node_modules folders under the /home/user/my_code directory\n$ dirstuff list ~/Documents/Code/Projects/Current node_modules\n```\n\n```python\n |-> 419.6 MB > /user/my_code/portfolio/web/node_modules\n |-> 320.3 MB > /user/my_code/fun_project/node_modules\n |-> 298.1 MB > /user/my_code/simple_game/version_2/node_modules\n```\n',
    'author': 'Chris Gregory',
    'author_email': 'christopher.b.gregory@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gregorybchris/dirstuff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)

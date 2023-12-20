# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cumulative']

package_data = \
{'': ['*']}

install_requires = \
['black[jupyter]>=23.12.0,<24.0.0',
 'colorama>=0.4.6,<0.5.0',
 'joblib>=1.3.2,<2.0.0',
 'matplotlib>=3.8.2,<4.0.0',
 'pandas>=2.1.3,<3.0.0',
 'polars>=0.19.17,<0.20.0',
 'pytest>=7.4.3,<8.0.0',
 'scikit-learn>=1.3.2,<2.0.0',
 'scipy>=1.11.4,<2.0.0',
 'sqlalchemy>=2.0.23,<3.0.0',
 'tqdm>=4.66.1,<5.0.0']

setup_kwargs = {
    'name': 'cumulative',
    'version': '0.0.9',
    'description': 'S-curves analysis toolkit.',
    'long_description': '# CUMULATIVE\n\nWork in progress, not yet ready for prime time.\n\n## License\n\nThis project is licensed under the terms of the [BSD 3-Clause License](LICENSE).\n\n',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elehcimd/cumulative',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0',
}


setup(**setup_kwargs)

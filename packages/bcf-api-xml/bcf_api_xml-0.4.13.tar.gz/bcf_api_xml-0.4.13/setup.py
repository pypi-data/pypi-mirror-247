# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcf_api_xml', 'bcf_api_xml.export', 'bcf_api_xml.models']

package_data = \
{'': ['*'], 'bcf_api_xml': ['Schemas/*']}

install_requires = \
['generateDS>=2.35.13,<3.0.0',
 'lxml>=4.5.0,<5.0.0',
 'pillow>=10.0.1,<11.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'xlsxwriter>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'bcf-api-xml',
    'version': '0.4.13',
    'description': 'Convert BCF-API to BCF-XML',
    'long_description': 'BCF-API-XML-converter\n=====================\n\nBCF-API-XML-converter is a library to open BCFzip and get data similar to BCF API json and to save BCF API data as BCFzip files.\n\n\n# Install\n```bash\npip install bcf-api-xml\n```\n\n# usage\n```python\n    from bcf_api_xml import to_zip, to_json\n\n    file_like_bcf_zip = to_zip(topics, comments, viewpoints)\n\n    imported_topics = to_json(file_like_bcf_zip)\n```\n\n# develop\n```bash\npoetry shell\npoetry install\npytest\npre-commit install\n```\n\n# Publish new version\n```bash\npoetry publish --build --username= --password=\n```\n',
    'author': 'Hugo Duroux',
    'author_email': 'hugo@bimdata.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bimdata/BCF-API-XML-translator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

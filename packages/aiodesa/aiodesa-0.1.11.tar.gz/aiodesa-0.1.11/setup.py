# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodesa', 'aiodesa.utils']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=7.2.6,<8.0.0',
 'aiosqlite>=0.19.0,<0.20.0',
 'sphinx-autodoc-typehints>=1.25.2,<2.0.0',
 'sphinx-rtd-theme>=2.0.0,<3.0.0',
 'sphinxcontrib-napoleon>=0.7,<0.8']

setup_kwargs = {
    'name': 'aiodesa',
    'version': '0.1.11',
    'description': "AIODesa offers a straightforward and 100% Python interface for managing asynchronous data access. By leveraging Python's built-ins and standard library, it seamlessly wraps around AioSqlite, providing a hassle-free experience. With AIODesa, you can define, generate, and commit data effortlessly, thanks to shared objects for tables and records.",
    'long_description': '# Asyncio Dead Easy Sql API\n\n## Simplify Your Personal Projects with AIODesa\n\n### Are you tired of the hassle of setting up complex databases for small apllications and personal projects? Designed to streamline monotony, AIODesa makes managing asynchronous database access easy. Perfect for smaller-scale applications where extensive database operations are not a priority.\n\n### *No need to write even a single line of raw SQL.*\n\nA straightforward and 100% Python interface for managing asynchronous database API\'s by leveraging Python\'s built-ins and standard library. It wraps around AioSqlite, providing a hassle-free experience to define, generate, and commit data effortlessly, thanks to shared objects for tables and records.\n\n\n### Ideal for Personal Projects\n\nAIODesa is specifically crafted for simpler projects where database IO is minimal. It\'s not intended for heavy production use but rather serves as an excellent choice for personal projects that require SQL structured data persistence without the complexity of a full-scale database setup. SQLite is leveraged here, meaning youre free to use other SQLite drivers to consume and transform the data if your project outgrows AIODesa.\n\n\n### [Read the docs](https://sockheadrps.github.io/AIODesa/index.html)\n\n![AIODesa](https://github.com/sockheadrps/AIODesa/raw/main/AIODesaEx1.png?raw=true)\n\n\n# Usage\n\n__Install via pip__\n```\npip install aiodesa\n```\n\nSample API usage:\n\n```\nfrom aiodesa import Db\nimport asyncio\nfrom dataclasses import dataclass\nfrom aiodesa.utils.tables import ForeignKey, UniqueKey, PrimaryKey, set_key\n\n\nasync def main():\n\t# Define structure for both tables and records\n\t# Easily define key types\n\t@dataclass\n\t@set_key(PrimaryKey("username"), UniqueKey("id"), ForeignKey("username", "anothertable"))\n\tclass UserEcon:\n\t\tusername: str\n\t\tcredits: int | None = None\n\t\tpoints: int | None = None\n\t\tid: str | None = None\n\t\ttable_name: str = "user_economy"\n\n\n\tasync with Db("database.sqlite3") as db:\n\t\t# Create table from UserEcon class\n\t\tawait db.read_table_schemas(UserEcon)\n\n\t\t# Insert a record\n\t\trecord = db.insert(UserEcon.table_name)\n\t\tawait record(\'sockheadrps\', id="fffff")\n\n\t\t# Update a record\n\t\trecord = db.update(UserEcon.table_name, column_identifier="username")\n\t\tawait record(\'sockheadrps\', points=2330, id="1234")\n\t\t\n\nasyncio.run(main())\n\n```\n\n<br>\n\n# Development:\n\nEnsure poetry is installed:\n\n```\npip install poetry\n```\n\nInstall project using poetry\n\n```\npoetry add git+https://github.com/sockheadrps/AIODesa.git\npoetry install\n```\n\ncreate a python file for using AIODesa and activate poetry virtual env to run it\n\n```\npoetry shell\npoetry run python main.py\n```\n',
    'author': 'sockheadrps',
    'author_email': 'r.p.skiles@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

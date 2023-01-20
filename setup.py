from setuptools import setup

setup(
    name='qbsync',
    version='0.1.0',
    package_dir={'': 'src'},
    install_requires=[
        'click==8.1.3',
        'Flask==2.2.2',
        'Flask-Spyne==0.1',
        'importlib-metadata==4.12.0',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'lxml==4.9.1',
        'MarkupSafe==2.1.1',
        'pytz==2022.2.1',
        'six==1.16.0',
        'spyne==2.14.0',
        'Werkzeug==2.2.2',
        'zipp==3.8.1',
        'suds',
        'xmltodict',
        'argparse',
        'loguru',
        'spnexus~=0.0.62',
        'PyYAML',
    ],
)

try:
    from setuptools import setup
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    from distutils.core import setup

config = {
    'description':
        'mms-certificates generates certificates for munichmotorsport members',
    'author': 'Florian Eich',
    'url': 'https://github.com/floGik/mms-certificates.git',
    # 'download_url': 'git.nrmncr.net/RaceControl',
    'author_email': 'flrn@nrmncr.net',
    'version': '0.1',
    'install_requires': [
        'gspread',
        'oauth2client',
        'PyOpenSSL',
        'jinja2',
        'latex'
    ],

    'packages': ['certificates'],
    'scripts': [
        'bin/certificates'
    ],

    'data_files': [
        'etc/mms-zeugnisse-4b0d902bf20d.json',
        'etc/certificates.cfg'
    ],

    'name': 'mms-certificates'
}

setup(**config)

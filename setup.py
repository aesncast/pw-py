 
#!/usr/bin/env python
from setuptools import setup, find_packages
from pw.config import PROG, AUTHOR, VERSION


setup_info = dict(
    name=PROG,
    version=VERSION,
    author=AUTHOR,
    author_email='94376350+aesncast@users.noreply.github.com',
    url='TODO',
    download_url='https://github.com/aesncast/pw-py/releases/latest',
    project_urls={
        'Documentation': 'TODO',
        'Source': 'https://github.com/aesncast/pw-py',
        'Tracker': 'https://github.com/aesncast/pw-py/issues'
    },
    description='Password generator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='GPL-3',
    classifiers=[],

    # Package info
    packages=['pw'] + ['pw.' + pkg for pkg in find_packages('pw')],
    entry_points={'console_scripts': [PROG + "=pw.__main__:__main__"]},
    
    # requirements
    install_requires=[
        'clipboard>=0.0.4',
        'appdirs>=1.4.4',
        'base58>=2.1.1'
    ],

    zip_safe=True,
)

setup(**setup_info)

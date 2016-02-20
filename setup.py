from setuptools import find_packages, setup

from mo import __version__


with open('README.rst') as file:
    long_description = file.read()

setup(
    name='mo',
    version=__version__,
    description='Incredibly simple YAML-based task runner.',
    long_description=long_description,
    url='https://github.com/thomasleese/mo',
    author='Thomas Leese',
    author_email='inbox@thomasleese.me',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['mo = mo.cli:main']
    },
    install_requires=[
        'PyYAML',
        'colorama'
    ],
    test_suite='tests',
    download_url='https://github.com/thomasleese/mo/releases',
    keywords=['task', 'runner'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities'
    ],
)

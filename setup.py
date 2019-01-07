from setuptools import setup

meta = {}
exec(open('./roipoly/version.py').read(), meta)
meta['long_description'] = open('./README.org').read()

setup(
    name='roipoly',
    version=meta['__version__'],
    description='Tool to draw regions of interest (ROIs)',
    long_description=meta['long_description'],

    author='Joerg Doepfert',
    author_email='joerg.doepfert@gmx.net',
    url='https://github.com/jdoepfert/roipoly.py',
    python_requires='>=2.7',
    install_requires=[
        'matplotlib',
        'numpy',
    ],
    packages=['roipoly'],
    license='Apache License, Version 2.0',
)

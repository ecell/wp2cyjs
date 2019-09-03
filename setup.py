from setuptools import setup

__version__ = '0.0.1'

with open("README.md") as f:
    long_description = f.read()

setup(
    name='wp2cyjs',
    version=__version__,
    url='https://github.com/ecell/wp2cyjs',
    license='MIT',
    py_modules=['wp2cyjs'],
    python_requires='>=3.6',
    author='Kozo Nishida',
    author_email='knishida@riken.jp',
    install_requires=['beautifulsoup4', 'requests'],
    description='Convert Wikipathways pathway XML(GPML) to Cytoscape.js JSON (.cyjs)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=['License :: OSI Approved :: MIT License',]
)

import setuptools


with open('README.md', 'r') as f:
    long_desc = f.read()


setuptools.setup(
    name='blaseball-mike',
    version='1.1.3',
    author='Joe Maliksi',
    author_email='joe.maliksi@gmail.com',
    url='https://github.com/jmaliksi/blaseball-mike',
    description='Read-only Python wrapper around blaseball game API',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
)

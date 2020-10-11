import setuptools


with open('README.md', 'r') as f:
    long_desc = f.read()


setuptools.setup(
    name='blaseball-mike',
    version='3.1.1',
    author='Joe Maliksi',
    author_email='joe.maliksi@gmail.com',
    url='https://github.com/jmaliksi/blaseball-mike',
    description='Read-only Python wrapper around blaseball game API',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires="~=3.6",
)

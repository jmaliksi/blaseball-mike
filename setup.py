import setuptools


with open('README.md', 'r') as f:
    long_desc = f.read()


install_requires = [
    'aiohttp',
    'aiohttp-sse-client',
    'python-dateutil',
    'requests',
    'ujson',
    'requests-cache'
    ]

setuptools.setup(
    name='blaseball-mike',
    version='5.2.0',
    author='Joe Maliksi',
    author_email='joe.maliksi@gmail.com',
    url='https://github.com/jmaliksi/blaseball-mike',
    description='Read-only Python wrapper around blaseball game API',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires="~=3.8",
)

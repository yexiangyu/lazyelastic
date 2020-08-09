from setuptools import setup, find_packages

setup(
    name="lazyelastic",
    version="0.2.1",
    keywords=("lazy", "elasticsearch", "orm"),
    long_description="lay elastic orm, create/search/delete",
    license="MIT Licence",
    url="https://github.com/yexiangyu/lazyelastic",
    author="yexiangyu",
    author_email="yexiangyu@maimenggroup.com",
    packages=['lazyelastic'],
    platforms="any",
    install_requires=[
        'setuptools',
        'elasticsearch >=7.8.0',
        'aiohttp',
    ],
)

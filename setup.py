from setuptools import setup, find_packages

setup(
    name="lazyelastic",
    version="0.2",
    keywords=("lazy", "elasticsearch", "orm"),
    long_description="lay elastic orm, create/search/delete",
    license="MIT Licence",
    url="https://codeup.aliyun.com/5f166157db0493ecef90a46c/mmcloud/lazyelastic",
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

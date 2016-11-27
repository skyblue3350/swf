# -*- encoding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="swf",
    version="0.1",
    description="Parse SWF File",
    author="skyblue3350",
    author_email="skyblue3350@gmail.com",
    install_requires=["numpy", "PIL"],
    url="http://sky-net.pw",
    license="MIT License",
    packages=find_packages(exclude=("tests")),
    test_suite="tests",
)

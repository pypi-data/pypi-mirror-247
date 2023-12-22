from setuptools import setup, find_packages

setup(
    name='schedule-sdk',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        "requests",
        "redis"
    ],
)
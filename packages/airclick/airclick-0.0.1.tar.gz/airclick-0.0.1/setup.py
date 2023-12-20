from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'airclick 相关python包'

setup(
    name="airclick",
    version=VERSION,
    author="aojoy",
    author_email="aojoytec@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    keywords=['python', "airscript"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/itisl2220/airscript",
)

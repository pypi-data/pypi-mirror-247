from setuptools import setup
import os
folders = []
for folder in os.listdir("zrcl3"):
    if os.path.isdir(os.path.join("zrcl3", folder)):
        folders.append(os.path.join("zrcl3", folder))

setup(
    name="zrcl3",
    version="1.0.6",
    packages=folders + ["zrcl3"],
    description="zack's common reusable library",
    author="ZackaryW",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    url="https://github.com/ZackaryW/py-zrcl3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
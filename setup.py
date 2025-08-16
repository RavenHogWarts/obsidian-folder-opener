# -*- coding: utf-8 -*-
"""
Obsidian文件夹打开器安装包配置
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="open-folder-with-obsidian",
    version="1.0.0",
    author="RavenHogwarts",
    author_email="",
    description="用Obsidian打开文件夹的Windows右键菜单工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RavenHogwarts/open-folder-with-obsidian",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "open-folder-with-obsidian=main:main",
            "obsidian-installer=installer:main",
        ],
    },
)

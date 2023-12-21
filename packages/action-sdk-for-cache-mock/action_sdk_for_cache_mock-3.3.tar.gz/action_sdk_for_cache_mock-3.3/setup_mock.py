# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import shutil

import action_sdk_for_cache

dst_ = f".{os.sep}action_sdk_for_cache{os.sep}action_cache_sdk.py"
if os.path.exists(dst_) is True:
    os.remove(dst_)

shutil.copyfile(f'.{os.sep}action_sdk_for_cache{os.sep}mock{os.sep}action_cache_sdk.py',
                dst_)

NAME = 'action_sdk_for_cache_mock'
DESCRIPTION = 'sdk used for honeyguide app'
AUTHOR = 'flagify'
#VERSION = '0.1'
VERSION = action_sdk_for_cache.__version__
with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=">=3.6",
    install_requires=["requests"],
    license='MIT',

    packages=find_packages(exclude=[
        'tests.*', 'tests',
        'examples.*', 'examples',
        'dat.*', 'dat', 'action_sdk_for_cache.src', 'action_sdk_for_cache.mock']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False,
)

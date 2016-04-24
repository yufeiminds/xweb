#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
        'xweb=xweb.interactive:cli'
    ]
}

requirements = [
    'flask',
    'click',
    'PyYaml',
    'six',
    'chardet'
]

test_requirements = [
    'nose'
]

setup(
    name='xweb',
    version='0.1.0',
    description="A micro web service framework.",
    author="Yufei Li",
    author_email='yufeiminds@gmail.com',
    url='https://github.com/yufeiminds/xweb',
    py_modules=['xweb'],
    entry_points=entry_points,
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='web',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

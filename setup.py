from setuptools import setup, find_packages

import versioneer


long_description = """\
quetzal-client
==============

A Python package that provides a layer on top of quetzal-openapi-client for
easier usage of the [Quetzal API](https://quetz.al).
"""
dependencies = [
    'click',
    'backoff',
    'requests',
    'appdirs',
    'PyYAML',
    'pyreadline;platform_system=="Windows"',
    'quetzal-openapi-client>=0.5.0,<0.6',
]

setup_requires = dependencies[:]
# extra_dependencies = []

setup_args = dict(
    name='quetzal-client',
    version=versioneer.get_version(),
    description="Python client and helpers to the Quetzal API",
    author='David Ojeda',
    author_email='support@quetz.al',
    url='https://github.com/quetz-al/quetzal-client',
    project_urls={
        "Documentation": "https://quetzal-client.readthedocs.io",
        "Code": "https://github.com/quetz-al/quetzal-client",
        "Issue tracker": "https://github.com/quetz-al/quetzal-client/issues",
    },
    license="BSD-3-Clause",
    keywords=["OpenAPI", "Quetzal API"],
    # keywords='',
    packages=find_packages(exclude=['docs', 'tests']),
    namespace_packages=['quetzal'],
    python_requires='>=3.6',
    install_requires=dependencies,
    tests_require=['pytest', ],
    zip_safe=False,
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Archiving',
    ],
    entry_points={
        'console_scripts': [
            'quetzal-client = quetzal.client.cli.main:cli',
        ],
    },
    cmdclass=versioneer.get_cmdclass(),
)

setup(**setup_args)

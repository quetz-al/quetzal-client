from setuptools import setup, find_packages

import versioneer


long_description = '...'
dependencies = [
    'quetzal-openapi-client',
    'click',
    'backoff',
    'requests',
    'appdirs',
    'PyYAML',
    'pyreadline;platform_system=="Windows"',
]

setup_requires = dependencies[:]
# extra_dependencies = []

setup_args = dict(
    name='quetzal-client',
    description="Python client to the Quetzal API",
    long_description=long_description,
    author='David Ojeda',
    author_email='david.ojeda@gmail.com',
    url='https://github.com/dojeda/quetzal-client',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='Proprietary',
    platforms=['Linux', 'OSX', 'Windows'],
    # keywords='',
    packages=find_packages(exclude=['docs', 'tests', 'test']),
    install_requires=dependencies,
    setup_requires=setup_requires,
    # build_requires=setup_requires,
    tests_require=['pytest', ],
    # extras_require=extra_dependencies,
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'quetzal-client = quetzal.client.cli.main:cli',
        ],
    },
    # dependency_links=dependency_links,
)

setup(**setup_args)

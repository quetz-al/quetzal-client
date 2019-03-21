from setuptools import setup, find_packages

import versioneer


long_description = '...'
dependencies = [
    'click',
    'backoff',
    'requests',
    'appdirs',
    'PyYAML',
    'pyreadline;platform_system=="Windows"',
    'quetzal-openapi-client @ git+https://github.com/quetz-al/quetzal-openapi-client.git@v0.2.0#egg=quetzal-openapi-client',
]

setup_requires = dependencies[:]
# extra_dependencies = []

setup_args = dict(
    name='quetzal-client',
    description="Python client to the Quetzal API",
    long_description=long_description,
    author='David Ojeda',
    author_email='david@dojeda.com',
    url='https://github.com/quetz-al/quetzal-client',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='Proprietary',
    platforms=['Linux', 'OSX', 'Windows'],
    # keywords='',
    packages=find_packages(exclude=['docs', 'tests', 'test']),
    namespace_packages=['quetzal'],
    python_requires='>=3.6',
    install_requires=dependencies,
    tests_require=['pytest', ],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'quetzal-client = quetzal.client.cli.main:cli',
        ],
    },
)

setup(**setup_args)

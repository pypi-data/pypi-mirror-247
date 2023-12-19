from setuptools import setup, find_packages

# read version
version_globals = {}
with open("trustar2/version.py", encoding="utf-8") as fp:
    exec(fp.read(), version_globals)
version = version_globals['__version__']

setup(
    name='trustar2',
    packages=find_packages(exclude=("tests",)),
    version=version,
    author='TruSTAR Technology, Inc.',
    author_email='dsolmirano@splunk.com',
    url='https://github.com/trustar/trustar-sdk2-proto/',
    download_url=f'https://github.com/trustar/trustar-sdk2-proto/tarball/{version}',
    description='Python SDK2 for the TruSTAR REST API',
    license='MIT',
    install_requires=['json_log_formatter',
                      'python-dateutil',
                      'pytz',
                      'requests',
                      'configparser',
                      'dateparser',
                      'tzlocal',
                      'PyYAML',
                      ],
    include_package_data=True,
)

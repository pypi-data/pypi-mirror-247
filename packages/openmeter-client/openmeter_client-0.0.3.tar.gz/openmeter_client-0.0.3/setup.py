from setuptools import setup, find_packages

setup(
    name='openmeter_client',
    version='0.0.3',
    description='A Python client to interact with the OpenMeter API endpoints',
    packages=find_packages(where='src'),  # Update the 'where' parameter
    package_dir={'': 'src'},  # Update the package directory
    install_requires=[
        "requests",
        "pandas",
        "loguru",
    ],
    package_data={
        '': ['docs/*'],
    },
)
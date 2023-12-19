from setuptools import setup, find_packages

setup(
    name="telesco_utils",
    version="0.4.2",
    packages=find_packages(),
    description='This package provides general-purpose functionality',
    author='Rhubenni Telesco',
    url='https://github.com/rhubenni/telesco-utils',
    license='CC0-1.0',
    install_requires=[
        'requests', 'python-dotenv', 'pyodbc'
    ],
    python_requires='>=3.9'
)
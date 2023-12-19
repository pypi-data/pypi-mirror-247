from setuptools import setup, find_packages

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="Testing-sample2",
    version="0.2.0",
    author="zebu",
    author_email="venkateshnsm@gmail.com",
    description="This PIP package used for testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/Zebu-Dev/Mynt-PY-Api-Package.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.31.0',
        'websocket_client>=1.6.0',
        'pandas>=1.6.0',
        'pyyaml>=6.0'
    ],
)

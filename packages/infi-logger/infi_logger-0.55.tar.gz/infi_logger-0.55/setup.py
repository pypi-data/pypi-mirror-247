from setuptools import find_packages, setup

setup(
    dependency_links=[],
    name="infi_logger",
    packages=find_packages(),
    version="0.55",
    description="Logger package for infinity team",
    author="Infinity Team",
    install_requires=[
        "certifi==2023.7.22; python_version >= '3.6'",
        "colorama==0.4.6; sys_platform == 'win32'",
        "elastic-transport==8.10.0; python_version >= '3.6'",
        "elasticsearch==8.10.1; python_version >= '3.6' and python_version < '4'",
        "iniconfig==2.0.0; python_version >= '3.7'",
        "packaging==23.2; python_version >= '3.7'",
        "pluggy==1.3.0; python_version >= '3.8'",
        "pytest==7.4.3; python_version >= '3.7'",
        "python-dotenv==1.0.0; python_version >= '3.8'",
        "urllib3==2.0.7; python_version >= '3.7'",
    ],
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

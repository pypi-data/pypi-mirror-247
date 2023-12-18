from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasssi",
    version="0.1",
    author="nhi bataunga",
    description="nhi bataunga",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pygame", "colorama"],
    entry_points={
        "console_scripts": [
            "lasssi=lasssi.main:main",
        ],
    },
    package_data={'lasssi': ['assets/*.mp3', 'assets/*.mp4']},
    include_package_data=True,
)
from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "An API wrapper for the Bloxlink API."

long_desc = ""
with open(".github/README.md") as f:
    long_desc = f.read()

setup(
    name="pybloxlink",
    version=VERSION,
    author="acatiadroid",
    license="The MIT License (MIT)",
    author_email="<acatia@mail.com>",
    url="https://github.com/acatiadroid/pybloxlink",
    project_urls={
        "Issues": "https://github.com/acatiadroid/pybloxlink/issues"
    },
    description=DESCRIPTION,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    install_requires=["aiohttp"],
    keywords=["python", "bloxlink", "api wrapper"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
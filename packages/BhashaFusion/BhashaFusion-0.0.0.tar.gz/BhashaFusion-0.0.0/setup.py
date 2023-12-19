from setuptools import find_packages, setup

with open("BhashaFusion/README.md", "r") as f:
    long_description = f.read()

setup(
    name="BhashaFusion",
    version="0.0.0",
    description="A package used to convert indic language to iast & iast to inidc langauge viceversa",
    packages=['BhashaFusion'],
    package_data={'BhashaFusion': ["iast-token.db"]},

#    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
#    keyword='iast'
    url="https://github.com/dankarthik25/BhashaFusion",
    author="Dan Karthik",
    author_email="dankarthik25@gmail.com",
    project_urls= {
        "Documentation": "https://dankarthik25.github.io/BashaFusion",
        "Source" : "https://github.com/dankarthik25/BhashaFusion",
},
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
#    install_requires=['pysqlite3'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.9",
)


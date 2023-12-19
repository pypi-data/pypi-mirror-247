import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quickinit",
    version="0.0.2",
    author="toto",
    author_email="toto8@duck.com",
    description="""quickinit - quickly scaffold projects in Python, Golang, Web, Next.js and Rust.
Generate starter code and project structure from the command line so you can start coding faster.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toine08/clitool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
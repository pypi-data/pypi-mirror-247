import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yonestools",
    version="0.0.1",
    author="yone",
    author_email="1242925780@qq.com",
    description="tool for convenience",
    url="https://github.com/yonesun/python-class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["yonestools"],
    requires=["datetime"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)
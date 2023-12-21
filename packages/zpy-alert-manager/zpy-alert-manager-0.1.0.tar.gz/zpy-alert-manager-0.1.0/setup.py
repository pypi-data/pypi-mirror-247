import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zpy-alert-manager",
    version="0.1.0",
    author="Noé Cruz | linkedin.com/in/zurckz/",
    author_email="zurckz.services@gmail.com",
    description="Básic module for delivery alerts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoeCruzMW",
    packages=setuptools.find_packages(),
    install_requires=[
        "zpy-api-core==2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)

from setuptools import setup, find_packages

setup(
    name="py_oculus_touch",
    version="0.0.2",
    packages=find_packages(),
    package_data={'':['*.dll']},
    description="An API to interface with your Oculus Touch controllers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eliasbenb/py_oculus_touch",
    author="Elias Benbourenane",
    author_email="eliasbenbourenane@gmail.com",
    license="MIT",  # Or any other license
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)

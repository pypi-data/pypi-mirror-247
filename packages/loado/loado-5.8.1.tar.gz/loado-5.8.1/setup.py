from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="loado",
    version="5.8.1",
    description="Easy, modern, and beginner friendly loading animations.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/toolkitr/loado",
    author="loado",
    author_email="toolkitr.email@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta",
        "Development Status :: 3 - Alpha",
        "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Natural Language :: English"
    ],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.7",
)
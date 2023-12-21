from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="calar",
    version="2.5.1",
    description="The text colorizer everyone needs!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/calar",
    author="calar",
    author_email="calar.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta",
        "Development Status :: 3 - Alpha",
        "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    packages=find_packages(exclude=["tests", "docs"]),
    include_package_data=True,
    install_requires=[
        'pygments',
    ],
    python_requires=">=3.7",
)
from setuptools import find_packages, setup

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="gazpacho",
    version="1.1-alpha",
    description="The simple, fast, and modern web scraping library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=["web scraping", "BeautifulSoup", "requests"],
    url="https://github.com/maxhumber/gazpacho",
    author="Max Humber",
    author_email="max.humber@gmail.com",
    license="MIT",
    packages=find_packages(),
    package_data={"gazpacho": ["py.typed"]},
    extras_require={
        "dev": ["black>=20.8b1", "mypy>=0.782", "portray>=1.4.0", "pytest>=6.0.2"],
    },
    python_requires=">=3.6",
    setup_requires=["setuptools>=38.6.0"],
    zip_safe=False,
)

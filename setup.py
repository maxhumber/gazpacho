from setuptools import setup

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="gazpacho",
    version="0.9",
    description="gazpacho is a web scraping library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["web scraping", "web", "scraping", "BeautifulSoup", "requests"],
    url="https://github.com/maxhumber/gazpacho",
    author="Max Humber",
    author_email="max.humber@gmail.com",
    license="MIT",
    packages=["gazpacho"],
    python_requires=">=3.6",
    setup_requires=["setuptools>=38.6.0"],
)

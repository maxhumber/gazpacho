from setuptools import setup

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='gazpacho',
    version='0.0.1',
    description='NO SOUP FOR YOU',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    keywords=[
        'web', 'web scraping', 'beautifulsoup'
    ],
    url='https://github.com/maxhumber/gazpacho',
    author='Max Humber',
    author_email='max.humber@gmail.com',
    license='MIT',
    packages=['gazpacho'],
    python_requires='>=3.6',
    setup_requires=['setuptools>=38.6.0']
)
from setuptools import setup, find_packages

VERSION = '0.3'
DESCRIPTION = 'Tools to make a compiler in python'
LONG_DESCRIPTION = 'A package that contains a lexer and a parser that creates an AST.'

# Setting up
setup(
    name="compyler-tools",
    version=VERSION,
    author="ricardoquinteladev",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'compiler', 'lexer', 'parser', 'lalr', 'ast'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

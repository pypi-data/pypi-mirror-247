import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codeepy",
    version="2.0.0",
    author="Marita Fitzgerald",
    author_email="maritafitzgerald@gmail.com",
    maintainer="Simon Egerton",
    maintainer_email="segerton@creativescience.com",
    description="A library for the Codee Robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/segertonGH/CodeePy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
	install_requires=[
   'pyfirmata2',
   'pyserial'
	],
)


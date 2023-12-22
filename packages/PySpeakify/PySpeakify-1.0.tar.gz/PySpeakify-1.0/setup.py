from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

# Setting up
setup(
    name="PySpeakify",
    version="1.0",
    author="Ephiliaa",
    author_email="abinsibin63@gmail.com",
    long_description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pyttsx3'],
    keywords=['talk', 'python talk', 'speak', 'python speak'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
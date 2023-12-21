import setuptools


setuptools.setup(
    name="moki",
    version="0.0.2",
    author="bk",
    author_email="wowlupin@outlook.com",
    description="remove boring print warning of mobi",
    long_description="",
    long_description_content_type="",
    packages=setuptools.find_packages(),
    license="GPL-3.0",
    install_requires = ['loguru>=0.6,<0.7'],
    python_requires = ">=3.7"
)

from setuptools import setup, find_packages

setup(
    name="abdulkerim",
    version="0.3",
    packages=find_packages(),
    author='Ali Cenk Baytop',
    author_email='baytop.alicenk@gmail.com',
    description='Fun',
    install_requires=[],
    entry_points={
        "console_scripts": [
            "abdulkerim-hello = abdulkerim_hello:hello"
        ],
    },
)
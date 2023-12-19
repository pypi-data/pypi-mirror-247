from setuptools import setup

setup(
    name="syntheseus-chemformer",
    version="0.1.0",
    package_dir={
        "chemformer": ".",
        "chemformer.molbart": "molbart"
    },
    package_data={"": ["*.txt"]},
    install_requires=[
        "pytorch-lightning==1.9.4",
        "syntheseus-PySMILESutils"
    ],
    url="https://github.com/kmaziarz/Chemformer",
)

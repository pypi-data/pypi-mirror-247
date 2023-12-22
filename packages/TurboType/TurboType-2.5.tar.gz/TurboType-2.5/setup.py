from setuptools import setup, find_packages

setup(
    name="TurboType",
    version="2.5",
    author="1337",
    description="A Game for Typing challenge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pygame"],
    entry_points={"console_scripts": ["TurboType = src.TurboType:main"]},
)
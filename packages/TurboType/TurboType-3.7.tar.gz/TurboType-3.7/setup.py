from setuptools import setup, find_packages

setup(
    name="TurboType",
    version="3.7",
    author="1337",
    description="A Game for Typing challenge",
    packages=find_packages(),
    package_data={'TurboType': ['data/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pygame"],
    entry_points={"console_scripts": ["TurboType = src.TurboType:main"]},
)

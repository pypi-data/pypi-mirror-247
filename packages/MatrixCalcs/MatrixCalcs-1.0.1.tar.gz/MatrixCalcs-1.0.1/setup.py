from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="MatrixCalcs",
    version="1.0.1",
    description="A matrix calculator in your command line.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matjohn10/MatrixCalculator",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.10",
    ],
    author="Mathieu Johnson",
    author_email="mathieujohnson10@gmail.com",
    license="MIT",
    entry_points={
        "console_scripts": ["matcalc=matrixcalc.command_line:run"],
    },
    install_requires=["numpy >= 1.26.2"],
    extras_require={
        "dev": ["pytest>=7.4", "twine>=4.0.2"]
    },
    python_requires=">=3.10",
)

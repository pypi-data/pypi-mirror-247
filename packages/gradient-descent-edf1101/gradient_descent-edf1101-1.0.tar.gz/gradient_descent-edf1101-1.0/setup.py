import setuptools

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="gradient_descent-edf1101",
    version="1.0",
    author="Ed Fillingham",
    description="Gradient Descent module",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/edf1101/GradientDescent",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["matplotlib"]
)
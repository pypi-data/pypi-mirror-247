import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spartacloud", # Replace with your own username
    version="0.1",
    author="Benjamin Meyer",
    author_email="spartacloud@gmail.com",
    description="Spartacloud Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://spartaquant.com",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
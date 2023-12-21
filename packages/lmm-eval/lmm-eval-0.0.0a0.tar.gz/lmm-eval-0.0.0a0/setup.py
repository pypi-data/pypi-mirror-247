from setuptools import setup, find_packages


setup(
    name="lmm-eval",
    version="0.0.0-alpha-0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
    ],
    include_package_data=True,
    author="Fanyi Pu",
    author_email="FPU001@e.ntu.edu.sg",
    description="LMM-Eval",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
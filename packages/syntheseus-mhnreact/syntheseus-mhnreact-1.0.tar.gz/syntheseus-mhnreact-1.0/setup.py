import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syntheseus-mhnreact",
    version="1.0",
    description="Fork of MHNreact for use in the syntheseus library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmaziarz/mhn-react",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "scikit-learn",
        "scipy",
        "swifter",
        "tqdm",
        "wandb",
    ],
    python_requires='>=3.7',
)

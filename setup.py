import setuptools

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

setuptools.setup(
    name="kaggle",
    version="0.1",
    description="To imrpove our Data Science skills",
    url="https://github.com/jackt153/kaggle",
    author="Kaggle Bros",
    author_email="@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=REQUIREMENTS,
    zip_safe=False,
)

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

REPO_NAME = "Real_Time_Credit_Card_Fraud_Detection_System"
AUTHOR_USER_NAME = "santosh3110"
SRC_REPO = "fraud_detection"
AUTHOR_EMAIL = "santoshkumarguntupalli@gmail.com"
LIST_OF_REQUIREMENTS = []


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small local packages for detecting and alerting credit card fraud transactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    packages=setuptools.find_packages(),
    license="Apache License 2.0",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)
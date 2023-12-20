from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="helper20sms",
    version="0.3.1",
    url="https://github.com/HelperSMS/helper20sms",
    license="MIT License",
    author="HelperSMS",
    author_email="admin@helper20sms.ru",
    description="HelperSMS API wrapper for Python",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["aiohttp~=3.8.4", "typing~=3.7.4.3", "requests~=2.31.0"],
    python_requires=">=3.9",
    project_urls={"Documentation": "https://api.helper20sms.ru/docs"},
)

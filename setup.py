from setuptools import setup, find_packages

setup(
    name="erpn8n",
    version="0.0.1",
    description="ERPNext ChatGPT-style AI assistant using n8n",
    author="Apex Logic Software",
    author_email="info@apexlogicsoftware.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"],
)

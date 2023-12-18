from setuptools import find_packages, setup

setup(
    name="azurepricingapi",
    version="0.3.0",
    description="Python SDK to leverage Azure Pricing API",
    url="https://github.com/ravi-ck/azure-pricing-api-python",
    author="Ravi Rana",
    author_email="ravi.rana@tothenew.com",
    license="Apache-2.0 license",
    packages=find_packages(),
    install_requires=[
        "requests",
        "uplink"
    ]
)
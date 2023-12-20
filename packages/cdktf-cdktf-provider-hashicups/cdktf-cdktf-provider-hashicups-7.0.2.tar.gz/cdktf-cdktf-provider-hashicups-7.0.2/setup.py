import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-hashicups",
    "version": "7.0.2",
    "description": "Prebuilt hashicups Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-hashicups.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-hashicups.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_hashicups",
        "cdktf_cdktf_provider_hashicups._jsii",
        "cdktf_cdktf_provider_hashicups.data_hashicups_coffees",
        "cdktf_cdktf_provider_hashicups.data_hashicups_ingredients",
        "cdktf_cdktf_provider_hashicups.data_hashicups_order",
        "cdktf_cdktf_provider_hashicups.order",
        "cdktf_cdktf_provider_hashicups.provider"
    ],
    "package_data": {
        "cdktf_cdktf_provider_hashicups._jsii": [
            "provider-hashicups@7.0.2.jsii.tgz"
        ],
        "cdktf_cdktf_provider_hashicups": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf>=0.19.0, <0.20.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.93.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)

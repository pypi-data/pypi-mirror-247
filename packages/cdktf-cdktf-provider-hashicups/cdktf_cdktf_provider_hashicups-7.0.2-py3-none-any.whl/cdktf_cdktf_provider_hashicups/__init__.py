'''
# CDKTF prebuilt bindings for hashicorp/hashicups provider version 0.3.1

HashiCorp made the decision to stop publishing new versions of prebuilt [Terraform hashicups provider](https://registry.terraform.io/providers/hashicorp/hashicups/0.3.1) bindings for [CDK for Terraform](https://cdk.tf) on December 19, 2023. As such, this repository has been archived and is no longer supported in any way by HashiCorp. Previously-published versions of this prebuilt provider will still continue to be available on their respective package managers (e.g. npm, PyPi, Maven, NuGet), but these will not be compatible with new releases of `cdktf` past `0.19.0` and are no longer eligible for commercial support.

As a reminder, you can continue to use the `hashicorp/hashicups` provider in your CDK for Terraform (CDKTF) projects, even with newer versions of CDKTF, but you will need to generate the bindings locally. The easiest way to do so is to use the [`provider add` command](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#provider-add), optionally with the `--force-local` flag enabled:

cdktf provider add hashicorp/hashicups --force-local

For more information and additional examples, check out our documentation on [generating provider bindings manually](https://cdk.tf/imports).

## Deprecated Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-hashicups](https://www.npmjs.com/package/@cdktf/provider-hashicups).

`npm install @cdktf/provider-hashicups`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-hashicups](https://pypi.org/project/cdktf-cdktf-provider-hashicups).

`pipenv install cdktf-cdktf-provider-hashicups`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Hashicups](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Hashicups).

`dotnet add package HashiCorp.Cdktf.Providers.Hashicups`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-hashicups](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-hashicups).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-hashicups</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-hashicups-go`](https://github.com/cdktf/cdktf-provider-hashicups-go) package.

`go get github.com/cdktf/cdktf-provider-hashicups-go/hashicups`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-hashicups).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "data_hashicups_coffees",
    "data_hashicups_ingredients",
    "data_hashicups_order",
    "order",
    "provider",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import data_hashicups_coffees
from . import data_hashicups_ingredients
from . import data_hashicups_order
from . import order
from . import provider

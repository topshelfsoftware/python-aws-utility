# python-aws-utility

Utility functions for interacting with AWS.

## Makefile

A `Makefile` is provided to standardize building and publishing the Python package. Satisfy the following prerequisites to be successful:

- Install Python 3.9 and add to PATH (executable name assumed to be `python3.9`)
- Create a file named `local_pypi_dir.txt` in the project root directory (same folder as this `README`)
  - Contents of file are a single line defining the path to a local directory to be used as a local PyPI repository

### Project Dependencies

Install project dependencies by running the following command one time

```bash
# install project deps such as poetry
make install
```

### Build Instructions

Simply navigate to the same folder as this `README`, and run the following command to build and publish the utility package to a local PyPI repo.

```bash
make
```

This command activates the virtual environment with `poetry`, builds the package as a wheel and copies it to the local PyPI repository.

## Versioning

This package uses Semantic Versioning 2.0.0 to describe MAJOR.MINOR.PATCH releases.

IMPORTANT❗
Search the project for the existing package version and update in the following places prior to building the package and deploying the lambda layer:

- `PKG_VER` variable in the project `Makefile`
- `version` in the poetry `pyproject.toml`
- `PackageVersion` parameter in the `template.yaml`
- `topshelfsoftware-aws-util` package in the `lambda_layer/no_deps/requirements.txt`

## Tagging

After incrementing the package version (and merging PR), create an associated tag of the repository. Perform the following from the command line:

```bash
git tag -a <version> <commit_hash>
```

`<version>` will take the form vX.Y.Z where X.Y.Z represents MAJOR.MINOR.PATCH in semantic versioning. Then push the tag to the remote server using:

```bash
git push origin <version>
```

## Available Modules

See the list of [available modules](./docs/README.md#available-modules).

# S4 Platform API

## Requirements

`s4-platform-api` requires Python 3.9+.


## Contributing

This may change in the future, but for now, please follow [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) style. The short summary of this is, when you open a PR or make a commit:

- If you change code, prefix your PR title with `fix:` if it's a fix or `feat:` if it adds a feature.
- If you change the API, include the text `BREAKING CHANGE` in your PR title.
- If you don't change code at all, prefix the PR title with `ci:`, `docs:`, `test:`, `build:`, or something else.

The version of the library will be incremented according to the text in merged PRs, so that it follows [semver](https://semver.org/).


#### Clarifications
"Adding a feature" includes, at least, any time you make something available to users of the library which wasn't available before. If you remove or change current behaviour, you're changing the API.

## Developer Setup

1. Install poetry: `brew install poetry`
2. Install dependencies: `poetry install`
3. Export AUTH0_DOMAIN=dev-d3p316sq.us.auth0.com and AUTH0_AUDIENCE=https://dev-d3p316sq.us.auth0.com/api/v2/ as environment variables
4. Export AUTH0_TEST_CLIENT_ID=D9wQOscnTJnXEmimsviFiDimppJ7A1bK and AUTH0_TEST_CLIENT_SECRET as environment variables. Secret's value is in LastPass as "Auth0 test client secret" in "Shared-Platypus" folder

### Testing

#### Unit tests
From the root directory: `poetry run pytest test/`

#### Integration tests
From the root directory: `poetry run pytest integration_test/`

#### All tests
From the root directory: `poetry run pytest`

### Building

To build a source and binary wheel distribution: `poetry build`

### Examples
Scripts from the `examples` directory use the library. These can be run from the command line.

    `poetry run examples/get_prospective_task 614e1f114640ba4b197af7ea`

The file `examples/.env` contains configurable parameters used by the examples scripts. Edit this as necessary or
override by setting environment variables on the system running the scripts.

    HOST_URL=http://example.org/orange get_prospective_task 614e1f114640ba4b197af7ea

### URI Override
If this library is run within an AWS deployment application queries need to be altered to use local networking. If the 
environment variable `URI_OVERRIDE` is present queries to the application will be overwritten to use this value.
e.g.
If connection is initialized with a value of `https://app.laboratory.plat.s4hq.com` and the environment variable
`URI_OVERRIDE` exists with a value `http://localhost:8080`, a query intended to go to 
`https://app.laboratory.plat.s4hq.com/blueHealth` will actually go to `http://localhost:8080/blueHealth`

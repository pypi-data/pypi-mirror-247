# fragment-py

`fragment-py` is a library for using Fragment's Ledger building toolkit while running a subset of your Ledger Accounts on your own infrastructure. 

<img width="1089" alt="EntryPosting" src="https://github.com/fragment-dev/fragment-py/assets/23367193/0fefd0f0-a5b4-4bcf-bcc6-127dc46c9acc">


## Usage

To use the library:
1. Write your fragment schema and add the JSON file to your codebase
2. Generate types from the schema using `python -m fragment.code --schema-path <schema> --destination <destination_file>`
3. Use the generate types to call the Fragment() function 

The e2e tests in `test_fragment.py` can be a good reference for this.

## Contributing

### Prerequisites

We recommend developing against this project using [`pyenv`](https://github.com/pyenv/pyenv) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv).

If you're on macOS, run:
```bash
brew install pyenv pyenv-virtualenv
```

Ensure that **git** is installed on your system.

### Installation

```bash
git clone git@github.com:fragment-dev/fragment-py.git
cd fragment-py
make install
```

### Run tests

```bash
make test
```

### Linting
    
```bash
make lint
```

# UISP CRM

[![PyPI version](https://badge.fury.io/py/uisp-crm.svg)](https://badge.fury.io/py/uisp-crm)

## Overview

`uisp_crm` is a Python library for working with UISP Clients.

## Installation

You can install the library using pip. Open your terminal and run:

```bash
pip install uisp-crm
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## Usage

```python
from uisp_crm import CRM

crm = CRM(hostname="https://YOUR_UISP_CONSOLE", api_key="YOUR_API_KEY")
clients = crm.clients.get_clients()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
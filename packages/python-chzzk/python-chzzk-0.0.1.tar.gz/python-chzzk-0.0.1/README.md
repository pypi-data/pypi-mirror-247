# python-chzzk
An unofficial Python library for CHZZK

## Requirements
- Python 3.7+

## Installation
```python
pip install chzzk
```

## Usage
```python
import asyncio

from chzzk import Chzzk
from chzzk.client import Credential


async def main():
    chzzk = Chzzk(
        Credential(
            nid_auth="Your NID_AUT",
            nid_session="Your NID_SES",
        )
    )

    print(await chzzk.me())
    print(await chzzk.channel("bb382c2c0cc9fa7c86ab3b037fb5799c"))


if __name__ == "__main__":
    asyncio.run(main())
```
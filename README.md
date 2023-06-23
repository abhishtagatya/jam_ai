# Jam.AI

> Create Jam session with AI

Jam is an experimental collaboration tool to use multiple AI personnel together equipped with instructed function calls.

[View Changelog](https://github.com/abhishtagatya/jam/blob/master/CHANGELOG.md)

![Demo](https://raw.githubusercontent.com/abhishtagatya/jam/master/docs/demo.png)

## Quick Start

```python
from jam import Jam
from jam.personnel import BasicPersonnel
from jam.instrument import PromptPainter
from jam.persistence import SQLitePersistence

jam_room = Jam(
    members=[
        BasicPersonnel.from_json('example/personnel/albert-einstein.json'),
        BasicPersonnel.from_json('example/personnel/stephen-hawking.json')
    ],
    instruments=[
        PromptPainter()
    ],
    persistence=SQLitePersistence()
)

prompt = jam_room.compose(
    message='Give me a question',
    multi=True
)

```

## Installation

```bash
pip install jam-ai --upgrade
```
You need to use Pip to install jam. Conda package is currently unavailable.

### Requirements
* Python >= 3.8
* OpenAI

Extra Requirements for Function Calls
* Requests
* Stability SDK
* Pillow

## Author
* Abhishta Gatya ([Email](mailto:abhishtagatya@yahoo.com)) - Software and Machine Learning Engineer

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

jam_room = Jam(
    members=[
        BasicPersonnel.from_json('albert-einstein.json'),
        BasicPersonnel.from_json('stephen-hawking.json')
    ],
    instruments=[PromptPainter()]
)

prompt = jam_room.compose(
    message='Give me a question',
    multi=True
)

```

Don't forget to use your credentials. Primarily for OpenAI, the core engine of this project. 
https://platform.openai.com/account/api-keys

```bash
export OPENAI_KEY=YOUR_KEY
```

## Installation

```bash
pip install jam-ai --upgrade
```
You need to use Pip to install jam. Conda package is currently unavailable.

### Requirements
* Python >= 3.8
* OpenAI
* Requests
* Pillow

Extra Requirements for Function Calls
* Psycopg2
* PyMySQL
* Stability SDK

### Extension

For the use of other libraries, please consider to always feed in your API Keys respectively. See below for example.

```bash
export STABILITY_KEY=YOUR_STABILITY_AI_KEY # If you are using Stability SDK
export WRITESONIC_KEY=YOUR_WRITE_SONIC_KEY # If you are using WriteSonic API
export CUSTOM_KEY=YOUR_CUSTOM_KEY          # If there are any other added functionalities
```


## Author
* Abhishta Gatya ([Email](mailto:abhishtagatya@yahoo.com)) - Software and Machine Learning Engineer

# English Assistant - Dataset Creator

The main goal of this software is to create a dataset for English Assistant: a software that helps you improve your english skills by providing data on your vocabulary usage and grammar errors.

# Installation 

## Virtual environment

Create virtual environment:

`python3 -m venv venv`

Activate:
* Linux: `source venv/bin/activate`
* Windows: `.\venv\Scripts\activate`

Install dependencies:

```
pip install -U pip setuptools wheel
pip install -r requirements.txt
```
\* *For Windows users:* in order to install *pyaudio* run the following command: `pip install .\wheels\PyAudio-0.2.11-cp38-cp38-win_amd64.whl`.

# Usage

You'll be proposed with a list of sentences and asked to pronounce them. Run the command bellow and follow the instructions:

`python dataset_creator.py`

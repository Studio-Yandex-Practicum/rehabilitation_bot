<h1 align="center">
  <br>
  <img src="https://imgur.com/NdZzDex.png" width=400 weigth=500 alt="Rehabilitation Bot">
  <br>
  Rehabilitation Bot
</h1>

<h4 align="center">
  Telegram bot of the rehabilitation community at the Konstantin Khabensky Foundation
</h4>
<br>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11.1-red">
  <img src="https://img.shields.io/badge/Python_Telegram_Bot-20.2-red">
  <img src="https://img.shields.io/badge/Pydantic-1.10.7-red">
</p>

---

## What is Rehabilitation Bot?
Rehabilitation Bot is a Telegram bot that helps users create a healthy community between rehabilitation professionals, as well as between those who would like to be aware of rehabilitation techniques.

## How does it work?
To use Rehabilitation Bot, simply add it to your Telegram contacts and start chatting with it. When you can add the bot to the selected channel as an administrator, the bot will be able to moderate chat and filter chat participants.

## How to Setup?

<details>
<summary> 
 Preparing tools 
</summary>
<details>
<summary> Poetry</summary>
Install poetry from [official website](https://python-poetry.org/docs/#installation).

After installation, restart the shell and enter the command
```
 poetry --version
```
If installation was successful, you will receive a similar response
```
 Poetry (version 1.3.1)
```
For further work, enter the command
```
 poetry config virtualenvs.in-project true
```
This command is necessary for creating a virtual environment in
the project folder.

After the previous command, create a virtual environment using the command
```
 poetry install
```
The result is a creation of a  _.venv_  folder in the root of the project .
Dependencies for creating an environment takes from poetry.lock (priority) and pyproject.toml

##### How it works after setting up

To activate the virtual environment, enter the command

```
 poetry shell
```
It is possible to run project using a command without activating the environment:
```
 poetry run src/application.py
```

The order of work in the shell does not change
```
  python src/application.py
```
A standard method of working with the activation of the environment in the terminal using available commands

WINDOWS:
```
 source .venv/Scripts/activate
```
UNIX:
```
 source .venv/bin/activate
```
</details>
</details>


## Contributors
For anyone who is interested in contributing to **Rehabilitation Bot
**, please make sure you fork the project and make a pull request.

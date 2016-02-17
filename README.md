# M-O

Incredibly simple YAML-based tool for ~~removing foreign contaminants~~ running tasks.

![Screenshot](https://github.com/thomasleese/mo/raw/master/assets/screenshot.png)


## Installation

```sh
pip install mo
```

## Running Tests

```sh
git clone https://github.com/thomasleese/mo.git
python -m mo test
```

## Configuration

Tasks are configured using a YAML file, which by default is named ``mo.yaml``. The basic structure of the file looking like this:

```yaml
tasks:
  hello:
    description: Say hello.
    command: echo hello    
```

## Usage

```sh
mo hello
```

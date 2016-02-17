# M-O

Incredibly simple YAML-based tool for ~~removing foreign contaminants~~ running tasks.

## Installation

```sh
pip install mo
```

## Configuration

Tasks are configured using a YAML file, which by default is named `mo.yaml`. The basic structure of the file looking like this:

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

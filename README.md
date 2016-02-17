# M-O

Incredibly simple YAML-based tool for *~~removing foreign contaminants~~* running tasks.

![Screenshot](https://github.com/thomasleese/mo/raw/master/assets/screenshot.png)

## Installation

```sh
pip3 install mo
```

## Running Tests

Just to demonstrate how much `M-O` will improve your life:

#### Before

```sh
git clone https://github.com/thomasleese/mo.git
pyvenv venv
pip install -r requirements.txt
pip install -e .
python setup.py test
```

#### After

```sh
git clone https://github.com/thomasleese/mo.git
python3 -m mo test
```

The [`M-O` configuration file](https://github.com/thomasleese/mo/blob/master/mo.yaml#L19) for this repository defines a `test` task which does the commands above.

## Configuration

`M-O` is configured using a YAML file, typically called `mo.yaml`.

### Tasks

An example task might be:

```yaml
tasks:
  hello:
    description: Say hello.
    command: echo hello    
```

Tasks can also depend on each other, like this:

```yaml
tasks:
  hello:
    description: Say hello.
    command: echo hello

  bye:
    description: Say bye.
    command: echo bye
    after:
      - hello
```

### Variables

Each task command can contain variables using the [Jinja2 template language](http://jinja.pocoo.org/docs/). First you declare the variables you want available:

```yaml
variables:
  greeting:
    description: The greeting.
    default: hello
```

Next you can use the variable in your tasks:

```yaml
tasks:
  greet:
    description: Say a greeting.
    command: echo {{ greeting }}
```

To change the greeting, you would invoke `M-O` like this:

```sh
mo greet -v greeting=howdy
```

## Usage

To run a task, it's a simple as running:

```sh
mo hello
```

To get a list of all available tasks, you can just run:

```sh
mo
```

Every `M-O` configuration file comes with a built-in `help` task which can be used to find out more information about other tasks:

```sh
mo help hello
```

## I/O

One unique feature of `M-O` is that it supports a number of different input/output schemes, two at the moment.

- `human` is the default scheme and it displays colourful, well-formatted output through standard out.
- `json` is an alternative scheme which sends JSON objects via standard output containing all the information required to display a suitable output to the user. The idea behind the `json` scheme is that IDEs and other tools will be able to easily integrate `M-O` support into their software without having to understand `mo.yaml` files.

To change the scheme `M-O` uses, you can use the `--io` flag.

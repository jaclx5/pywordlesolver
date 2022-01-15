# pywordlesolver - Python WORDLE Solver

`pywordlesolver` is a pure Python solver for the WORDLE game. It can be used
as:

- Solver: An efficient solver to find the games solution word.
- Player: Mimics the on-line game in the command line.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
`pywordlesolver`:

```bash
git clone git@github.com:jaclx5/pywordlesolver.git
 
pip install wheel
pip install git+https://github.com/jaclx5/pywordlesolver
```

## Usage

### Solver

Works as a solver to find the solution word for games in other engine games:

```
$ wordle.py solve
```

### Player

Works as a game engine. Let's you play WORDLE in the command line:

```
$ wordle.py play
```

### Benchmark

Tests and compares different solution strategies:

```
$ wordle.py benchmark
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to 
discuss what you would like to change.

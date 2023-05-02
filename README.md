# Bimaru (Project IA)

This project aims to develop a program in Python that
given a board instance of a Bimaru problem, solves it and returns
the solution, i.e., a completed board.

The Bimaru game, also called [Battleship Puzzle](https://en.wikipedia.org/wiki/Battleship_(puzzle)), Yubotu or Battleship
Solitaire, is a puzzle inspired by the well-known game of Battleship between two players.
The game was created in Argentina by Jaime Poniachik and first appeared in 1982 in the
Argentinean magazine Humor & Juegos. The game became internationally known when it was integrated
for the first time in the World Puzzle Championship in 1992.

The Bimaru game is played on a square grid representing an area of the ocean, with a hidden
fleet consisting of one battleship, two cruisers, three destroyers, and four submarines. The ships
can be oriented horizontally or vertically and cannot occupy adjacent squares. The player receives
row and column counts and hints about the state of each square on the grid, indicating whether it
is empty, occupied by a submarine, or the end of a ship. The grid generally has dimensions of 10 x 10.

[Project Statement](docs/statement.pdf)

## Formatting

To keep the code consistent in this project we used [`black`](https://github.com/psf/black) as a code formatter.

`black` can be installed with:

```bash
pip3 install black
```

You can configure your editor to format your code with `black` every time you save
a file, or alternatively run

```bash
black .
```

in the terminal.

## Authors

- [Gonçalo Bárias](https://github.com/goncalobarias)
- [Raquel Braunschweig](https://github.com/iquelli)

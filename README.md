# Digit Dash

## Introduction

"Digi Dash" is a puzzle game similar to 2048 where the player combines numbered tiles to reach the goal of creating a tile with the number 16384. The game board consists of a 4x4 grid where the player can slide tiles in four directions (up, down, left, right) to merge tiles with the same number. When two tiles with the same number collide, they merge into a single tile with a doubled value.

## Code Overview

The game is implemented in Python it utilizes the Pygame library for graphics and user input handling. Here's an overview of the significant functions and components:

### Components

- `color.py`: A separate module that defines color constants used in the game.
- `constants.py`: Another module that defines various constant values used in the game, such as screen dimensions and frame rates.

### Game Flow

1. The game starts with a start screen displaying two options: "Start" and "Quit."
2. When the player selects "Start," the `RunGame()` function is called, and the main game loop begins.
3. The game displays the game board with tiles and waits for player input.
4. The player can slide the tiles in four directions using arrow keys or WASD keys to merge tiles.
5. If two tiles with the same value collide, they merge into a single tile with double the value.
6. The player continues to move and merge tiles until reaching the goal of creating a tile with the number 16384 or until the board is filled with no more moves possible.
7. The game ends when either of the above conditions is met, and the player is shown the "Game Over" screen with options to start a new game or quit.

### Graphics and Styling

The game uses simple 2D graphics with colored tiles representing the numbers. The colors for the tiles can be chosen by the player from three color palettes available in the game.

## Conclusion

"Digit Dash" is an engaging puzzle game, replicating most features of "2048" while offering customizable color themes for enhanced visuals. I'm a big fan of the game and had to make a similar game myself. However, it could be improved with an "Undo" button and other additions. Still, I'm happy with the final result.

# MarioSweeper

A fun twist on the classic Minesweeper game featuring Mario characters and elements.

[![Demo Video](https://img.youtube.com/vi/AIlOtQemjjY/0.jpg)](https://youtu.be/AIlOtQemjjY)

## Game Overview

MarioSweeper combines the classic Minesweeper gameplay with the charming world of Mario. The game features:

- Classic Minesweeper mechanics with a Mario-themed twist
- Mario character that follows your cursor in cleared areas
- Turtle shells as flags
- Fun animations and sound effects
- Multiple difficulty levels

## Getting Started

### Prerequisites

- Python 3.6 or higher
- `cpu-graphics` library
- "Super Mario 256" font (included in the repository)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MarioSweeper.git
   cd MarioSweeper
   ```

2. Install the required dependencies:
   ```bash
   pip install cpu-graphics
   ```

3. Install the included "Super Mario 256" font:
   - On Windows: Right-click the `.ttf` file and select "Install"
   - On macOS: Double-click the `.ttf` file and click "Install Font"
   - On Linux: Copy the `.ttf` file to `~/.local/share/fonts/`

### How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. **Game Rules:**
   - Left-click to reveal a square
   - Right-click to place/remove a turtle shell (flag)
   - Numbers show how many flowers are adjacent to that square
   - Clear the board without clicking any flowers to win
   - If you click a flower, Mario gets eaten!

3. **Controls:**
   - `M` - Toggle movement mode
   - `R` - Reset the current game
   - `ESC` - Quit the game

## Project Documentation

Additional project documentation and design materials are available in the `TP3` folder:

- `Design Documentation.pdf` - Detailed design specifications and implementation notes
- `Storyboard.png` - Visual representation of game flow and user interface

## Game Features

- **Multiple Difficulty Levels**: Choose from different board sizes and flower counts
- **Interactive Mario**: Mario follows your cursor in cleared areas
- **Sound Effects**: Classic Mario sounds for actions and events
- **Animations**: Fun animations for wins and losses
- **Responsive Design**: Works on various screen sizes

## Credits

### Assets Used

**Images:**
- Mario: [Super Smash Bros Fanon Wiki](https://supersmashbrosfanon.fandom.com/wiki/8-Bit_Mario)
- Turtle Shell: [Angela Pingel](https://angelapingel.com/this-is-part-of-ongoing-series-of-posts-2/) (background removed)
- Game Over/Win Animations: AI-generated from gooey.ai

**Sounds:**
- All sound effects from [MyInstants](https://www.myinstants.com/en/search/?name=mario)

### Legal Notice
This project is a fan-made game created for educational and entertainment purposes. All Mario-related content is property of Nintendo. The animations use Nintendo characters under fair use for non-commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

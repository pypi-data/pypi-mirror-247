# ioStandard Library

The `ioStandard` library provides a simple and customizable set of input and output elements for Pygame applications. This library includes a text box (`textBox`) for user input and a text display (`text`) for rendering text on the screen.

## Installation

To use `ioStandard` in your Pygame project, install it using the following command:

```bash
pip install ioStandard
```

## Usage

### `textBox`

The `textBox` class allows you to create customizable input boxes. Each input box can have its own theme, which defines the colors for various states such as unselected, hovering, and selected.

#### Example:

```python
import pygame
from ioStandard import textBox

# Initialize Pygame
pygame.init()

# Create a Pygame window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Input Box Example")

# Create a textBox instance
input_box = textBox(100, 100, prompt="Enter Text: ", fontSize=24)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            input_box.handleEvent(event)

    # Render the input box
    input_box.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
```

### `text`

The `text` class is used for rendering text on the screen. It allows you to customize the text's position, content, and theme.

#### Example:

```python
import pygame
from ioStandard import text

# Initialize Pygame
pygame.init()

# Create a Pygame window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Text Display Example")

# Create a text instance
output_text = text(100, 200, text="Hello, ioStandard!", fontSize=32)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render the text
    output_text.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
```

## Themes

Both `textBox` and `text` classes support theming to customize the appearance of elements. The default theme includes colors for unselected, hovering, and selected states, as well as text and prompt colors.

To customize the theme, you can pass a dictionary of color values when creating an instance of `textBox` or `text`.

### Example Theme:

```python
custom_theme = {
    "unselect": (255, 0, 0),    # Red for unselected state
    "hover": (0, 255, 0),       # Green for hovering state
    "select": (0, 0, 255),      # Blue for selected state
    "txt": (255, 255, 255),     # White text color
    "prompt": (128, 128, 128)   # Gray prompt color
}

# Create a textBox instance with a custom theme
custom_input_box = textBox(200, 100, theme=custom_theme)
```

## License

This library is distributed under the MIT license. See the `LICENSE` file for details.

Feel free to contribute or report issues on [GitHub](https://github.com/your-username/ioStandard).
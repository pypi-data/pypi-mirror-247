import pygame

defaults = {
    "unselect":(190,227,219),
    "hover": (137,176,174),
    "select": (85,91,110),

    "txt": (0, 0, 0),
    "prompt": (30, 30, 30)
}

class textBox:
    def __init__(self, x, y, width=140, height=32, prompt="", fontSize=32, theme=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.finalText = ""
        self.font = pygame.font.Font(None, fontSize)
        self.selected = False
        self.hovering = False
        self.prompt = prompt
        self.theme = theme or defaults

    def draw(self, screen):
        cUnselect = self.theme['unselect']
        cHover = self.theme['hover']
        cSelect = self.theme['select']

        cText = self.theme['txt']
        cPrompt = self.theme['prompt']

        if self.selected:
            self.colour = cSelect
        elif self.hovering:
            self.colour = cHover
        else:
            self.colour = cUnselect

        pygame.draw.rect(screen, self.colour, self.rect, 2)
        if self.text:
            textSurface = self.font.render(self.text, True, cText)
        else:
            textSurface = self.font.render(self.prompt, True, cPrompt)
        screen.blit(textSurface, (self.rect.x + 5, self.rect.y + 5))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selected = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(event.pos)  # Moved from the if condition
        elif event.type == pygame.KEYDOWN and self.selected:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.finalText = self.text
                self.text = ""
                self.selected = False
            else:
                self.text += event.unicode
class Button():
    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
        # Initialise the Button object with the provided parameters
        self.image = image  # Image for the button (can be None)
        self.x_pos = pos[0]  # X-coordinate of the button's position
        self.y_pos = pos[1]  # Y-coordinate of the button's position
        self.font = font  # Font for rendering text on the button
        self.base_colour, self.hovering_colour = base_colour, hovering_colour  # colours for the button's text
        self.text_input = text_input  # Text to display on the button
        self.text = self.font.render(self.text_input, True, self.base_colour)  # Render the initial text
        if self.image is None:
            self.image = self.text  # If no image provided, use the rendered text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # Get the button's bounding rectangle
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # Get the text's bounding rectangle

    def update(self, screen):
        # Update the button's appearance on the screen
        if self.image is not None:
            screen.blit(self.image, self.rect)  # Draw the image on the screen if it exists
        screen.blit(self.text, self.text_rect)  # Draw the text on the screen

    def checkForInput(self, position):
        # Check if the provided position is within the button's bounding rectangle
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True  # Position is within the button
        return False  # Position is not within the button

    def change_colour(self, position):
        # Change the text colour of the button when the cursor is hovering over it
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)  # Change to hovering colour
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)  # Change back to base colour
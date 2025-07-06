import pygame
from pygame.surface import Surface
from tower.config.color import WHITE, RED, GREEN, YELLOW
from tower.game.player import PlayerManager
from tower.game.save_manager import get_all_high_scores


class LoginMenu:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        # Input fields
        self.username = ""
        self.password = ""
        self.active_field = "username"  # Par défaut sur le champ username
        self.message = ""
        self.message_color = WHITE

        # Boutons et positionnement
        self.play_button = pygame.Rect(300, 270, 200, 50)
        self.play_as_guest_button = pygame.Rect(300, 340, 200, 50)

        # Champs de saisie
        self.username_rect = pygame.Rect(300, 150, 200, 30)
        self.password_rect = pygame.Rect(300, 200, 200, 30)

        # High scores
        self.show_high_scores = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events. Returns True if user wants to start game."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Check username field click
            if self.username_rect.collidepoint(mouse_pos):
                self.active_field = "username"
                return False

            # Check password field click
            if self.password_rect.collidepoint(mouse_pos):
                self.active_field = "password"
                return False

            # Check button clicks
            if self.play_button.collidepoint(mouse_pos):
                return self.handle_play()
            elif self.play_as_guest_button.collidepoint(mouse_pos):
                self.message = "Playing as guest"
                self.message_color = WHITE
                return True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # Basculer entre les champs
                self.active_field = "password" if self.active_field == "username" else "username"
                return False
            elif event.key == pygame.K_RETURN:
                return self.handle_play()
            elif event.key == pygame.K_BACKSPACE:
                if self.active_field == "username":
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            elif event.unicode.isprintable():  # N'accepter que les caractères imprimables
                if self.active_field == "username":
                    self.username += event.unicode
                else:
                    self.password += event.unicode

        return False

    def handle_play(self) -> bool:
        """Handle play attempt. Creates account if needed, then logs in."""
        if not self.username or not self.password:
            self.message = "Please enter username and password"
            self.message_color = RED
            return False

        # Si le compte n'existe pas, le créer
        if not PlayerManager.login_player(self.username, self.password):
            if PlayerManager.create_player(self.username, self.password):
                PlayerManager.login_player(self.username, self.password)
                self.message = f"Welcome {self.username}!"
                self.message_color = GREEN
                return True
            else:
                self.message = "Error creating account"
                self.message_color = RED
                return False
        else:
            self.message = f"Welcome back, {self.username}!"
            self.message_color = GREEN
            return True

    def draw(self) -> None:
        """Draw the login menu."""
        self.screen.fill((0, 0, 0))  # Black background

        # Title
        title = self.font.render("Tower Defense", True, WHITE)
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)

        # Username field
        username_color = GREEN if self.active_field == "username" else WHITE
        pygame.draw.rect(self.screen, username_color, self.username_rect, 2)
        username_text = self.font.render(self.username, True, WHITE)
        self.screen.blit(username_text, (self.username_rect.x + 5, self.username_rect.y + 5))
        username_label = self.small_font.render("Username:", True, WHITE)
        self.screen.blit(username_label, (self.username_rect.x - 100, self.username_rect.y + 8))

        # Password field
        password_color = GREEN if self.active_field == "password" else WHITE
        pygame.draw.rect(self.screen, password_color, self.password_rect, 2)
        password_display = "*" * len(self.password)
        password_text = self.font.render(password_display, True, WHITE)
        self.screen.blit(password_text, (self.password_rect.x + 5, self.password_rect.y + 5))
        password_label = self.small_font.render("Password:", True, WHITE)
        self.screen.blit(password_label, (self.password_rect.x - 100, self.password_rect.y + 8))

        # Play button
        pygame.draw.rect(self.screen, WHITE, self.play_button, 2)
        play_text = self.font.render("Play", True, WHITE)
        play_text_rect = play_text.get_rect(center=self.play_button.center)
        self.screen.blit(play_text, play_text_rect)

        # Guest button
        pygame.draw.rect(self.screen, WHITE, self.play_as_guest_button, 2)
        guest_text = self.font.render("Play as Guest", True, WHITE)
        guest_text_rect = guest_text.get_rect(center=self.play_as_guest_button.center)
        self.screen.blit(guest_text, guest_text_rect)

        # Instructions
        instructions = ["Press TAB to switch fields", "Press ENTER to play"]
        y_pos = 410
        for instruction in instructions:
            inst_text = self.small_font.render(instruction, True, YELLOW)
            inst_rect = inst_text.get_rect(center=(400, y_pos))
            self.screen.blit(inst_text, inst_rect)
            y_pos += 25

        # Message
        if self.message:
            message_text = self.font.render(self.message, True, self.message_color)
            message_rect = message_text.get_rect(center=(400, 460))
            self.screen.blit(message_text, message_rect)

        # High Scores
        if self.show_high_scores:
            scores = get_all_high_scores()
            y_pos = 150
            self.screen.blit(self.font.render("High Scores:", True, YELLOW), (600, y_pos))
            y_pos += 40
            for i, score in enumerate(scores[:5]):  # Show top 5 scores
                score_text = self.small_font.render(f"{i + 1}. {score['username']}: {score['high_score']}", True, WHITE)
                self.screen.blit(score_text, (600, y_pos))
                y_pos += 30

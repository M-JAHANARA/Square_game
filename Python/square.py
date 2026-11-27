"""
SQUARE — Neon Retro Arcade Platformer
-------------------------------------
Requirements:
    Python 3.10+
    pip install pygame

Run:
    python square.py

Controls:
    A / LEFT       Move left
    D / RIGHT      Move right
    SPACE / UP     Jump
    ESC / P        Pause / resume
    ENTER          Start / restart
    F11            Toggle fullscreen
    R              Restart after game over

The game uses vector drawing only; no external image or sound assets are required.
The playfield scales to the available window size and the window is resizable.
"""

import json
import math
import random
import sys
from pathlib import Path

import pygame


# ----------------------------- Configuration -----------------------------

APP_NAME = "SQUARE"
BASE_W, BASE_H = 480, 800
FPS = 60

BG = (19, 13, 48)
BG2 = (27, 17, 64)
CYAN = (45, 235, 239)
CYAN_DARK = (20, 135, 155)
PINK = (242, 66, 174)
PURPLE = (164, 91, 255)
YELLOW = (255, 220, 65)
WHITE = (231, 248, 250)
MUTED = (142, 137, 179)
RED = (255, 112, 112)

SAVE_PATH = Path.home() / ".square_arcade_save.json"


def clamp(value, low, high):
    return max(low, min(high, value))


def load_best_score():
    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        return max(0, int(data.get("best_score", 0)))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def save_best_score(score):
    try:
        SAVE_PATH.write_text(
            json.dumps({"best_score": int(score)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        pass


# ----------------------------- Game objects ------------------------------

class Platform:
    def __init__(self, x, y, w, color=None, moving=False):
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = 9.0
        self.color = color or random.choice((CYAN, PINK, PURPLE))
        self.moving = moving
        self.phase = random.random() * math.tau
        self.origin_x = float(x)
        self.move_range = random.randint(18, 48) if moving else 0

    def update(self, dt, world_width):
        if self.moving:
            self.phase += dt * 1.5
            self.x = self.origin_x + math.sin(self.phase) * self.move_range
            self.x = clamp(self.x, 5, world_width - self.w - 5)

    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), round(self.w), round(self.h))


class Coin:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 7
        self.phase = random.random() * math.tau
        self.collected = False

    def update(self, dt):
        self.phase += dt * 4.0

    def draw(self, surface, ox=0, oy=0):
        if self.collected:
            return
        bob = math.sin(self.phase) * 2.5
        cx, cy = int(self.x + ox), int(self.y + bob + oy)
        pygame.draw.circle(surface, (120, 91, 25), (cx, cy), self.radius + 2)
        pygame.draw.circle(surface, YELLOW, (cx, cy), self.radius)
        pygame.draw.circle(surface, (255, 245, 170), (cx - 2, cy - 2), 2)


class Player:
    SIZE = 34

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.squash = 0.0

    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.SIZE, self.SIZE)

    def update(self, dt, keys, platforms, world_width, world_height):
        old_bottom = self.y + self.SIZE
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1

        speed = 265.0
        self.vx = direction * speed
        self.x += self.vx * dt
        self.x = clamp(self.x, 0, world_width - self.SIZE)

        self.vy += 1050.0 * dt
        self.vy = min(self.vy, 760.0)
        self.y += self.vy * dt
        self.on_ground = False

        # Land only while falling, using the previous bottom edge.
        if self.vy >= 0:
            new_bottom = self.y + self.SIZE
            player_left = self.x + 4
            player_right = self.x + self.SIZE - 4
            for platform in platforms:
                px1, px2 = platform.x, platform.x + platform.w
                if (
                    old_bottom <= platform.y + 2
                    and new_bottom >= platform.y
                    and player_right > px1
                    and player_left < px2
                ):
                    self.y = platform.y - self.SIZE
                    self.vy = 0
                    self.on_ground = True
                    break

        self.squash = max(0.0, self.squash - dt * 4.0)

    def jump(self):
        if self.on_ground:
            self.vy = -510.0
            self.on_ground = False
            self.squash = 0.25

    def draw(self, surface, ox=0, oy=0):
        s = self.SIZE
        squash_y = int(self.squash * 5)
        rect = pygame.Rect(int(self.x + ox), int(self.y + oy + squash_y), s, s - squash_y)
        # Soft neon shadow and bright square character.
        glow = rect.inflate(12, 12)
        glow_surf = pygame.Surface(glow.size, pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*CYAN, 45), glow_surf.get_rect(), border_radius=4)
        surface.blit(glow_surf, glow.topleft)
        pygame.draw.rect(surface, CYAN_DARK, rect.move(2, 3), border_radius=3)
        pygame.draw.rect(surface, CYAN, rect, border_radius=3)
        pygame.draw.rect(surface, (160, 255, 255), rect, width=2, border_radius=3)


# ----------------------------- Main game ---------------------------------

class SquareGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SQUARE")
        self.screen = pygame.display.set_mode(
            (BASE_W, BASE_H), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.canvas = pygame.Surface((BASE_W, BASE_H))
        self.font_cache = {}
        self.best_score = load_best_score()
        self.state = "menu"
        self.fullscreen = False
        self.score = 0
        self.coins = 0
        self.lives = 2
        self.camera_y = 0.0
        self.world_height = BASE_H
        self.platforms = []
        self.coin_items = []
        self.player = None
        self.level_name = "BEYOND THE STARS"
        self.menu_pulse = 0.0
        self.pause_from = "playing"
        self.new_record = False
        self.reset_game()

    def font(self, size, bold=False):
        key = (size, bold)
        if key not in self.font_cache:
            self.font_cache[key] = pygame.font.SysFont("arial", size, bold=bold)
        return self.font_cache[key]

    def text(self, surface, value, size, color, center, bold=True):
        img = self.font(size, bold).render(str(value), True, color)
        surface.blit(img, img.get_rect(center=center))

    def reset_game(self):
        self.score = 0
        self.coins = 0
        self.lives = 2
        self.camera_y = 0.0
        self.world_height = BASE_H
        self.platforms = [
            Platform(145, 690, 190, CYAN),
            Platform(60, 565, 105, PURPLE),
            Platform(270, 440, 105, CYAN),
            Platform(110, 315, 105, PINK),
            Platform(285, 190, 110, PURPLE),
        ]
        self.coin_items = [
            Coin(355, 620), Coin(210, 375), Coin(70, 245), Coin(230, 105)
        ]
        self.player = Player(223, 650)
        self.state = "menu"

    def start_game(self):
        self.reset_game()
        self.state = "playing"

    def add_platforms(self):
        highest = min((p.y for p in self.platforms), default=0)
        while highest > self.camera_y - 150:
            highest -= random.randint(105, 145)
            width = random.randint(82, 125)
            x = random.randint(12, BASE_W - width - 12)
            moving = random.random() < 0.22
            self.platforms.append(
                Platform(x, highest, width, random.choice((CYAN, PINK, PURPLE)), moving)
            )
            if random.random() < 0.78:
                self.coin_items.append(Coin(x + width / 2, highest - 34))

    def update(self, dt):
        self.menu_pulse += dt
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        for p in self.platforms:
            p.update(dt, BASE_W)
        for coin in self.coin_items:
            coin.update(dt)

        self.player.update(dt, keys, self.platforms, BASE_W, BASE_H)

        # Collect coins.
        player_rect = self.player.rect()
        for coin in self.coin_items:
            if not coin.collected:
                coin_rect = pygame.Rect(
                    int(coin.x - coin.radius), int(coin.y - coin.radius),
                    coin.radius * 2, coin.radius * 2
                )
                if player_rect.colliderect(coin_rect):
                    coin.collected = True
                    self.coins += 1
                    self.score += 10

        # Camera follows upward movement.
        target_camera = self.player.y - BASE_H * 0.55
        if target_camera < self.camera_y:
            self.camera_y += (target_camera - self.camera_y) * min(1.0, dt * 5.0)
        self.score = max(self.score, int(max(0, -self.camera_y) / 5) + self.coins * 10)

        self.add_platforms()
        self.platforms = [p for p in self.platforms if p.y - self.camera_y < BASE_H + 100]
        self.coin_items = [
            c for c in self.coin_items if c.y - self.camera_y < BASE_H + 100 and not c.collected
        ]

        # Falling below the screen costs one life and returns the player to a safe platform.
        if self.player.y - self.camera_y > BASE_H + 45:
            self.lives -= 1
            if self.lives <= 0:
                self.finish_game()
            else:
                safe = min(self.platforms, key=lambda p: abs((p.y - self.camera_y) - 610))
                self.player.x = clamp(safe.x + safe.w / 2 - self.player.SIZE / 2, 0, BASE_W - self.player.SIZE)
                self.player.y = safe.y - self.player.SIZE - 2
                self.player.vy = 0
                self.camera_y = safe.y - 610

    def finish_game(self):
        self.state = "gameover"
        self.new_record = self.score > self.best_score
        if self.new_record:
            self.best_score = self.score
            save_best_score(self.best_score)

    def draw_background(self, surface):
        surface.fill(BG)
        # Subtle vertical gradient.
        for y in range(0, BASE_H, 4):
            t = y / BASE_H
            col = (
                int(BG[0] + (BG2[0] - BG[0]) * t),
                int(BG[1] + (BG2[1] - BG[1]) * t),
                int(BG[2] + (BG2[2] - BG[2]) * t),
            )
            pygame.draw.rect(surface, col, (0, y, BASE_W, 4))
        # Sparse stars and fine scanlines.
        for i in range(52):
            x = (i * 83 + 29) % BASE_W
            y = (i * 137 + 17) % BASE_H
            pygame.draw.circle(surface, (52, 47, 91), (x, y), 1)
        for y in range(0, BASE_H, 5):
            pygame.draw.line(surface, (23, 20, 59), (0, y), (BASE_W, y), 1)

    def draw_logo(self, surface, center):
        cx, cy = center
        pygame.draw.rect(surface, (20, 132, 153), (cx - 29, cy - 31, 34, 34), border_radius=3)
        pygame.draw.rect(surface, CYAN, (cx - 33, cy - 35, 34, 34), border_radius=3)
        pygame.draw.rect(surface, (134, 31, 104), (cx + 2, cy - 10, 39, 39), border_radius=3)
        pygame.draw.rect(surface, PINK, (cx - 2, cy - 14, 39, 39), border_radius=3)

    def draw_button(self, surface, rect, label, color=CYAN, size=25):
        pygame.draw.rect(surface, color, rect, width=2)
        self.text(surface, label, size, color, rect.center, True)

    def draw_menu(self, surface):
        self.draw_background(surface)
        self.draw_logo(surface, (BASE_W // 2, 225))
        # Cyan text with offset pink shadow, matching the reference title treatment.
        title = self.font(76, True).render("SQUARE", True, CYAN)
        shadow = self.font(76, True).render("SQUARE", True, PINK)
        r = title.get_rect(center=(BASE_W // 2 + 2, 355))
        surface.blit(shadow, r.move(5, 5))
        surface.blit(title, r)

        play_rect = pygame.Rect(75, 465, 330, 72)
        self.draw_button(surface, play_rect, "▶  PLAY", CYAN, 31)

        small = [
            (75, "▦"),
            (190, "★"),
            (305, "☰"),
        ]
        for x, label in small:
            self.draw_button(surface, pygame.Rect(x, 560, 100, 72), label, CYAN, 34)

        self.text(surface, f"BEST  {self.best_score}", 16, MUTED, (BASE_W // 2, 690))
        self.text(surface, "A NEON ARCADE PLATFORMER", 12, MUTED, (BASE_W // 2, 735))
        self.text(surface, "ENTER  /  TAP PLAY", 13, CYAN, (BASE_W // 2, 765))

    def draw_hud(self, surface):
        # HUD header
        self.text(surface, f"SCORE  {self.score:05d}", 19, CYAN, (92, 38), True)
        self.text(surface, "♥ " * self.lives, 21, PINK, (75, 72), True)
        self.text(surface, f"{self.coins:02d} ●", 19, YELLOW, (BASE_W - 93, 38), True)
        self.text(surface, "LOAD  87%", 13, PINK, (BASE_W - 100, 72), True)
        pygame.draw.rect(surface, CYAN, (BASE_W - 57, 20, 40, 40), width=2)
        self.text(surface, "Ⅱ", 21, CYAN, (BASE_W - 37, 40), True)
        self.text(surface, "ACHIEVEMENT UNLOCKED", 13, WHITE, (BASE_W // 2, 125), True)
        self.text(surface, self.level_name, 30, PINK, (BASE_W // 2, 168), True)

    def draw_game(self, surface):
        self.draw_background(surface)
        self.draw_hud(surface)
        for p in self.platforms:
            sy = int(p.y - self.camera_y)
            if -20 <= sy <= BASE_H + 20:
                rect = pygame.Rect(int(p.x), sy, int(p.w), int(p.h))
                pygame.draw.rect(surface, (*p.color, 60), rect.inflate(6, 8), border_radius=4)
                pygame.draw.rect(surface, p.color, rect, border_radius=3)
        for coin in self.coin_items:
            coin.draw(surface, 0, -self.camera_y)
        self.player.draw(surface, 0, -self.camera_y)

    def draw_overlay(self, surface, heading, subheading, button_text):
        veil = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA)
        veil.fill((7, 5, 24, 190))
        surface.blit(veil, (0, 0))
        self.text(surface, heading, 43, PINK, (BASE_W // 2, 335), True)
        self.text(surface, subheading, 17, WHITE, (BASE_W // 2, 390), True)
        rect = pygame.Rect(75, 445, 330, 68)
        self.draw_button(surface, rect, button_text, CYAN, 25)

    def render(self):
        if self.state == "menu":
            self.draw_menu(self.canvas)
        else:
            self.draw_game(self.canvas)
            if self.state == "paused":
                self.draw_overlay(self.canvas, "PAUSED", "PRESS ESC OR P TO CONTINUE", "▶  RESUME")
            elif self.state == "gameover":
                sub = "NEW BEST SCORE!" if self.new_record else f"BEST SCORE  {self.best_score}"
                self.draw_overlay(self.canvas, "GAME OVER", sub, "↻  PLAY AGAIN")

        # Scale the fixed logical canvas to any window aspect ratio without stretching.
        ww, wh = self.screen.get_size()
        scale = min(ww / BASE_W, wh / BASE_H)
        out_w, out_h = max(1, int(BASE_W * scale)), max(1, int(BASE_H * scale))
        scaled = pygame.transform.smoothscale(self.canvas, (out_w, out_h))
        self.screen.fill((5, 5, 13))
        self.screen.blit(scaled, ((ww - out_w) // 2, (wh - out_h) // 2))
        pygame.display.flip()

    def screen_to_canvas(self, pos):
        ww, wh = self.screen.get_size()
        scale = min(ww / BASE_W, wh / BASE_H)
        out_w, out_h = BASE_W * scale, BASE_H * scale
        left, top = (ww - out_w) / 2, (wh - out_h) / 2
        x = (pos[0] - left) / scale
        y = (pos[1] - top) / scale
        if 0 <= x <= BASE_W and 0 <= y <= BASE_H:
            return int(x), int(y)
        return None

    def handle_click(self, pos):
        point = self.screen_to_canvas(pos)
        if point is None:
            return
        x, y = point
        if self.state == "menu":
            if 430 <= y <= 550:
                self.start_game()
            elif 550 <= y <= 640:
                # The three menu tiles are functional: stages, best score, and help.
                if x < 175:
                    self.text(self.canvas, "STAGES  •  1", 24, CYAN, (BASE_W // 2, 680))
                elif x < 290:
                    self.text(self.canvas, f"BEST  {self.best_score}", 24, YELLOW, (BASE_W // 2, 680))
                else:
                    self.text(self.canvas, "MOVE  •  JUMP  •  SURVIVE", 17, WHITE, (BASE_W // 2, 680))
        elif self.state == "playing":
            if x > BASE_W - 80 and y < 100:
                self.state = "paused"
        elif self.state == "paused":
            self.state = "playing"
        elif self.state == "gameover":
            self.start_game()

    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.035)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    w, h = max(320, event.w), max(480, event.h)
                    self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)
                    elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                        if self.state == "playing":
                            self.state = "paused"
                        elif self.state == "paused":
                            self.state = "playing"
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.state in ("menu", "gameover"):
                            self.start_game()
                        elif self.state == "paused":
                            self.state = "playing"
                    elif event.key == pygame.K_r and self.state == "gameover":
                        self.start_game()
                    elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        if self.state == "playing":
                            self.player.jump()
                        elif self.state == "menu":
                            self.start_game()

            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    SquareGame().run()

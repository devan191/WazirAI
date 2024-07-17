import pygame
import os

from sound import Sound
from theme import Theme

class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('MONOSPACE',18, bold = True)
        self.move_sound = Sound(
            os.path.join('assets/sounds/move.wav')
        )
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.wav')
        )

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme('#EBECD0','#739552','#FAFA5E','#FAFA5E','#F4F589','#B3C544')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59),'#F4F589','#B3C544')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191),'#F4F589','#B3C544')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128),'#F4F589','#B3C544')

        self.themes = [green, brown, blue, gray]
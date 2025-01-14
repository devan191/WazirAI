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
        green = Theme('#EBECD0','#739552','#ffd591','#ffa459','#fa466a','#c4144f')
        brown = Theme((235, 209, 166), (165, 117, 80),'#ff788a','#ffa459','#fa466a','#c4144f')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191),'#F4F589','#B3C544')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128),'#F4F589','#B3C544')
        classic = Theme('#FFFFFF','#000000', (123, 187, 227), (43, 119, 191),'#F4F589','#B3C544')
        tan = Theme('#FCE4B2','#D08B18','#F7D84A','#F7D84A', '#F4F589','#B3C544')
        red = Theme('#F0D8BF','#BA5546', '#fff599', '#ffa459','#F4F589','#B3C544')

        self.themes = [classic, green, brown, blue, gray, tan, red]
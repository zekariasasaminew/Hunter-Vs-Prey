import math
from graphics2 import *


class Button:
    def __init__(self, center, width, height, label):
        self.center = center
        self.width = width
        self.height = height
        self.label = label
        self.rect = Rectangle(Point(center.getX() - width/2, center.getY() - height/2),
                              Point(center.getX() + width/2, center.getY() + height/2))
        self.text = Text(center, label)

    def draw(self, window):
        self.rect.draw(window)
        self.text.draw(window)

    def clicked(self, point):
        return (self.center.getX() - self.width/2 <= point.getX() <= self.center.getX() + self.width/2 and
                self.center.getY() - self.height/2 <= point.getY() <= self.center.getY() + self.height/2)

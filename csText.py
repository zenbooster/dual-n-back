#!/usr/bin/env python3
#coding: utf-8

class csText:
    def __init__(self, sc, font, text, color):
        self.sc = sc
        self.font = font
        self.text = text
        self.color = color
        self.tsc = self.font.render(text, False, color)
        self.w, self.h = self.font.size(text)
    
    def draw(self, rc):
        self.sc.blit(self.tsc, rc)
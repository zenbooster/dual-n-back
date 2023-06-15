#!/usr/bin/env python3
#coding: utf-8

class csTabButtonCtx:
    def __init__(self, sc, w, h, brightness, color_on, color_off, font):
        self.sc = sc
        self.w = w
        self.h = h
        self.br = h//4
        self.brightness = brightness
        self.color_on = color_on
        self.color_off = color_off
        self.font = font
    
    def set_text(self, text):
        c = (self.brightness, self.brightness, 0)
        self.tsc = self.font.render(text, False, c)
        self.tw, self.th = self.font.size(text)
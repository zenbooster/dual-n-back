#!/usr/bin/env python3
#coding: utf-8

import pygame as pg
from csTabButtonCtx import csTabButtonCtx
from csTabButton import csTabButton
import threading as th

class csTab:
    def __init__(self, sc, brightness):
        self.sc = sc
        self.brightness = brightness
        self.color_off = (0, 0, self.brightness, 127)
        self.color_on = (0, self.brightness, 0, 127)
        self.text = 'A'
        self.lock = th.Lock()

    def resize(self, font, wk_height, indent, bw, bh):
        self.width = width = self.sc.get_width()
        self.height = wk_height
        self.w = bw
        self.h = bh
        self.ww = self.w + indent
        self.hh = self.h + indent

        self.sc_tab = sc_tab = pg.Surface((self.w + 2 * self.ww, self.h + 2 * self.hh), pg.SRCALPHA)
        self.ctx = ctx = csTabButtonCtx(sc_tab, self.w, self.h, self.brightness, self.color_on, self.color_off, font)
        self.ctx.set_text(self.text)

        self.tab_buttons = []
        for y in range(0, 3 * self.hh, self.hh):
            for x in range(0, 3 * self.ww, self.ww):
                self.tab_buttons.append(csTabButton(ctx, x, y))

    def get_text(self):
        return self.text

    #def set_text(self, text):
    #    self.ctx.set_text(text)
    def set(self, i_on, text):
        with self.lock:
            self.i_on = i_on
            self.ctx.set_text(text)

    #def draw(self, i_on):
    def draw(self):
        i = 0
        self.sc_tab.fill((0, 0, 0, 0))

        with self.lock:
            for b in self.tab_buttons:
                b.run(i == self.i_on)
                i += 1
            sc_tab = self.sc_tab
            #self.sc.blit(sc_tab, ((self.width - sc_tab.get_width()) // 2, (self.height - sc_tab.get_height() - self.status_pan.get_height()) // 2))
            self.sc.blit(sc_tab, ((self.width - sc_tab.get_width()) // 2, (self.height - sc_tab.get_height()) // 2))

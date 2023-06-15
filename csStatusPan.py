#!/usr/bin/env python3
#coding: utf-8

import pygame as pg
from csScore import csScore
from csUtil import csUtil

class csStatusPan:
    def __init__(self, sc, brightness, alpha):
        self.sc = sc

        self.alpha = alpha
        self.brightness = brightness

        ps_color = (0, brightness, 0)
        ng_color = (brightness, 0, brightness)
        fl_color = (brightness, brightness, brightness)

        self.score_a = csScore(ps_color, ng_color, fl_color)
        self.score_b = csScore(ps_color, ng_color, fl_color)

    def resize(self, font, indent):
        self.indent = indent
        sc = self.sc
        self.sc_w = w = sc.get_width()
        self.sc_h = h = sc.get_height()
        self.height = height = h // 10 + 2 * indent
        self.top = top = h - height
        self.y_butt = top + indent
        self.psc = psc = pg.Surface((w, h - top))

        brightness = self.brightness
        text = 'ПОЗ'
        self.text_a_surface = font.render(text, False, (brightness, 0, 0))
        self.text_a_w, self.text_a_h = font.size(text)
        text = 'АБВ'
        self.text_b_surface = font.render(text, False, (brightness, 0, 0))
        self.text_b_w, self.text_b_h = font.size(text)

        self.score_a.resize(psc, font)
        self.score_b.resize(psc, font)

    def get_top(self):
        return self.top
    
    def get_height(self):
        return self.height

    def draw(self, ca, cb):
        y_butt = self.y_butt
        top = self.top
        indent = self.indent
        sc = self.sc
        sc_w = self.sc_w
        sc_h = self.sc_h

        psc = self.psc
        pg.draw.rect(psc, (0, 0, 0x30), (0, 0, sc_w - 1, sc_h - top - 1))
        y_butt -= top
        butt_h = sc_h - top - 2 * indent

        ####
        self.w = sc_w // 5
        self.h = top // 5
        self.ww = self.w + indent
        self.hh = self.h + indent
        tab_w = self.w + 2 * self.ww
        ####

        w_ofs = (sc_w - tab_w) // 2
        csUtil.rect_text(psc, ca, (w_ofs, y_butt, self.w, butt_h), (self.text_b_surface, self.text_b_w, self.text_b_h))
        csUtil.rect_text(psc, cb, (w_ofs + 2 * self.ww, y_butt, self.w, butt_h), (self.text_a_surface, self.text_a_w, self.text_a_h))

        self.score_a.draw((sc_w - 1 - self.score_a.nr_tx.w - 10, y_butt + (butt_h - self.text_a_h) // 2))
        self.score_b.draw((10, y_butt + (butt_h - self.text_a_h) // 2))

        psc.set_alpha(self.alpha)
        sc.blit(psc, (0, top))

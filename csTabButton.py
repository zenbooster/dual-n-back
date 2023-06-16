#!/usr/bin/env python3
#coding: utf-8

import random as rnd
from water import csWaterButton

class csTabButton:
    def __init__(self, ctx, x, y):
        self.ctx = ctx
        self.x = x
        self.y = y
        self.butt = csWaterButton(self.ctx.sc, x + self.ctx.w//2, y + self.ctx.h//2, self.ctx.w, self.ctx.h, self.ctx.br)
        #for i in range(4):
        #    self.butt.hit_corner(i, 3*0.5)
        #self.butt.hit_corner(rnd.randint(0, 3), 2)
        self.butt.hit(rnd.randint(0, self.butt.get_water_length() - 1), 100, 8)
    
    def run(self, is_on):
        sc = self.ctx.sc
        x = self.x
        y = self.y
        w = self.ctx.w
        h = self.ctx.h
        tsc = self.ctx.tsc
        tw = self.ctx.tw
        th = self.ctx.th
        color_on = self.ctx.color_on
        color_off = self.ctx.color_off
        br = self.ctx.br
        if is_on:
            c = color_on
            t = (tsc, tw, th)
        else:
            c = color_off
            t = None
        
        #csUtil.rect_text(sc, c, (x, y, w, h), t, br)
        self.butt.run(c)
        if t is not None:
            tsc, tw, th = t
            sc.blit(tsc, (x + (w - tw) // 2, y + (h - th) // 2))
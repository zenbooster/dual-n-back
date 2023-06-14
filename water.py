#!/usr/bin/env python3
#coding: utf-8

# Imports
import sys
import math
import pygame as pg
import random as rnd

class csWaterCtx:
    def __init__(self, dampening=0.001, tension=0.01):
        self.dampening = dampening
        self.tension = tension

class csWaterSpring:
    def __init__(self, ctx, x, y, vel=0):
        self.ctx = ctx
        self.tgt_len = math.sqrt(x*x + y*y)
        self.cur_len = self.tgt_len
        self.vel = vel
        self.x = x
        self.y = y

    def update(self):
        dh = self.tgt_len - self.cur_len
        if abs(dh) < 0.01:
            self.tgt_len = self.cur_len
        ctx = self.ctx
        self.vel += ctx.tension * dh - self.vel * ctx.dampening
        self.cur_len += self.vel
    
    def get_dt(self):
        return self.tgt_len - self.cur_len

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

class csWater:
    def _move_pt(self, i, dt):
        cx = self.cx
        cy = self.cy
        springs = self.springs

        x = springs[i].x - cx
        y = springs[i].y - cy
        rlen = math.sqrt(x*x + y*y) + dt
        a = math.atan2(y, x)
        onev = (math.cos(a), math.sin(a))
        rvec = (onev[0] * rlen + cx, onev[1] * rlen + cy)
        springs[i].nx = int(rvec[0])
        springs[i].ny = int(rvec[1])

    def __init__(self, sc, cx, cy, dampening=0.001, tension=0.1):
        self.cx = cx
        self.cy = cy
        self.sc = sc
        self.ctx = csWaterCtx(dampening, tension)
        self.springs = []
    
    #def new_spring(self, x, y, vel=rnd.random() / 10):
    def new_spring(self, x, y, vel=0):
        self.springs.append(csWaterSpring(self.ctx, x, y, vel))
    
    def update(self):
        springs = self.springs
        cnt = len(springs)

        for i in range(cnt):
            springs[i].update()

        # распространить волну:
        spread = 0.1
        for i in range(cnt):
            i_prev = (i - 1) % cnt
            i_next = (i + 1) % cnt
            springs[i_prev].vel += spread * (springs[i].cur_len - springs[i_prev].cur_len)
            springs[i_next].vel += spread * (springs[i].cur_len - springs[i_next].cur_len)

            self._move_pt(i, springs[i].get_dt())

    def draw(self, c):
        pts = [(v.nx, v.ny) for v in self.springs]
        pg.draw.polygon(self.sc, c, pts)

    def run(self, c):
        self.update()
        self.draw(c)

    def splash(self, i, v=1):
        self.springs[i].vel += v

class csWaterButton:
    def _fill_corner(self, ox, oy, ang):
        br = self.br
        if br > 0:
            hpi = csWaterButton.hpi
            s = hpi / (2 * br - 1)
            for fp in frange(0, hpi, s):
                p = fp + ang
                x = ox + br * math.cos(p)
                y = oy + br * math.sin(p)
                self.water.new_spring(x, y)

    def _fill_round_rect(self):
        cx = self.cx
        cy = self.cy
        bw = self.bw
        bh = self.bh
        br = self.br
        water = self.water

        ox = cx - bw//2 + br
        oy = cy - bh//2 + br
        self._fill_corner(ox, oy, math.pi)

        oy -= br
        cnt = bw - br*2
        for i in range(0, cnt):
            x = ox + i
            water.new_spring(x, oy)

        ox += cnt
        oy += br
        self._fill_corner(ox, oy, math.pi*3/2)

        ox += br
        cnt = bh - br*2
        for i in range(0, cnt):
            y = oy + i
            water.new_spring(ox, y)

        ox -= br
        oy += cnt
        self._fill_corner(ox, oy, math.pi*2)

        oy += br
        cnt = bw - br*2
        for i in range(0, cnt):
            x = ox - i
            water.new_spring(x, oy)

        ox -= cnt
        oy -= br
        self._fill_corner(ox, oy, math.pi/2)

        ox -= br
        cnt = bh - br*2
        for i in range(0, cnt):
            y = oy - i
            water.new_spring(ox, y)

    def __init__(self, sc, cx, cy, bw, bh, br):
        self.sc = sc
        self.cx = cx
        self.cy = cy
        self.bw = bw
        self.bh = bh
        self.br = br
        self.water = csWater(sc, cx, cy, 0)
        csWaterButton.hpi = math.pi / 2

        self._fill_round_rect()
    
    def run(self, c):
        self.water.run(c)
    
    def hit_corner(self, i, v=1):
        bw = self.bw
        bh = self.bh
        br = self.br

        if i == 0:
            j = 0
        elif i == 1:
            j = bw
        elif i == 2:
            j = bw + bh
        elif i == 3:
            j = bw + bh + bw

        water = self.water
        for i in range(j, j + br):
            water.splash(i, v)

'''
pg.init()

#hpi = math.pi/2
k = 3
w, h = 1024//k, 768//k
sc = pg.display.set_mode((w, h), pg.RESIZABLE)

bw=200
bh=100
br = min(bw, bh) // 8

cx = w // 2
cy = h // 2

butt = csWaterButton(sc, cx, cy, bw, bh, br)

# Game loop.
force = 0.25*4
while  True:
    sc.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                for i in range(4):
                    butt.hit_corner(i, force)
            if event.key == pg.K_1:
                butt.hit_corner(0, force)
            if event.key == pg.K_2:
                butt.hit_corner(1, force)
            if event.key == pg.K_3:
                butt.hit_corner(2, force)
            if event.key == pg.K_4:
                butt.hit_corner(3, force)

    butt.run((0, 0x7f, 0))

    #for pt in ppts:
    #    x, y = pt
    #    pg.draw.rect(sc, c, (x, y, 1, 1))

    pg.display.flip()
'''
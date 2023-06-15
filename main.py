#!/usr/bin/env python3
#coding: utf-8

# Imports
import sys
import pygame as pg
import random as rnd
from threading import Timer
from plasma import csPlasma
from water import csWaterButton
from csStatusPan import csStatusPan
from csUtil import csUtil

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
    
    def run(self, is_on, is_text):
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
            if is_text:
                t = (tsc, tw, th)
            else:
                t = None
        else:
            c = color_off
            t = None
        
        #csUtil.rect_text(sc, c, (x, y, w, h), t, br)
        self.butt.run(c)
        if t is not None:
            tsc, tw, th = t
            sc.blit(tsc, (x + (w - tw) // 2, y + (h - th) // 2))

class csDNB:
    def timeout(self):
        if self.running:
            if self.i_step > self.n:
                if self.seq_a[0] == self.seq_a[self.n]:
                    if self.is_a_clicked:
                        pass
                    else:
                        self.status_pan.score_a.dec()
                if self.seq_b[0] == self.seq_b[self.n]:
                    if self.is_b_clicked:
                        pass
                    else:
                        self.status_pan.score_b.dec()
            
            self.is_a_clicked = False
            self.is_b_clicked = False
            self.is_a_released = False
            self.is_b_released = False

            #self.i_on = rnd.randrange(9)
            while True:
                i_on = rnd.randrange(9)
                if self.i_on != i_on:
                    self.i_on = i_on
                    break

            self.i_on_fx = 0

            #text = chr(ord('А') + rnd.randrange(9))
            while True:
                text = chr(ord('А') + rnd.randrange(9))
                if self.text != text:
                    self.text = text
                    break

            if len(self.seq_a) > self.n:
                self.seq_a.pop(0)

            if len(self.seq_b) > self.n:
                self.seq_b.pop(0)

            self.seq_a.append(self.i_on)
            self.seq_b.append(text)
            
            if self.is_text_buttons:
                self.ctx.set_text(text)

            self.i_step += 1

            self.t = Timer(2, self.timeout)
            self.t.start()
    
    def resize(self):
        self.width = width = self.sc.get_width()
        self.height = height = self.sc.get_height()
        self.indent = height // 25

        pg.font.init()
        #self.font = font = pg.font.SysFont('arial', self.h // 2)
        height = self.height
        indent = self.indent
        self.font = font = pg.font.SysFont('arial', (height - height // 10 + 2 * indent) // 10)

        status_pan = self.status_pan
        status_pan.resize(font, self.indent)

        self.w = width // 5
        self.h = status_pan.get_top() // 5
        self.ww = self.w + self.indent
        self.hh = self.h + self.indent

        self.sc_tab = sc_tab = pg.Surface((self.w + 2 * self.ww, self.h + 2 * self.hh), pg.SRCALPHA)
        self.ctx = ctx = csTabButtonCtx(sc_tab, self.w, self.h, self.brightness, self.color_on, self.color_off, font)
        self.ctx.set_text(self.text)

        self.tab_buttons = []
        for y in range(0, 3 * self.hh, self.hh):
            for x in range(0, 3 * self.ww, self.ww):
                self.tab_buttons.append(csTabButton(ctx, x, y))
        
    def __init__(self):
        pg.init()

        self.fps = 60
        self.fpsClock = pg.time.Clock()
        #width, height = 1024, 768
        k = 3
        width, height = 1024//k, 768//k
        sc = self.sc = pg.display.set_mode((width, height), pg.RESIZABLE)

        #self.indent = 32
        #self.indent = height // 25

        self.brightness = 255
        self.alpha = 0x7f
        self.color_off = (0, 0, self.brightness, 127)
        self.color_on = (0, self.brightness, 0, 127)
        self.color_bt_wait = (self.brightness, self.brightness, self.brightness)
        self.color_bt_ok = (0, self.brightness, 0)
        self.color_bt_err = (self.brightness, 0, 0)

        self.status_pan = status_pan = csStatusPan(self.sc, self.brightness, self.alpha)
        self.text = 'A'
        self.resize()

        self.n = 2
        self.seq_a = []
        self.seq_b = []

        #pg.joystick.init()
        jc = pg.joystick.get_count()
        print(f'joystick_count: {jc}')
        self.j = pg.joystick.Joystick(0)
        self.j.init()

        self.is_a_clicked = False
        self.is_a_released = True
        self.is_b_clicked = False
        self.is_b_released = True

        self.i_step = 0

        self.i_on = 0
        self.i_on_fx = 0

        self.is_text_buttons = True

        self.plasma = csPlasma(sc)
        
        rnd.seed()
        self.running = True
    
    def draw_tab_buttons(self):
        i = 0
        self.sc_tab.fill((0, 0, 0, 0))
        for b in self.tab_buttons:
            b.run(i == self.i_on, self.is_text_buttons)
            i += 1
        sc_tab = self.sc_tab
        self.sc.blit(sc_tab, ((self.width - sc_tab.get_width()) // 2, (self.height - sc_tab.get_height() - self.status_pan.get_height()) // 2))

    def run(self):
        self.timeout()

        # Game loop.
        while  True:
            #self.sc.fill((0, 0, 0))
            self.plasma.run()

            for event in pg.event.get():
                if event.type == pg.VIDEORESIZE:
                    self.resize()
                elif event.type == pg.QUIT:
                    self.running = False
                    self.t.cancel()
                    pg.quit()
                    sys.exit()
                elif event.type == pg.JOYBUTTONDOWN:
                    #print(f'event.button = {event.button}')
                    if event.button == 9: # start
                        self.status_pan.score_a.reset()
                        self.status_pan.score_b.reset()
                        self.i_step = 1
                        self.seq_a = [self.seq_a[-1]]
                        self.seq_b = [self.seq_b[-1]]

                    elif not self.is_b_released and (event.button == 4):
                        self.is_b_clicked = True
                        if len(self.seq_b) > self.n:
                            if self.seq_b[0] == self.seq_b[self.n]:
                                bt_b_color = self.color_bt_ok
                                self.status_pan.score_b.inc()
                            else:
                                bt_b_color = self.color_bt_err
                                self.status_pan.score_b.dec()
                    elif not self.is_a_released and (event.button == 5):
                        self.is_a_clicked = True
                        if len(self.seq_a) > self.n:
                            if self.seq_a[0] == self.seq_a[self.n]:
                                bt_a_color = self.color_bt_ok
                                self.status_pan.score_a.inc()
                            else:
                                bt_a_color = self.color_bt_err
                                self.status_pan.score_a.dec()
                elif event.type == pg.JOYBUTTONUP:
                    if event.button == 4:
                        self.is_b_released = True
                    elif event.button == 5:
                        self.is_a_released = True

            # Main Loop Code belongs here
            self.draw_tab_buttons()
            
            if not self.is_a_clicked:
                bt_a_color = self.color_bt_wait
            if not self.is_b_clicked:
                bt_b_color = self.color_bt_wait

            self.status_pan.draw(bt_a_color, bt_b_color)
            '''
            y_butt = self.y_butt
            pan_top = self.pan_top

            psc = self.psc
            pg.draw.rect(psc, (0, 0, 0x30), (0, 0, self.width - 1, self.height - pan_top - 1))
            y_butt -= pan_top
            butt_h = self.height - pan_top - 2 * self.pan_indent
            w_ofs = (self.width - self.sc_tab.get_width()) // 2
            csUtil.rect_text(psc, bt_b_color, (w_ofs, y_butt, self.w, butt_h), (self.text_b_surface, self.text_b_w, self.text_b_h))
            csUtil.rect_text(psc, bt_a_color, (w_ofs + 2 * self.ww, y_butt, self.w, butt_h), (self.text_a_surface, self.text_a_w, self.text_a_h))

            self.score_a.draw((self.width - 1 - self.score_a.nr_tx.w - 10, y_butt + (butt_h - self.text_a_h) // 2))
            self.score_b.draw((10, y_butt + (butt_h - self.text_a_h) // 2))

            psc.set_alpha(self.alpha)
            self.sc.blit(psc, (0, pan_top))
            '''
            pg.display.flip()
            self.fpsClock.tick(self.fps)

o = csDNB()
o.run()
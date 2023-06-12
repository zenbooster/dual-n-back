#!/usr/bin/env python3
#coding: utf-8

# Imports
import sys
import pygame as pg
import random as rnd
from threading import Timer
from plasma import csPlasma

class csTabButton:
    def __init__(self, sc, x, y, w, h):
        self.sc = sc
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def run(self):
        pass

class csDNB:
    def timeout(self):
        if self.running:
            if self.i_step > self.n:
                if self.seq_a[0] == self.seq_a[self.n]:
                    if self.is_a_clicked:
                        pass
                    else:
                        self.i_a_score -= 1
                if self.seq_b[0] == self.seq_b[self.n]:
                    if self.is_b_clicked:
                        pass
                    else:
                        self.i_b_score -= 1
            
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
                self.text_surface = self.font.render(text, False, (self.brightness, 0, 0))
                self.text_w, self.text_h = self.font.size(text)

            self.i_step += 1

            self.t = Timer(2, self.timeout)
            self.t.start()
    
    def resize(self):
        self.width = width = self.sc.get_width()
        self.height = height = self.sc.get_height()

        pan_indent = self.pan_indent = self.indent * 2
        #self.y_butt = y_butt = height - height // 10 - pan_indent
        #pan_top = self.pan_top = y_butt - pan_indent
        pan_top = self.pan_top = height - height // 10 - 2*pan_indent
        self.y_butt = pan_top + pan_indent

        self.w = width // 5
        self.h = pan_top // 5
        self.ww = self.w + self.indent
        self.hh = self.h + self.indent

        pg.font.init()
        self.font = pg.font.SysFont('arial', self.h // 2)

    def __init__(self):
        pg.init()

        self.fps = 60
        self.fpsClock = pg.time.Clock()
        width, height = 1024, 768
        sc = self.sc = pg.display.set_mode((width, height), pg.RESIZABLE)

        self.indent = 8
        self.resize()

        # self.brightness = 128
        self.brightness = 128*2-1
        #self.alpha = 0x9f
        self.alpha = 0x7f
        self.color_off = (0, 0, self.brightness)
        self.color_on = (0, self.brightness, 0)
        self.color_bt_wait = (self.brightness, self.brightness, self.brightness)
        self.color_bt_ok = (0, self.brightness, 0)
        self.color_bt_err = (self.brightness, 0, 0)

        self.n = 2
        self.seq_a = []
        self.seq_b = []

        #pg.joystick.init()
        jc = pg.joystick.get_count()
        print(f'joystick_count: {jc}')
        self.j = pg.joystick.Joystick(0)
        self.j.init()

        text = '+' # chr(0x25ac)
        self.text_a_surface = self.font.render(text, False, (self.brightness, 0, 0))
        self.text_a_w, self.text_a_h = self.font.size(text)
        text = 'A'
        self.text_b_surface = self.font.render(text, False, (self.brightness, 0, 0))
        self.text_b_w, self.text_b_h = self.font.size(text)

        self.is_a_clicked = False
        self.is_a_released = True
        self.is_b_clicked = False
        self.is_b_released = True
        self.i_a_score = 0
        self.i_b_score = 0
        self.i_step = 0

        self.i_on = 0
        self.text = 'A'
        self.i_on_fx = 0

        self.is_text_buttons = True

        self.plasma = csPlasma(sc)
        rnd.seed()
        self.running = True

    def rect_text(self, sc, c, x, y, w, h, tsc, tw, th):
        '''
        if c == self.color_on:
            if not self.i_on_fx:
                self.i_on_fx = 255
            else:
                if self.i_on_fx > 20:
                    self.i_on_fx -= 20
        
        c = (self.i_on_fx, max(self.i_on_fx, self.brightness), self.i_on_fx)
        '''

        pg.draw.rect(sc, c, (x, y, w, h))
        sc.blit(tsc, (x + (w - tw) // 2, y + (h - th) // 2))
    
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
                        self.i_a_score = 0
                        self.i_b_score = 0
                        self.i_step = 1
                        self.seq_a = [self.seq_a[-1]]
                        self.seq_b = [self.seq_b[-1]]

                    elif not self.is_b_released and (event.button == 4):
                        self.is_b_clicked = True
                        #self.is_b_released = False
                        if len(self.seq_b) > self.n:
                            if self.seq_b[0] == self.seq_b[self.n]:
                                bt_b_color = self.color_bt_ok
                                self.i_b_score += 1
                            else:
                                bt_b_color = self.color_bt_err
                                self.i_b_score -= 1
                    elif not self.is_a_released and (event.button == 5):
                        self.is_a_clicked = True
                        #self.is_a_released = False
                        if len(self.seq_a) > self.n:
                            if self.seq_a[0] == self.seq_a[self.n]:
                                bt_a_color = self.color_bt_ok
                                self.i_a_score += 1
                            else:
                                bt_a_color = self.color_bt_err
                                self.i_a_score -= 1
                elif event.type == pg.JOYBUTTONUP:
                    if event.button == 4:
                        self.is_b_released = True
                    elif event.button == 5:
                        self.is_a_released = True

            # Main Loop Code belongs here
            i = 0
            sc_tab = pg.Surface((self.w + 2 * self.ww, self.h + 2 * self.hh))
            for y in range(0, 3 * self.hh, self.hh):
                for x in range(0, 3 * self.ww, self.ww):
                    if i == self.i_on:
                        if self.is_text_buttons:
                            self.rect_text(sc_tab, self.color_on, x, y, self.w, self.h, self.text_surface, self.text_w, self.text_h)
                        else:
                            pg.draw.rect(sc_tab, self.color_on, (x, y, self.w, self.h))
                    else:
                        pg.draw.rect(sc_tab, self.color_off, (x, y, self.w, self.h))

                    i += 1

            sc_tab.set_alpha(self.alpha)
            self.sc.blit(sc_tab, (self.w, self.h))
            
            if not self.is_a_clicked:
                bt_a_color = self.color_bt_wait
            if not self.is_b_clicked:
                bt_b_color = self.color_bt_wait

            #self.pan_indent = self.indent * 2
            #y_butt = self.height - self.h // 2 - self.pan_indent
            #pan_top = y_butt - self.pan_indent
            y_butt = self.y_butt
            pan_top = self.pan_top

            psc = pg.Surface((self.width, self.height - pan_top))
            pg.draw.rect(psc, (0, 0, 0x30), (0, 0, self.width - 1, self.height - pan_top - 1))
            y_butt -= pan_top
            butt_h = self.height - pan_top - 2 * self.pan_indent
            self.rect_text(psc, bt_b_color, self.w, y_butt, self.w, butt_h, self.text_b_surface, self.text_b_w, self.text_b_h)
            self.rect_text(psc, bt_a_color, self.w + 2 * self.ww, y_butt, self.w, butt_h, self.text_a_surface, self.text_a_w, self.text_a_h)

            text = f'{self.i_a_score}'
            c = self.i_a_score >= 0 and (0, self.brightness, 0) or (self.brightness, 0, self.brightness)
            self.text_a_score_sc = self.font.render(text, False, c)
            self.text_a_score_w, self.text_a_score_h = self.font.size(text)
            psc.blit(self.text_a_score_sc, (self.width - 1 - self.text_a_score_w - 10, y_butt + (butt_h - self.text_a_h) // 2))

            text = f'{self.i_b_score}'
            c = self.i_b_score >= 0 and (0, self.brightness, 0) or (self.brightness, 0, self.brightness)
            self.text_b_score_sc = self.font.render(text, False, c)
            self.text_b_score_w, self.text_b_score_h = self.font.size(text)
            psc.blit(self.text_b_score_sc, (10, y_butt + (butt_h - self.text_a_h) // 2))

            psc.set_alpha(self.alpha)
            self.sc.blit(psc, (0, pan_top))

            pg.display.flip()
            self.fpsClock.tick(self.fps)

o = csDNB()
o.run()
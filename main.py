#!/usr/bin/env python3
#coding: utf-8

# Imports
import sys
import pygame as pg
import random as rnd
from threading import Timer
from plasma import csPlasma
from csTab import csTab
from csStatusPan import csStatusPan
from csUtil import csUtil
from csText import csText

class csDNB:
    def timeout(self):
        if self.running and not self.is_paused:
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

            #text = chr(ord('А') + rnd.randrange(9))
            while True:
                text = chr(ord('А') + rnd.randrange(9))
                if self.tab.get_text() != text:
                    self.text = text
                    break

            if len(self.seq_a) > self.n:
                self.seq_a.pop(0)

            if len(self.seq_b) > self.n:
                self.seq_b.pop(0)

            self.seq_a.append(self.i_on)
            self.seq_b.append(text)
            
            #self.tab.set_text(text)
            self.tab.set(i_on, text)

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
        self.font_big = font_big = pg.font.SysFont('arial', (height - height // 10 + 2 * indent) // 5)
        self.font_big.bold = True

        s_pause = "PAUSE"
        #self.sc_pause = pg.Surface(self.font_big.size(s_pause), pg.SRCALPHA)
        #self.sc_pause.fill((0, 0, 0, 0))
        #self.tx_pause = csText(self.sc_pause, font_big, s_pause, (self.brightness, 0, 0, 32))
        self.tx_pause = csText(self.sc, font_big, s_pause, (self.brightness, 0, 0))
        self.tx_pause.tsc.set_alpha(0x9f)
        #self.tx_pause.draw((0, 0))

        #tab = self.tab
        #tab.resize(font, self.indent, bw, bh)
        status_pan = self.status_pan
        status_pan.resize(font, self.indent)

        bw = width // 5
        bh = status_pan.get_top() // 5
        tab = self.tab
        tab.resize(font, self.height - status_pan.get_height(), self.indent, bw, bh)

    def __init__(self):
        pg.init()

        self.fps = 60
        self.fpsClock = pg.time.Clock()
        #width, height = 1024, 768
        k = 3
        width, height = 1024//k, 768//k
        sc = self.sc = pg.display.set_mode((width, height), pg.RESIZABLE)

        self.brightness = 255
        self.alpha = 0x7f
        self.color_bt_wait = (self.brightness, self.brightness, self.brightness)
        self.color_bt_ok = (0, self.brightness, 0)
        self.color_bt_err = (self.brightness, 0, 0)

        self.tab = tab = csTab(self.sc, self.brightness)
        self.status_pan = status_pan = csStatusPan(self.sc, self.brightness, self.alpha)
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

        self.plasma = csPlasma(sc)
        
        rnd.seed()
        self.running = True
        self.is_paused = False
        self.is_start_released = True
    
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
                else:
                    if event.type == pg.JOYBUTTONDOWN:
                        #print(f'event.button = {event.button}')
                        if self.is_start_released and (event.button == 9): # start
                            if self.is_paused:
                                self.is_paused = False
                                self.timeout()
                            else:
                                self.is_paused = True
                                self.t.cancel()

                            self.is_start_released = False
                            continue

                    elif event.type == pg.JOYBUTTONUP:
                        if event.button == 9:
                            self.is_start_released = True

                    if self.is_paused:
                        pass
                    else:
                        if event.type == pg.JOYBUTTONDOWN:
                            #print(f'event.button = {event.button}')
                            if event.button == 1: # A
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
            #self.tab.draw(self.i_on)
            self.tab.draw()
            
            if not self.is_a_clicked:
                bt_a_color = self.color_bt_wait
            if not self.is_b_clicked:
                bt_b_color = self.color_bt_wait

            self.status_pan.draw(bt_a_color, bt_b_color)

            if self.is_paused:
                self.tx_pause.draw(((self.width - self.tx_pause.w) // 2, (self.height - self.tx_pause.h - self.status_pan.get_height()) // 2))
                #sc_pause = self.sc_pause
                #self.sc.blit(sc_pause, ((self.width - sc_pause.get_width()) // 2, (self.height - sc_pause.get_height() - self.status_pan.get_height()) // 2))

            pg.display.flip()
            self.fpsClock.tick(self.fps)

o = csDNB()
o.run()
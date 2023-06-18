#!/usr/bin/env python3
#coding: utf-8

# Imports
import sys
import pygame as pg
import pygame_shaders as pgsh
import random as rnd
from threading import Timer
from csTab import csTab
from csStatusPan import csStatusPan
from csUtil import csUtil
from csText import csText

class csDNB:
    def timeout(self):
        if self.running and not self.is_paused:
            seq_a = self.seq_a
            seq_a_len = len(seq_a)
            seq_b = self.seq_b
            seq_b_len = len(seq_b)
            if seq_a_len > self.n:
                if seq_a[0] == seq_a[self.n]:
                    if self.is_a_clicked:
                        pass
                    else:
                        self.status_pan.score_a.dec()
            if seq_b_len > self.n:
                if seq_b[0] == seq_b[self.n]:
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

            if seq_a_len > self.n:
                self.seq_a.pop(0)

            if seq_b_len > self.n:
                self.seq_b.pop(0)

            self.seq_a.append(self.i_on)
            self.seq_b.append(text)
            
            #self.tab.set_text(text)
            self.tab.set(i_on, text)

            self.i_step += 1

            self.t = Timer(self.sec_per_step, self.timeout)
            self.t.start()
    
    def resize(self, wh):
        width, height = self.width, self.height = wh
        self.indent = height // 25

        self.sc = sc = pg.display.set_mode(wh, pg.OPENGL | pg.DOUBLEBUF | pg.HWSURFACE | pg.RESIZABLE)
        self.ds = ds = pg.Surface(wh, pg.SRCALPHA)

        #self.shd_bg = pgsh.Shader(wh, wh, (0, 0), "shaders/v-default.txt", "shaders/f-plasma.txt", ds)
        #self.shd_bg = pgsh.Shader(wh, wh, (0, 0), "shaders/v-default.txt", "shaders/f-art.txt", ds)
        self.shd_bg = pgsh.Shader(wh, wh, (0, 0), "shaders/v-default.txt", "shaders/f-smoke-mirrors.txt", ds)
        #self.shd_test = pgsh.Shader(wh, wh, (0, 0), "shaders/v-default.txt", "shaders/f-test.txt", ds)
        self.shd_blit = pgsh.Shader(wh, wh, (0, 0), "shaders/v-blit.txt", "shaders/f-blit.txt", ds)

        pg.font.init()
        height = self.height
        indent = self.indent
        self.font = font = pg.font.SysFont('arial', (height - height // 10 + 2 * indent) // 10)
        self.font_big = font_big = pg.font.SysFont('arial', (height - height // 10 + 2 * indent) // 5)
        self.font_big.bold = True

        s_pause = "ПАУЗА"
        self.tx_pause = csText(self.ds, font_big, s_pause, (self.brightness, 0, 0))
        self.tx_pause.tsc.set_alpha(0x9f)

        status_pan = self.status_pan
        status_pan.resize(ds, font, self.indent)

        bw = width // 5
        bh = status_pan.get_top() // 5
        tab = self.tab
        tab.resize(ds, font, self.height - status_pan.get_height(), self.indent, bw, bh)

    def __init__(self):
        pg.init()

        self.fps = 60
        self.fpsClock = pg.time.Clock()
        width, height = 1024, 768
        k = 1
        wh = (width, height) = 1024//k, 768//k

        self.brightness = 255
        self.alpha = 0x7f
        self.color_bt_wait = (self.brightness, self.brightness, self.brightness)
        self.color_bt_ok = (0, self.brightness, 0)
        self.color_bt_err = (self.brightness, 0, 0)

        self.tab = tab = csTab(self.brightness)
        self.status_pan = status_pan = csStatusPan(self.brightness, self.alpha)
        #self.status_pan = status_pan = csStatusPan(self.brightness, self.alpha * 1.2)
        self.resize(wh)

        self.n = 2
        self.sec_per_step = 1.5
        #self.n = 3
        #self.sec_per_step = 4.0
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
        
        rnd.seed()
        self.running = True
        self.is_paused = False
        self.is_start_released = True
    
    def run(self):
        self.timeout()

        dt = 1.0
        # Game loop.
        while  True:
            self.ds.fill((0, 0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.VIDEORESIZE:
                    self.resize(event.dict['size'])
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
                                n = self.n
                                #if self.i_step > n:
                                #    self.i_step -= n

                                self.seq_a = [self.seq_a[-1]]
                                self.seq_b = [self.seq_b[-1]]

                                self.is_paused = False
                                self.t = Timer(2, self.timeout)
                                self.t.start()
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
            self.tab.draw()

            if not self.is_a_clicked:
                bt_a_color = self.color_bt_wait
            if not self.is_b_clicked:
                bt_b_color = self.color_bt_wait

            self.status_pan.draw(bt_a_color, bt_b_color)

            if self.is_paused:
                self.tx_pause.draw(((self.width - self.tx_pause.w) // 2, (self.height - self.tx_pause.h - self.status_pan.get_height()) // 2))

            shd_bg = self.shd_bg
            shd_bg.send('iResolution', [1, 1])
            shd_bg.send('iTime', [dt])
            shd_bg.render(self.ds)
            '''
            shd_test = self.shd_test
            shd_test.send('iResolution', [1, 1])
            shd_test.send('iTime', [dt])
            shd_test.send('iChannel0', )
            shd_test.render(self.ds)
            '''
            dt += 0.01

            self.shd_blit.render(self.ds)

            pg.display.flip()
            self.fpsClock.tick(self.fps)

o = csDNB()
o.run()
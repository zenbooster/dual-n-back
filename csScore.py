#!/usr/bin/env python3
#coding: utf-8

from csText import csText
import threading as th

class csScore:
    '''
    def _timer_flash(self):
        with self.lck_draw:
            self.i_tx = (self.i_tx + 1) % 2

        with self.lck_timer:
            is_flash = self.is_flash

        if is_flash:
            self.t = th.Timer(self.t_sec, self._timer_flash)
            self.t.start()
        else:
            with self.lck_draw:
                self.i_tx = 0
    '''

    def _timer_term(self):
        with self.lck_timer:
            self.is_flash = False

    def __init__(self, ps_color, ng_color, fl_color = (0xff, 0xff, 0xff)):
        self.ps_color = ps_color
        self.ng_color = ng_color
        self.fl_color = fl_color
        self.i = self.old_i = 0
        self.lck_draw = th.Lock()
        self.lck_timer = th.Lock()
        #self.t_sec = 0.1 # 0.05
        self.tt_sec = 1 # 0.5
        self.is_flash = False
    
    def resize(self, sc, font):
        self.sc = sc
        self.font = font
        self.update()
    
    def update(self):
        sc = self.sc
        #rc = self.rc
        font = self.font
        ps_color = self.ps_color
        ng_color = self.ng_color
        fl_color = self.fl_color
        i = self.i
        text = f'{i}'
        self.nr_tx = nr_tx = csText(sc, font, text, (i < 0) and ng_color or ps_color)
        self.fl_tx = fl_tx = csText(sc, font, text, fl_color)

        with self.lck_draw:
            self.a_tx = [nr_tx, fl_tx]

        if self.i != self.old_i:
            with self.lck_draw:
                self.i_tx = 1

            with self.lck_timer:
                is_flash = self.is_flash
            
            if not is_flash:
                self.is_flash = True
                self.tt = th.Timer(self.tt_sec, self._timer_term)
                self.tt.start()
                #self.t = th.Timer(self.t_sec, self._timer_flash)
                #self.t.start()

            self.old_i = self.i
        else:
            with self.lck_draw:
                self.i_tx = 0

    def reset(self):
        self.i = 0
        self.update()

    def inc(self):
        self.i += 1
        self.update()

    def dec(self):
        self.i -= 1
        self.update()

    def draw(self, rc):
        if self.is_flash:
            self.i_tx = (self.i_tx + 1) % 2
        else:
            self.i_tx = 0

        with self.lck_draw:
            self.a_tx[self.i_tx].draw(rc)
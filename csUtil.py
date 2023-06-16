#!/usr/bin/env python3
#coding: utf-8

import pygame as pg

class csUtil:
    def rect_text(sc, c, rect, tpar, br=0):
        x, y, w, h = rect
        pg.draw.rect(sc, c, rect, border_radius=br)
        
        if tpar is not None:
            tsc, tw, th = tpar
            sc.blit(tsc, (x + (w - tw) // 2, y + (h - th) // 2))

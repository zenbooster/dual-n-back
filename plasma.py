import pygame as pg
import math


Pi2 = math.pi * 2.0     # Просто константа 2 * Пи для простоты и скорости

class csPlasma:
    def getInd(self, num):
        return int((((self.M - 1) * (num % Pi2) / Pi2)))

    def __init__(self, sc):
        self.sc = sc
        self.t = 0 # Сдвиг для получения анимации

        self.M = M = 128           # Размер массива с плазмой
        self.scale = scale = 2               # Масштаб точек для вывода на экран

        self.delta = Pi2 / (M - 1) # Шаг нашего сдвига, на каждом кадре анимации

        self.sintab = sintab = []     # Таблица заранее просчитанных значений синусов
        self.costab = costab = []     # и косинусов.

                        # Заполняем начальными значениями таблицы sin и cos
        t = M - 1
        for i in range(t):
            sintab.append(math.sin(i * Pi2 / t))
            costab.append(math.cos(i * Pi2 / t))

    def run(self):
        M = self.M
        sintab = self.sintab
        costab = self.costab
        scale = self.scale
        t = self.t

        surf = pg.Surface((M * scale, M * scale))
        for i in range(M):
            y = i / M
            for j in range(M):
                x = j / M
                
                # Вычисляем цветовые коэффициенты и затем сами цветовые составляющие
                xpt = x + t
                v_sin = sintab[self.getInd(xpt)]
                a1 = 8.0 * v_sin
                a2 = 7.0 * costab[self.getInd(xpt)]
                a3 = 6.0 * v_sin
                r = int(100 * abs(sintab[self.getInd(a1 * x + t)] + costab[self.getInd(a1 * y - t)]))
                g = int(100 * abs(costab[self.getInd(a2 * y - t)] + sintab[self.getInd(a2 * x + t)]))
                b = int(100 * abs(sintab[self.getInd(a3 * x + t)] + costab[self.getInd(a3 * y - t)]))
                pg.draw.rect(surf, (r//10, g//10, b//4), (i*scale, j*scale, scale, scale))
        
        surf_x = pg.transform.flip(surf, True, False)
        surf_y = pg.transform.flip(surf, False, True)
        surf_xy = pg.transform.flip(surf, True, True)
        m_scale = M * scale
        for j in range(1 + self.sc.get_height() // m_scale):
            for i in range(1 + self.sc.get_width() // m_scale):
                if j & 1:
                    src = (i & 1) and surf_xy or surf_y
                else:
                    src = (i & 1) and surf_x or surf

                self.sc.blit(src, (i * m_scale, j * m_scale))

        # "Двигаем" анимацию
        t += self.delta
        if t >= Pi2:
            t = 0
        self.t = t
from math import exp

class TwistGenerator:
    def __init__(self):
        self.w = 16 # битовая длина числа
        self.N1 = 0 # максимальное число
        self.x0 = 1 # начало последовательности
        self.xB = 1 # начало очередного вихря
        self.xG = 0 # созданная случайная величина
        self.xL = 0
        self.xR = 1 # парные величины
        self.abf = 0.39 # относительное начало а
        self.aef = 0.39 # относительнео окончание a
        self.a1b = 1 # начало интервала a1
        self.a1e = 0 # конец интервала а1
        self.a1s = 0 # состояние интервала а1
        self.a2b = 1 # начало интервала a2
        self.a2e = 0 # конец интервала а2
        self.a2s = 0 # состояние интервала а2
        self.a1 = 5 # константа для интервала а1
        self.a2 = 5 # константа для интервала а2
        self.nA = 1 # номер константы а1 или а2
        self.a = 5 # текущее значение константы а
        self.cbf = 0.1 # относительное начало с
        self.cef = 0.3 # относительное окончание с
        self.cb = 1 # начало интервала с
        self.ce = 0 # окончание интервала с
        self.c = 1 # конгруэнтная константа с
        self.stG = 0 # номер группы состояний
        self.st0 = 1 # группа начальных состояний
        self.st1 = 101 # группа генерации xG
        self.st2 = 201 # группа смены параметров
        self.nW = 0 # номер парного вихря в w
        self.nT = 0 # номер вихря
        self.nV = 0 # номер элемента в x
        self.maskW = 0 # маска числа
        self.maskU = 0 # маска старшего бита
        self.maskT = 0 # вихревые биты



        self.N = 10 # ? количество равномерных событий
        self.dN = 10 # ? количество равномерных событий
        self.Alpha = 2 # параметр Alpha
        self.emAlpha = exp(-self.Alpha) # exp(-Alpha)
        self.cEta = 0 # максимальное Eta
        self.pC = [] # распределение вероятностей
        self.nuC = [] # распределение частот
        self.cnuC = [] # кумулятивные частоты
        
        self.N1 = 0xFFFFFFFF >> (32 - int(self.w))
        self.x0 = self.N1 // 7

    def Next(self):
        flagNext = True
        while flagNext:
            if self.stG == 0:
                flagNext = self.__DeonYuli_Next0()
            elif self.stG == 1:
                flagNext = self.__DeonYuli_Next1()
            elif self.stG == 2:
                flagNext = self.__DeonYuli_Next2()
        return self.xG

    def __DeonYuli_Next0(self):
        flagWhile0 = True
        while flagWhile0:
            if self.st0 == 1: # начальные действия
                self.nA = 1
                self.a1s = 1
                self.a2s = 0
                self.a1 = self.a1e
                self.a = self.a1
                self.a2 = self.a2b - 4
                self.c = self.cb
                self.st0 = 2
            elif self.st0 == 2: # при измененных параметрах
                self.xB = self.x0
                self.xR = self.xB
                self.nT = 0
                self.nW = 0
                self.nV = 0
                self.stG = 1
                self.st1 = 101
                flagWhile0 = False
        return True # необходима генерация xG

    def __DeonYuli_Next1(self):
        flagNext1 = False
        flagWhile1 = True
        while flagWhile1:
            if self.st1 == 101: # конгруэнтная генерация
                self.xL = self.xR
                self.xR = self.__DeonYuli_Cong(self.xL)
                self.xG = self.xL
                if self.nV < self.N1:
                    self.nV = self.nV + 1
                else:
                    self.st1 = 102
                flagWhile1 = False # число создано
            elif self.st1 == 102: # для парного вихря nW
                self.nW = self.nW + 1
                if self.nW < self.w:
                    self.maskT = self.maskU
                    for m in range(1, self.nW):
                        self.maskT |= self.maskU >> m
                    self.xL = self.xB
                    self.xR = self.__DeonYuli_Cong(self.xL)
                    self.nV = 0
                    self.st1 = 103 # генерировать вихрь nT
                else:
                    self.st1 = 104
            elif self.st1 == 103: # генерация вихря
                self.xG = self.__DeonYuli_TwistPair()
                self.xL = self.xR
                self.xR = self.__DeonYuli_Cong(self.xL)
                if self.nV == self.N1:
                    self.st1 == 102
                else:
                    self.nV = self.nV + 1
                flagWhile1 = False
            elif self.st1 == 104: # закончились вихри nW внутри nT
                if self.nT < self.N1:
                    self.nT = self.nT + 1
                    self.xB = self.__DeonYuli_Cong(self.xB)
                    self.xR = self.xB
                    self.nW = 0
                    self.nT = 0
                    self.st1 = 101
                else:
                    self.st1 = 105
            elif self.st1 == 105:
                self.stG = 2
                self.st2 = 201
                flagWhile1 = False
                flagNext1 = True
        return flagNext1

    def __DeonYuli_Next2(self):
        flagNext2 = True
        flagWhile2 = True
        while flagWhile2:
            if self.st2 == 201: # изменить параметр с
                self.c += 2
                if self.c < self.ce:
                    self.stG = 0
                    self.st0 = 2
                    flagWhile2 = False
                    flagNext2 = True
                else:
                    self.st2 = 202
            elif self.st2 == 202: # заменить интервал по а
                self.c = self.cb
                if self.nA == 1:
                    self.nA = 2
                else:
                    self.nA = 1
                if self.nA == 1:
                    self.st2 = 203
                else:
                    self.st2 = 204
            elif self.st2 == 203: # новое значение из а1
                self.a1 -= 4
                if self.f1 < self.a1b:
                    self.a1s = 2
                    self.st2 = 205
                else:
                    self.a = self.a1
                    self.c = self.cb
                    self.a1s = 1
                    self.stG = 0
                    self.st0 = 2
                    flagWhile2 = False
                    flagNext2 = True
            elif self.st2 == 204: # новое значение из а2
                self.a2 += 4
                if self.a2 > self.a2e:
                    self.a2s = 2
                    self.st2 = 205
                else:
                    self.a = self.a2
                    self.c = self.cb
                    self.a2s = 1
                    self.stG = 0
                    self.st0 = 2
                    flagWhile2 = False
                    flagNext2 = True
            elif self.st2 == 205: # один из а1 или а2 пройдет
                if self.a2s != 2:
                    self.st2 = 204
                elif self.s1s != 2:
                    self.st2 = 203
                else:
                    self.stG = 0
                    self.st0 = 1
                    flagWhile2 = False
                    flagNext2 = True
        return flagNext2

    def __DeonYuli_Cong(self, z):
        return (self.a * z + self.c) & self.maskW

    def __DeonYuli_TwistPair(self):
        g = (self.xR & self.maskT) >> int(self.w - self.nW)
        return ((self.xL << int(self.nW)) & self.maskW) | g

    def __Start(self):
        self.N1 = 0xFFFFFFFF >> (32 - int(self.w))
        self.maskW = 0xFFFFFFFF >> (32 - int(self.w))
        self.maskU = 1 << (int(self.w) - 1)
        self.maskT = self.maskU
        self.__DeonYuli_SetA()
        self.__DeonYuli_SetC()
        self.x0 &= self.maskW
        self.stG = 0
        self.st0 = 1

    def SetW(self, sw):
        self.w = abs(sw)
        if self.w < 3:
            self.w = 3
        elif self.w > 32:
            self.w = 32
        self.N1 = 0xFFFFFFFF >> (32 - int(self.w))
        self.x0 = self.N1 // 7

    def SetA(self, sab, sae):
        self.abf = abs(sab)
        self.aef = abs(sae)
        if self.abf > 1:
            self.abf = 1
        if self.aef > 1:
            self.aef = 1
        if self.abf > self.aef:
            self.aef = self.abf

    def __DeonYuli_SetA(self):
        self.a1b = int(self.N1 * self.abf)
        self.a1b = self.__DeonYuli_PlusA(self.a1b)
        self.a2e = int(self.N1 *  self.aef)
        self.a2e = self.__DeonYuli_MinusA(self.a2e)
        r = self.a2e - self.a2b
        if self.a1b > self.a2e:
            self.a1e = self.a1b
            self.a2b = self.a1b
            self.a2e = self.a2b
            return
        if r == 4:
            self.a1e = self.a1b
            self.a2b = self.a2e
            return
        if r == 8:
            self.a1e = self.a1b + 4
            self.a2b = self.a2e
            return
        self.a1e = (self.a1b + self.a2e) // 2
        self.a1e = self.__DeonYuli_MinusA(self.a1e)
        self.a2b = self.a1e + 4

    def __DeonYuli_PlusA(self, a):
        if a < 1:
            a = 1
            return a
        z = a
        for i in range(3):
            if a % 4 != 0:
                a -= 1
            else:
                break
        a += 1
        if a < z:
            a += 4
        if a >= self.N1 - 1:
            a -= 4
        return a

    def __DeonYuli_MinusA(self, a):
        if a < 1:
            a = 1
            return a
        z = 1
        for i in range(3):
            if a % 4 != 0:
                a -= 1
            else:
                break
        a += 1
        if a > z:
            a -= 4
        return a

    def setC(self, scb, sce):
        self.cbf = abs(scb)
        self.cef = abs(sce)
        if self.cbf > 1:
            self.cbf = 1
        if self.cef > 1:
            self.cef = 1
        if self.cbf > self.cef:
            self.cef = self.cbf

    def __DeonYuli_SetC(self):
        self.cb = int(self.N1 * self.cbf)
        if self.cb % 2 == 0:
            self.cb += 1
        if self.cb > self.N1:
            self.cb = self.N1
        self.ce = int(self.N1 * self.cef)
        if self.ce % 2 == 0:
            self.ce -= 1
        if self.ce > self.N1 - 1:
            self.ce = self.N1
        if self.cb > self.ce:
            self.ce = self.cb
        self.c = self.cb

    def setX0(self, xs):
        self.x0 = int(self.N1 * abs(xs))


    def start(self, alpha):
        self.Alpha = alpha
        self.__Start()
        self.__start_inside()

    def __start_inside(self):
        wX = 300
        self.pC = [0] * wX # распределение вероятностей
        self.nuC = [0] * wX # распределение частот
        self.cnuC = [0] * wX # кумулятивные частоты
        self.emAlpha = exp(-self.Alpha)
        self.N = self.N1 + 1
        self.dN = self.N
        self.cEta = self.__CPoissonDY() # вероятности и частоты
        self.__CVerifyProbability() # проверка вероятности

    def CNext(self, l=1):
        z = self.Next()
        result = self.__CSearchEta(z)
        return result

    def __CPoissonDY(self):
        spC = 0
        snuC = 0
        self.pC[0] = self.emAlpha
        spC += self.pC[0]
        self.nuC[0] = round(self.pC[0] * self.dN)
        snuC += self.nuC[0]
        self.cnuC[0] = snuC
        r = self.Alpha
        self.pC[1] = r * self.emAlpha
        spC += self.pC[1]
        self.nuC[1] = round(self.pC[1] * self.dN)
        snuC += self.nuC[1]
        self.cnuC[1] = snuC
        Eta = 2
        while True:
            r *= self.Alpha / Eta
            p = r * self.emAlpha
            nu = round(p * self.dN)
            if abs(nu) < 1e-8:
                break
            sd = snuC + nu
            if abs(nu) < 1e-8 or sd > self.N:
                break
            self.pC[Eta] = p
            spC += p
            self.nuC[Eta] = nu
            snuC += nu
            self.cnuC[Eta] = snuC
            Eta += 1
            if snuC >= self.N:
                break
        Eta -= 1
        d = self.N - snuC
        if (abs(d) < 1e-8):
            return Eta
        d1N = (1 - spC) / d
        while True:
            Eta += 1
            self.pC[Eta] = d1N
            self.nuC[Eta] = 1
            snuC += 1
            self.cnuC[Eta] = snuC
            if snuC >= self.N:
                break
        return Eta

    def __CVerifyProbability(self):
        for i in range(self.cEta):
            self.pC[i] = self.nuC[i] / self.dN

    def __CSearchEta(self, z):
        Eta = 0
        for i in range(self.cEta):
            Eta = i
            if z < self.cnuC[i]:
                break
        return Eta
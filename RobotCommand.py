#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ServerController import ServerController


class RobotCommand(object):
    def __init__(self, index, name, address, port, log):
        self._server = ServerController(address, port, log)
        self._index = index
        self._name = name
        self._server.send("I{} = {}".format(index, name))

    def srd(self, index, value):
        """
        Установка скорости вращения
        :param index:
        :param value:
        :return: self
        """
        self._server.send("SRD{} = {}".format(index, value))
        return self

    def srt(self, index, value):
        """
        Установить начальный угол поворота
        :param index:
        :param value:
        :return: self
        """
        self._server.send("SRT{} = {}".format(index, value))
        return self

    def gst(self, index):
        """
        Показатели сенсора касания
        :param index:
        :return: bool
        """
        self._server.send("GST{}".format(index))
        return bool(self._server.read())

    def gsd(self, index):
        """
        Показатели сенсора дистанции
        :param index:
        :return:
        """
        self._server.send("GSD{}".format(index))
        return float(self._server.read())

    def gsl(self):
        self._server.send("GSL")
        return self._server.read()

    def gsc(self):
        """
        Зарядное напряжение
        :return:
        """
        self._server.send("GSC")
        return self._server.read()

    def grd(self, index):
        """
        Угловая скорость вращения, часть от максимальной
        максимальное значение задается параметром motorOmega
        в конфигурации робота
        :param index:
        :return:
        """
        self._server.send("GRD{}".format(index))
        return float(self._server.read())

    def grt(self, index):
        """
        Угол поворота, рад
        :param index:
        :return:
        """
        self._server.send("GRT{}".format(index))
        return float(self._server.read())

    def gsd_all(self):
        """
        Список всех показаний датчика GSD
        :return: list
        """
        self._server.send("GSD*")
        gsd = self._server.read().split(',')
        response = []
        for i in gsd:
            response.append(float(i))
        return response

    def grd_all(self):
        """
        Список всех показаний датчика GSD
        :return: list
        """
        self._server.send("GRD*")
        gsd = self._server.read().split(',')
        response = []
        for i in gsd:
            response.append(float(i))
        return response

    def gpx(self):
        self._server.send("GPX{}".format(self._index))
        return self._server.read()

    def gpy(self):
        self._server.send("GPY{}".format(self._index))
        return self._server.read()

    def gpa(self):
        self._server.send("GPA{}".format(self._index))
        return self._server.read()

    def gpv(self):
        self._server.send("GPV{}".format(self._index))
        return self._server.read()

    def gpw(self):
        self._server.send("GPV{}".format(self._index))
        return self._server.read()

    def gpt(self):
        self._server.send("GPV{}".format(self._index))
        return self._server.read()

    def gp(self):
        self._server.send("GP{}".format(self._index))
        return self._server.read()

    def mark_pos(self):
        self._server.send("_MarkPos_{}".format(self._index))
        return self

    def pause(self):
        self._server.send("_Pause")
        return self

    def resume(self):
        self._server.send("_Resume")
        return self

    def ast(self, sensor, port):
        self._server.send("AST{} = {}, {}".format(sensor, self._index, port))
        return self

    def asd(self, sensor, port):
        self._server.send("ASD{} = {}, {}".format(sensor, self._index, port))
        return self

    def asl(self, port):
        self._server.send("ASL = {}, {}".format(self._index, port))
        return self

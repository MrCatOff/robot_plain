#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ipaddress import ip_address
from socket import socket
from threading import Thread
from time import sleep, time
from math import pi, cos, sin


class RobotPlain:
    """
    Задержка отправки запросов на считывание показателей сенсора и координат робота с углом
    """
    SENSORS_REQUEST_TIME_LIMIT = 0.3
    """
    Максимальный размер буфера для сокет запросов
    """
    SERVER_RESPONSE_BUFFER_SIZE = 128

    class Robot:
        def __init__(self, index=0, name="wheeled", address='127.0.0.1', port=27015, log=False):
            self._index = index
            self._name = name
            self._address = address
            self._port = port
            self._log = log
            self._server = RobotPlain.Server(address, port)
            self._server.command("I{} = {}".format(index, name))
            self._plot_coord = RobotPlain.PlotSensors(self)
            self._plot_coord.start()

        def read_indicators(self):
            """
            Считывать показатели сенсоров
            :return:
            """
            self._plot_coord.read = True

        def not_read_indicators(self):
            """
            Не считывать показатели сенсоров
            :return:
            """
            self._plot_coord.read = False

        def get_indicators(self):
            """
            Получить показатели сенсоров
            :return:
            """
            return self._plot_coord.list_point

        def clear_indicators(self):
            """
            Очистить показатели сенсоров
            :return:
            """
            self._plot_coord.list_point = []

        def gsd_all(self) -> list:
            """
            GSD*
            :return: list[float]
            """
            gsd = self._server.command("GSD*").split(',')
            response = []
            for i in gsd:
                response.append(float(i))
            return response

        def grd_all(self) -> list:
            """
            GRD*
            :return: list[float]
            """
            grd = self._server.command("GRD*").split(',')
            response = []
            for i in grd:
                response.append(float(i))
            return response

        def gpx(self) -> float:
            """
            Получить положение по x робота
            :return:
            """
            return float(self._server.command("GPX{}".format(self._index)))

        def gpy(self):
            """
            Получить положение по Y робота
            :return:
            """
            return float(self._server.command("GPY{}".format(self._index)))

        def gpa(self):
            """
            Получить угол поворота робота (Радианы)
            :return:
            """
            return float(self._server.command("GPA{}".format(self._index)))

        def asd(self, sensor, port):
            """
            ASD<sensor> = <nRobot>, <Port>
            :param sensor:
            :param port:
            :return:
            """
            self._server.command("ASD{} = {}, {}".format(sensor, self._index, port))

        def ast(self, sensor, port):
            """
            AST<sensor> = <nRobot>, <Port>
            :param sensor:
            :param port:
            :return:
            """
            self._server.command("AST{} = {}, {}".format(sensor, self._index, port))

        def asl(self, port):
            """
            ASL = <nRobot>, <Port>
            :param port:
            :return:
            """
            self._server.command("ASL = {}, {}".format(self._index, port))

        def pause(self):
            """
            Приостановка работы сцены
            :return:
            """
            self._server.command("_Pause")

        def resume(self):
            """
            Возобновляет работу сцены
            :return:
            """
            self._server.command("_Resume")

        def srd(self, index, value):
            """
            Установка скорости моторов
            :param index:
            :param value:
            :return: self
            """
            self._server.command("SRD{} = {}".format(index, value))

    class Server:
        def __init__(self, address='127.0.0.1', port=27018):
            """
            Открывает соединение с Robot Plain
            :param address:
            :param port:
            """
            ip_address(address)
            if port not in range(1, 65535):
                raise ValueError('The port must be a number between 1 and 65535')
            self.__socket = socket()
            self.__socket.connect((address, port))

        def command(self, command) -> str:
            """
            Отправляет команды на Robot Plain
            :param command:
            :return:
            """
            self.__socket.send(str.encode(command))
            recv = self.__socket.recv(RobotPlain.SERVER_RESPONSE_BUFFER_SIZE).decode("UTF-8").replace("\n", "")
            return recv

        def __del__(self) -> None:
            """
            Закрывает соединение с Robot Plain
            :return:
            """
            self.__socket.close()

    class PlotSensors(Thread):
        def __init__(self, robot):
            if type(robot) is not RobotPlain.Robot:
                raise ValueError("Robot not type RobotPlain.Robot")
            Thread.__init__(self)
            self.__robot = robot
            self.list_point = []
            self.__x = 0.0
            self.__y = 0.0
            self.read = False

        def run(self):
            """
            Запускает считывание показателей сенсора
            :return: None
            """
            while True:
                if self.read:
                    try:
                        x = self.__robot.gpx()
                        y = self.__robot.gpy()
                        if round(x, 2) != self.__x or round(y, 2) != self.__y:
                            self.__x = round(x, 2)
                            self.__y = round(y, 2)
                            self.list_point.append({
                                'x': x,
                                'y': y,
                                'a': self.__robot.gpa(),
                                'gsd': self.__robot.gsd_all(),
                                'time': round(time())
                            })
                    except ValueError:
                        pass
                sleep(RobotPlain.SENSORS_REQUEST_TIME_LIMIT)

    class PlotCoords:
        @staticmethod
        def remove_old(points, less_seconds=200) -> list:
            """
            Метод удаляет старые значения координат
            :param points:
            :param less_seconds:
            :return:
            """
            new_points = []
            for point in points:
                if point['time'] > time() - less_seconds:
                    new_points.append(point)
            return new_points

        @staticmethod
        def rad_to_angle(rad) -> float:
            """
            Конвертирует радианы в градусы
            :param rad:
            :return:
            """
            return rad * 180 / pi

        @staticmethod
        def coord_by_area(area=0, distance=8, x1=0, y1=0):
            """
            Определяет координаты по углу, дистанции, и координатам точки
            :param area:
            :param distance:
            :param x1:
            :param y1:
            :return:
            """
            u = area * pi / 180
            x = x1 + cos(u) * distance
            y = y1 + sin(u) * distance
            return x, y

        @staticmethod
        def create_point_coordinates(points=[], sensor_phi=[]) -> list:
            """
            Создает список координат точек
            :param points:
            :param sensor_phi:
            :return:
            """
            coordinates_points = []
            for point in points:
                length = 0
                for sd in point['gsd']:
                    if sd < 2.5:
                        area = RobotPlain.PlotCoords.rad_to_angle(point['a'])
                        if area > 0:
                            area += sensor_phi[length]
                        else:
                            if sensor_phi[length] < 0:
                                area = -(abs(sensor_phi[length]) + abs(area))
                            else:
                                if sensor_phi[length] != 0:
                                    if abs(area) > sensor_phi[length]:
                                        area = area + sensor_phi[length]
                                    else:
                                        area = sensor_phi[length] + area
                        x, y = RobotPlain.PlotCoords.coord_by_area(area, round(sd * 100), point['x'], point['y'])
                        coordinates_points.append({
                            'x': x,
                            'y': y,
                            'robot': {
                                'x': point['x'],
                                'y': point['y'],
                                'a': point['a'],
                                'time': point['time'],
                                'sd': sd
                            },
                            'time': time()
                        })
                    length += 1
            return coordinates_points


if __name__ == '__main__':
    """
    Подключиться к эмулятору по адресу 127.0.0.1 и порту 27015,
    установить робота I0 с именем wheeled
    отключить логирование работы (пока что не реализовано)
    """
    robot_plain = RobotPlain.Robot(0, "wheeled", '127.0.0.1', 27015, False)
    """ Установить сенсор ASD0 роботу который находится на порте 0 """
    robot_plain.asd(0, 0)
    """ Установить сенсор ASD1 роботу который находится на порте 1 """
    robot_plain.asd(1, 1)
    """ Поставить паузу сцене """
    robot_plain.pause()
    """ Установить скорость 0 мотора в 0.1 (10) """
    robot_plain.srd(0, 0.1)
    """ Установить скорость 1 мотора в 0.1 (10) """
    robot_plain.srd(1, 0.1)
    """ Возобновить работу робота """
    robot_plain.resume()
    """ Запустить считывание сенсоров """
    robot_plain.read_indicators()
    """ Пауза на 5 секунд """
    sleep(5)
    """ Отключить считывание сенсоров """
    robot_plain.not_read_indicators()
    """ Поставить паузу сцене """
    robot_plain.pause()
    """ Установить скорость 0 мотора в 0 """
    robot_plain.srd(0, 0)
    """ Установить скорость 1 мотора в 0 """
    robot_plain.srd(1, 0)
    """ Возобновить работу робота """
    robot_plain.resume()
    """ Получить количество показателей сенсора """
    print(len(robot_plain.get_indicators()))
    """ Вывести показатели сенсоров """
    print(robot_plain.get_indicators())
    """ Вывести координаты точек для прорисовки """
    print(RobotPlain.PlotCoords.create_point_coordinates(
        robot_plain.get_indicators(),
        [pi, -pi]
    ))
    """ Очистить показатели сенсоров """
    robot_plain.clear_indicators()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ipaddress import ip_address
from socket import socket
from CoreFunction import LogController, singleton


@singleton
class ServerController(object):
    """
    Контроллер доступка к Robot Plain, соединение, отправка команд
    Pattern: Singleton
    """
    def __init__(self, address='127.0.0.1', port=27018, log=False):
        """
        Инициализация подключения к програме эмулятору Robot Plain
        :param address: IP Адресс Robot Plain
        :param port: Порт Robot Plain
        """
        ip_address(address)
        if port not in range(1, 65535):
            raise ValueError('The port must be a number between 1 and 65535')
        if type(log) is not bool:
            raise ValueError('The log must be a bool')
        self._socket_client = socket()
        self._socket_client.connect((address, port))
        self._address = address
        self._port = port
        self._log = log
        self._request = ''

    def socket(self):
        """
        Получение Socket подключения
        :return: object
        """
        return self._socket_client

    def socket_change(self, address='127.0.0.1', port=27018):
        """
        Изменение socket подключения к програме эмулятору Robot Plain
        :param address:
        :param port:
        :return:
        """
        ip_address(address)
        if port not in range(1, 65535):
            raise ValueError('The port must be a number between 1 and 65535')
        self._socket_client.connect((address, port))
        self._address = address
        self._port = port
        return self.socket

    @property
    def address(self):
        """
        Получение текущего адреса подключения к програме Robot Plain
        :return:
        """
        return self._address

    @property
    def port(self):
        """
        Получение текущего порта подключения к програме Robot Plain
        :return:
        """
        return self._port

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, log):
        if log is not bool:
            raise ValueError('The log must be a bool')
        self._log = log
        return self._log

    def send(self, command):
        """
        Отправка команды на Robot Plain
        :param command:
        :return:
        """
        if self._log:
            LogController().add(command)
        self.socket().send(str.encode(command))
        request = self.socket().recv(1024).decode("UTF-8").replace("\n", "")
        if self._log:
            LogController().add(request)
        self._request = request

    def read(self):
        """
        Получение ответа от програмы Robot Plain
        :param buffer:
        :return:
        """
        return self._request

    def __del__(self):
        """
        Отключение от програмы Robot Plain
        :return:
        """
        self._socket_client.close()

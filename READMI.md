<pre>if __name__ == '__main__':
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
    robot_plain.clear_indicators()</pre>

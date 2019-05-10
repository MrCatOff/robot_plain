<pre>Подключаем робота к симулятору<br/>
0 - ID робота,
wheeled - Название робота,
127.0.0.1 - IP Robot Plain,
True - Включить логирование</pre>
<pre>robot = RobotCommand(0, 'wheeled', '127.0.0.1', 20037, True)</pre>
<hr/>
<pre>
Выполнить команды:
    ASD0 = 0, 0
    ASD1 = 0, 1
    ASD2 = 0, 1
    ASD3 = 0, 1
    ASD4 = 0, 1
</pre>
<pre>robot.asd(0, 0).asd(1, 1).asd(2, 2).asd(3, 3).asd(4, 4)</pre>
<hr/>
<pre>Выполнить команду GSD*, GPX, GPY, GPA</pre>
<pre>robot.gsd_all()
robot.gpx()
robot.gpy()
robot.gpa()</pre>
<pre>Тестовый код:
from RobotCommand import RobotCommand
from CoreFunction import LogController
from time import sleep
def main():
    robot = RobotCommand(0, 'wheeled', '127.0.0.1', 20037, True)
    robot.asd(0, 0).asd(1, 1).asd(2, 2).asd(3, 3).asd(4, 4)
    robot.gsd_all()
    robot.gpx()
    robot.gpy()
    robot.gpa()
    robot.pause().srd(0, 0.05).srd(1, 0.05).resume()
    sleep(5)
    robot.pause().srd(0, 0).srd(1, 0).resume()
    for log in LogController().get():
        print(log)
if __name__ == '__main__':
    main()</pre>
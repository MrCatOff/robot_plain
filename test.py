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
    main()
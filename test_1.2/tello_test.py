from pkgutil import get_data
from re import X
from time import sleep
import tellopy
from tellopy._internal.utils import *
from tellopy._internal.protocol import *
import stream_tello
import threading
import pygame

prev_flight_data = None
font = None
x = 5

def handler(event, sender, data, **args):
    global prev_flight_data
    global x
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)
        print(data.battery_percentage)
        x = data.battery_percentage
        print(x)
        return x
    elif event is drone.EVENT_LOG_DATA:
        log_data = data
        #print(log_data)



def test(drone):
    try:
        sleep(15)
        drone.takeoff()
        sleep(5)
        drone.down(50)
        sleep(3)
        drone.up(50)
        sleep(3)
        drone.down(0)
        sleep(2)
        drone.land()
        sleep(5)
    except Exception as ex:
        print(ex)
        show_exception(ex)
    print('end.')

if __name__ == '__main__':
    drone = tellopy.Tello()
    drone.connect()
    drone.wait_for_connection(20.0)
    drone.subscribe(drone.EVENT_LOG_DATA, handler)
    drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
    video = threading.Thread(target=stream_tello.Stream, args=(drone,))
    commandos = threading.Thread(target=test, args=(drone,))


    print(x)
    drone.take_picture()
    video.start()
    commandos.start()
    sleep(2)
    print(x)
    # drone.quit()
    # print('END')
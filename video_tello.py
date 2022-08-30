from configparser import Interpolation
import sys
import traceback
import tellopy
import av
import cv2  # for avoidance of pylint error
import numpy
import time


def frameRescale(frame, scale=0.82):

    withh = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)

    dimesion = (withh,height)

    return cv2.resize(frame, dimesion, interpolation=cv2.INTER_AREA)


        




def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                image_resize = frameRescale(image)
                #cv2.imshow('Original', image)
                cv2.imshow('Resize',image_resize)
                cv2.imshow('Canny', cv2.Canny(image_resize, 100, 200))
                cv2.waitKey(1)
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                frame_skip = int((time.time() - start_time)/time_base)
                    

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

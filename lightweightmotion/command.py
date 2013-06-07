from lightweightmotion.camera import HTTPCamera, USBCamera
from lightweightmotion.environment import Environment


def main():
    cam = USBCamera(0)
    env = Environment('captures')
    for frame in cam.motion(90, 20, 50):
        print(frame)
        env.make_space(40 * 1024**2)
        env.save_frame(frame)


if __name__ == '__main__':
    main()

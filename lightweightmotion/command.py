from lightweightmotion.camera import HTTPCamera, USBCamera
from lightweightmotion.environment import Environment


def main():
    cam = USBCamera(0)
    env = Environment('captures')
    for event in cam.events(90, 20, 50):
        env.save_event(event)


if __name__ == '__main__':
    main()

import pygame
import time

def main():
    pygame.mixer.init()
    pygame.mixer.music.load('drink-water.mp3')
    pygame.mixer.music.play()
    time.sleep(5)
    pygame.mixer.music.stop()

if __name__ == '__main__':
    main()

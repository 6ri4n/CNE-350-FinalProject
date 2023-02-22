import pygame

def main():
    pygame.mixer.init()
    sound = pygame.mixer.Sound('drink-water.mp3')
    playing = sound.play()
    while playing.get_busy():
        continue

if __name__ == '__main__':
    main()

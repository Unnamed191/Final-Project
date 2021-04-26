import pygame
import gameLevels
import os

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("./music/Go Time.flac")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, 0)
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 30)  # Set the position where the window appears
    plane = gameLevels.PlaneGame()
    plane.start()

if __name__ == '__main__':
    main()

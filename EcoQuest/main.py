import pygame
import sys
from game import EcoQuest

pygame.init()

if __name__ == "__main__":
    jogo = EcoQuest()
    jogo.executar()
    pygame.quit()
    sys.exit()

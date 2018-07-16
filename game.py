import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
from rank import Rank

ranks = [Rank("lory", "lory.jpg"), Rank("hulio", "hulio.jpg"), Rank("Regueiro", "arrebato.jpg")]


def load_ranks(ranks):
    rank_images[:] = []
    rank_areas[:] = []
    for rank in ranks:
        rank_image = pygame.image.load(rank.filename).convert_alpha()
        rank_images.append(rank_image)


def on_identification_complete():
    load_ranks(ranks)
    for image_idx, image in enumerate(rank_images):
        image = pygame.transform.scale(image, (100, 100))
        r = screen.blit(image, (screen_width - 100, 0 + image_idx * 100))
        rank_areas.append(r)
    message = game_font.render('SELECT YOUR IDENTITY', 1, (125, 255, 0))
    screen.blit(message, (screen_width / 2 - 100, 500))
    pygame.display.update()


def on_rank_clicked(idx):
    screen.fill([0, 0, 0])
    id_selected_message = game_font.render('Thanks {}'.format(ranks[idx].id), 1, (255, 100, 0))
    screen.blit(id_selected_message, (500, 0))
    pygame.display.update()


camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("Coffee machine mess blamer")
screen = pygame.display.set_mode([1280, 720])
pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
game_font = pygame.font.SysFont('Comic Sans MS', 30)

rank_images = []
rank_areas = []
names = ['lory', 'hulio', 'regueiro']

gradiant_logo = pygame.image.load('gradiant.png').convert_alpha()

REQUIRED_FRAMES = 100

complete = False
counter = 0

screen_width, screen_height = pygame.display.get_surface().get_size()

try:
    while not complete:

        ret, frame = camera.read()
        counter = counter + 1
        screen.fill([0, 0, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, (screen_width, screen_height))
        screen.blit(frame, (0, 0))
        gradiant_logo = pygame.transform.scale(gradiant_logo, (100, 100))
        screen.blit(gradiant_logo, (screen_width - 150, screen_height - 100))
        pygame.display.update()

        if counter >= REQUIRED_FRAMES:
            on_identification_complete()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    textsurface = game_font.render('Some Text', 1, (255, 255, 0))
                    screen.blit(textsurface, (500, 0))
                    pygame.display.update()
                if event.key == pygame.K_q:
                    sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for idx, rank_area in enumerate(rank_areas):
                    if rank_area.collidepoint(pos):
                        on_rank_clicked(idx)
                        counter = 0

except KeyboardInterrupt, SystemExit:
    pygame.quit()
cv2.destroyAllWindows()

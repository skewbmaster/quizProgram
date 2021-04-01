import pygame
import json
from pygame.locals import *
from os import environ, getcwd
from sys import exit as sysexit
from random import randint

environ['SDL_VIDEO_CENTERED'] = '1'

width, height = 1280, 720

screen = pygame.display.set_mode((width, height), HWSURFACE)

clock = pygame.time.Clock()

mfont = pygame.font.SysFont('Calibri', 24)

class Question:
    def __init__(self, question, answers, correct):
        self.question = question
        self.answers = answers
        self.correct = correct

    def check(self, answer):
        if self.correct == answer:
            return True
        return False

def serializeQuestions():
    tempq = []
    
    with open("questions.json") as f:
        jobject = json.loads(f.read())
        for questionobj in jobject['questions']:
            tempq.append(Question(questionobj[0], questionobj[1], questionobj[2]))

    for question in range(len(tempq)):
        randq = randint(0, len(tempq)-1)
        
        questions.append(tempq[randq])
        tempq.pop(randq)

if __name__ == "__main__":
    questions = []
    serializeQuestions()

    curquestion = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sysexit()

        screen.fill((30,30,30))

        pygame.draw.rect(screen, (255,250,250), [width//8, height//8, width-(width//4), height-(height//4)])

        screen.blit(mfont.render(questions[curquestion].question), ())



        clock.tick(60)
        pygame.display.update()

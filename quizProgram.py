import pygame
import json
from pygame.locals import *
from os import environ, getcwd
from sys import exit as sysexit
from random import randint

pygame.init()

environ['SDL_VIDEO_CENTERED'] = '1'

width, height = 1280, 720

screen = pygame.display.set_mode((width, height), HWSURFACE)

clock = pygame.time.Clock()

mfont = pygame.font.SysFont('Calibri', 48)

arrowleft = pygame.image.load('arrowleft.png')
arrowright = pygame.image.load('arrowright.png')

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

def generateSurfaces(questions):
    surfs = []
    
    for question in questions:
        cursurf = pygame.Surface((width - (width//4), height-(height//2)))
        
        splitquestion = question.question.split('\n')

        cursurf.fill((255,250,250))
        
        for i in range(len(splitquestion)):
            cardText = mfont.render(splitquestion[i], True, (0,0,0), (255,250,250))
            cursurf.blit(cardText, (480 - cardText.get_width() // 2, 180 - cardText.get_height() // 2 - (len(splitquestion)-1-i)*48))

        surfs.append(cursurf)

    return surfs


if __name__ == "__main__":
    questions = []
    
    serializeQuestions()
    answers = [None for i in range(len(questions))]
    
    questionSurfaces = generateSurfaces(questions)

    curquestion = 0
    totalPoints = 0

    while True:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sysexit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(40, height//2 - 40, 80, 80).collidepoint(mx,my) and curquestion > 0:
                    curquestion -= 1

                elif pygame.Rect(1160, height//2 - 40, 80, 80).collidepoint(mx,my) and curquestion < len(questions)-1:
                    curquestion += 1

                for i in range(4):
                    if pygame.Rect(i*241 + width//8, 500, 235, 175).collidepoint(mx,my):
                        answers[curquestion] = i

                if curquestion == len(questions)-1:
                    if pygame.Rect(1160, height//2-40, 80, 80).collidepoint(mx,my):
                        totalPoints = 0
                        for i in range(len(questions)):
                            if questions[i].correct == answers[i]:
                                totalPoints += 1


        screen.fill((30,30,30))

        questionNumText = mfont.render("Q" + str(curquestion+1), True, (255,250,250), (30,30,30))
        screen.blit(questionNumText, (width//2 - questionNumText.get_width()//2, 20))

        screen.blit(questionSurfaces[curquestion], (width//8, height//8))

        for answer in range(4):
            pygame.draw.rect(screen, (255,250,250), [answer*241 + width//8, 500, 235, 175])

            splitText = questions[curquestion].answers[answer].split('\n')

            ansTextSurf = pygame.Surface((235, len(splitText)*48))
            ansTextSurf.fill((255,250,250))
            for i in range(len(splitText)):
                ansText = mfont.render(splitText[i], True, (0,0,0), (255,250,250))
                ansTextSurf.blit(ansText, (117 - ansText.get_width()//2, i*48))

            screen.blit(ansTextSurf, (width//8 + answer*241, 587 - ansTextSurf.get_height()//2))

            if answers[curquestion] == answer:
                pygame.draw.rect(screen, (25,20,20), [answer*241 + width//8, 500, 235, 175], width=6)

        if curquestion > 0:
            screen.blit(arrowleft, (40, height//2-40))

        if curquestion < len(questions)-1:
            screen.blit(arrowright, (1160, height//2-40))


        if curquestion == len(questions)-1:
            pygame.draw.rect(screen, (20,200,50), [1160, height//2-40, 80, 80])

        if totalPoints != 0:
            screen.blit(mfont.render(str(totalPoints) + "/" + str(len(questions)), True, (255,250,250), (30,30,30)), (1100,20))

        clock.tick(60)
        pygame.display.update()

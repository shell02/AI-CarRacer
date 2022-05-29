import pygame

class Game:
    FRAMES = 0

    def __init__(self, win, img):
        self.win = win
        self.img = img
        
    def draw_background(self):
        if self.FRAMES != 100:
            self.FRAMES += 10
        else:
            self.FRAMES = 0
        for i in range(-100, 700, 100):
            self.win.blit(self.img, (0, i + self.FRAMES))

    def draw_window(self, Players, Cars, font, score):
        self.draw_background()
        try:
            for i in Players:
                i.draw(self.win)
        except:
            Players.draw(self.win)
        for i in Cars:
            i.draw(self.win)
        text = font.render("Score: " + str(score), 1, (0, 0, 0))
        self.win.blit(text, (380, 30))
        pygame.display.update()

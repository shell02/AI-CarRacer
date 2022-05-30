import math

class Player:
    VEL = 4
    STAG = 0

    def __init__(self, Rect, img):
        self.rect = Rect
        self.img = img
        self.lane = self.getLane()

    def collision(self, cars):
        for car in cars:
            if self.rect.colliderect(car):
                return 1
        return 0

    def playerMov(self, keys_pressed):
        if keys_pressed == 1 and self.rect.x - self.VEL > 0:
            self.rect.x -= self.VEL # go to the left
        if keys_pressed == 2 and \
                self.rect.x + self.VEL + self.rect.width < 500:
            self.rect.x += self.VEL # got to the right
         if self.lane != self.getLane():
            self.lane = self.getLane()
            self.STAG = 0
        else:
            self.STAG += 1

    def draw(self, win):
         win.blit(self.img, (self.rect.x, self.rect.y))
    
    def getLane(self):
        if self.rect.x < 110:
            return 0
        if 110 <= self.rect.x < 210:
            return 1
        if 210 <= self.rect.x < 310:
            return 2
        if 310 <= self.rect.x < 410:
            return 3
        if 400 <= self.rect.x:
            return 4

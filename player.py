import math

class Player:
    VEL = 4

    def __init__(self, Rect, img):
        self.rect = Rect
        self.img = img

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

    def draw(self, win):
         win.blit(self.img, (self.rect.x, self.rect.y))
    
    def getDistance(self, car):
        a = (self.rect.x + 40, self.rect.y)
        b = (car.rect.x + 40, car.rect.y + car.rect.height)
        return int(math.dist(a, b))
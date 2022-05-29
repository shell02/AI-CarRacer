class Cars:
    def __init__(self, Rect, img, speed):
        self.rect = Rect
        self.img = img
        self.speed = speed

    def draw(self, win):
        if self.rect.y < 700:
            self.rect.y += self.speed
            win.blit(self.img, (self.rect.x, self.rect.y))
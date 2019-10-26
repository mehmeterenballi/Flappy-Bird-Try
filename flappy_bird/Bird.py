import pygame as pg


class Bird(pg.sprite.Sprite):

    def __init__(self, screen, pos=[0, 0], *groups):
        self.alive = True
        self.flySound = pg.mixer.Sound('lips.wav')
        # F = m * a
        # g = 9.8 m/s^2
        # upwards: v += g * t, downwards: v -= g * t
        # x = a*t^2 / 2
        # x = v * t
        self.g = 9.8  # gravity
        self.v = 400  # speed

        # self.x = self.v * self.time

        self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image_array = []
        for i in range(1, 4):
            self.image_array.append(pg.image.load("b{}.png".format(str(i))).convert_alpha())

        self.current_pic = 0
        self.image = self.image_array[self.current_pic]
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.screenrect = screen.get_rect()

        self.pos = pos.copy()
        self.rect.center = self.pos

        self.animationinterval = 0.2
        self.animationtime = 0

        self.flyinginterval = 0.5
        self.flyingtime = 0

        self.buttoninterval = self.flyinginterval / 2
        self.buttontime = 0

        self.flying = False

        self.spin = 0
        self.spin_speed = 4
        self.last_update = pg.time.get_ticks()

        self.upwards = False

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now

            while self.spin < 60 and self.upwards and self.flying:
                self.spin += 1
                self.image = pg.transform.rotate(self.image_orig, self.spin)
                if self.spin == 60:
                    self.upwards = False
                    while 60 >= self.spin > 0:
                        self.spin -= 1
                        self.image = pg.transform.rotate(self.image_orig, self.spin)

            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def animation(self, time):
        self.animationtime += time
        if self.animationtime > self.animationinterval:
            self.current_pic += 1
            self.current_pic %= 3
            self.image = self.image_array[self.current_pic]
            self.animationtime = 0

    def update(self, time):

        if not self.alive:
            self.kill()

        elif self.alive:

            self.rotate()

            # F = m * a
            # g = 9.8 m/s^2
            # upwards: v += g * t, downwards: v -= g * t
            # x = a*t^2 / 2
            # x = v * t

            click = pg.mouse.get_pressed()

            # dx_u = self.v * time
            # dx_d = (self.v * time) / 2

            if self.flying:
                self.g = 9.8
                self.v -= self.g * time
                dx_u = self.v * time
                self.pos[1] -= dx_u
                self.flyingtime -= time
                self.animation(time)
                self.buttontime = self.buttoninterval
                self.upwards = True
            else:
                self.g = -9.8
                self.v += self.g * time
                dx_d = (self.v * time) / 2
                self.pos[1] += dx_d
                self.upwards = False

            if self.flyingtime <= 0:
                self.flying = False

            if self.buttontime >= 0:
                self.buttontime -= time

            if click[0] == 1 and self.buttontime <= 0:
                self.v = 400
                self.flySound.play()
                self.flyingtime = self.flyinginterval
                self.flying = True

            self.rect.center = self.pos

            if self.rect.top > self.screenrect.bottom:
                self.alive = False
        else:
            print("Bu ne lan amk")

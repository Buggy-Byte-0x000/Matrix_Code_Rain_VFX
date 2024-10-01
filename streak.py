import time

from generator import Generator

class Streak:
    def __init__(self, instance_number):
        self.instance_number = instance_number

        # (creates an array with space for all the characters from this streak)
        self.streak = [None] * 67

        # (creates an array with space for all the characters from this streak)
        if Generator.biased_boolean(0.975):
            self.testspeed = 1
        else:
            self.testspeed = 2

        #(visible or not)
        self.status = self.update_status()

        if self.status:
            for y in range(67):
                self.streak[y] = Generator.random_char()

        #(position of the white character "leading" the streak)
        self.head = Generator.random_number(0, 67)
        self.sec_head = self.head - Generator.random_number(0, 80)
        #(number of visible previous characters)
        self.interval = Generator.random_number(10, 30)

        #(opacity and color transition effects on the streak)
        self.streak_opacities = [0] * 67
        self.streak_colors_red = [0] * 67
        self.streak_colors_green = [0] * 67
        self.streak_colors_blue = [0] * 67

    def get_status(self):
        return self.status
    def get_streak(self):
        return self.streak
    def get_opacities(self):
        return self.streak_opacities
    def get_colors_red(self):
        return self.streak_colors_red
    def get_colors_green(self):
        return self.streak_colors_green
    def get_colors_blue(self):
        return self.streak_colors_blue

    #(120 ** ((self.head - y)) / (self.interval))
    def update_Streak(self):
        self.increment_head_position()
        for y in range(52):
            if y == self.head:
                self.streak_opacities[y] = 255
                self.streak_colors_red[y] = 255
                self.streak_colors_green[y] = 255
                self.streak_colors_blue[y] = 255
            elif y == self.sec_head and self.testspeed != 2:
                if self.sec_head > self.head - self.interval:
                    self.streak_opacities[y] = 255
                else:
                    self.streak_opacities[y] = 0
                self.streak_colors_red[y] = 255
                self.streak_colors_green[y] = 255
                self.streak_colors_blue[y] = 255
            elif y < self.head:
                self.streak_opacities[y] = 255 - (self.head - y) * (255 / self.interval)
                self.streak_colors_red[y] = 135
                self.streak_colors_green[y] = 255
                self.streak_colors_blue[y] = 135 + (75 - (self.head - y) * (140 / self.interval))
                if self.streak_opacities[y] > 0:  #(performance optimization)
                    if Generator.biased_boolean(0.3):
                        self.update_char(y)
            else:
                self.streak_opacities[y] = 0  #(why does removing this worsen performance ??)

    def update_char(self, y):
        self.streak[y] = Generator.random_char()

    def update_status(self):
        return Generator.biased_boolean(1)

    def increment_head_position(self):
        if self.head < Generator.random_number(52, 400):
            if Generator.biased_boolean(0.5):
                self.head += self.testspeed
        else:
            self.head = 0

        if self.sec_head < self.head and Generator.biased_boolean(1):
            self.sec_head += self.testspeed
        elif self.sec_head + 2 > self.head:
            self.sec_head = -30
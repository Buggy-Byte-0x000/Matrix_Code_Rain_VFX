from generator import Generator
from streak import Streak

class Matrix:
    cols = 180
    rows = 52

    #(creates an array with all the Streak instances from the matrix)
    Streaks = [None for i in range(cols)]
    for i in range(cols):
        Streaks[i] = Streak(i)

    @classmethod
    def get_Streak_instance(cls, x):
        return cls.Streaks[x]

    @classmethod
    def update(cls):
        for x in range(cls.cols):
            cls.Streaks[x].update_Streak()
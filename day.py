"""my day simulator"""

from random import random

class FSM:
    """class with all states"""
    def __init__(self):
        # initializing states
        self.SLEEP = self._create_sleep()
        self.EAT = self._create_eat()
        self.STUDY = self._create_study()
        self.DEPRESSION = self._create_depression()
        self.WALK = self._create_walk()
        self.PROCRASTINATE = self._create_procrastinate()

        # setting current state of the system
        self.current_state = self.SLEEP

        # stopped flag to denote that iteration is stopped due to bad
        # input against which transition was not defined.
        self.stopped = False

    def send(self, hour):
        """The function sends the curretn input to the current state
        It captures the StopIteration exception and marks the stopped flag.
        """
        try:
            self.current_state.send(hour)
        except TypeError:
            self.current_state.send(None)
            self.current_state.send(hour)
        except StopIteration:
            self.stopped = True

    def _create_sleep(self):
        while True:
            hour = yield
            print(f'At {hour} I sleep...')
            if hour in range(0, 8):
                self.current_state = self.SLEEP
            elif hour in range(8, 12) and random()<0.6:
                print(f'It\'s already {hour}! Time to wake up and have breakfast!')
                self.current_state = self.EAT
            elif hour==12:
                print(f'It\'s already {hour}! Time to wake up!')
                self.current_state = self.DEPRESSION
            elif hour == 24:
                print('The day has ended!')
            else:
                self.current_state=self.SLEEP

    def _create_eat(self):
        while True:
            hour = yield
            print(f'At {hour} I go and eat')
            if hour == 23:
                self.current_state = self.SLEEP
            elif hour <= 19:
                self.current_state = self.WALK
            else:
                self.current_state = self.STUDY

    def _create_walk(self):
        while True:
            hour = yield
            print(f'At {hour} I am outside on a walk')
            if hour == 23:
                self.current_state = self.SLEEP
            elif random()<=0.2:
                self.current_state = self.WALK
            elif hour <=14:
                self.current_state = self.PROCRASTINATE
            elif random()<0.4:
                self.current_state = self.EAT
            else:
                self.current_state = self.STUDY

    def _create_study(self):
        while True:
            hour = yield
            print(f'At {hour} I finally study!')
            if hour == 23:
                self.current_state = self.SLEEP
            elif random()<=0.9 and hour>=20:
                self.current_state = self.STUDY
            elif 14 <= hour <= 19 and random()<0.4:
                self.current_state = self.STUDY
            elif random()<0.7:
                self.current_state=self.EAT
            else:
                self.current_state = self.WALK

    def _create_depression(self):
        while True:
            hour = yield
            print(f'At {hour} I feel sad :_(')
            if hour == 23:
                self.current_state = self.SLEEP
            elif random()<0.3 and hour<=20:
                self.current_state = self.DEPRESSION
            elif random()<0.6 and hour>20:
                print('I\'m tired, so I want to lay down for a bit')
                self.current_state = self.DEPRESSION
            elif random()<0.2:
                self.current_state = self.WALK
            else:
                self.current_state = self.STUDY

    def _create_procrastinate(self):
        while True:
            hour = yield
            print(f'At {hour} I procrastinate (I know, don\'t judge me)')
            if hour == 23:
                self.current_state = self.SLEEP
            elif random()<=0.9 and hour>=21:
                self.current_state = self.STUDY
            elif hour <= 13:
                self.current_state = self.PROCRASTINATE
            elif random() < 0.5 and hour<=19:
                self.current_state = self.EAT
            else:
                self.current_state = self.STUDY

def day_cycle():
    """
    sends walues to the system
    """
    evaluator = FSM()
    evaluator.send(None)
    for hour in range(1, 25):
        evaluator.send(hour)

if __name__=="__main__":
    day_cycle()

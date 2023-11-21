from random import random

from generator import Generator
from handler import Handler

generation = 0
handling = 1

time = 0
state = 1

class System:
    def __init__(self, a, b, k, labmd, msg_num, probability, step):
        self.messages_amount = msg_num
        self.return_chance = probability
        self.step = step
        self.generator = Generator(a, b)
        self.handler = Handler(k, labmd)

    def delta_t(self):
        max_length = 0
        queue_length = 0
        processed_amount = 0
        self.handler.free = True

        handling_time = 0
        current_time = self.step
        generated_time = self.generator.get_time_interval()
        previous_generated_time = 0

        while processed_amount < self.messages_amount:
            if current_time > generated_time:
                queue_length += 1

                if queue_length > max_length:
                    max_length = queue_length

                previous_generated_time = generated_time
                generated_time += self.generator.get_time_interval()

            if current_time > handling_time:
                if queue_length > 0:
                    handler_was_free = self.handler.free
                    if self.handler.free:
                        self.handler.free = False
                    else:
                        processed_amount += 1
                        queue_length -= 1
                        return_chance = random()
                        if return_chance <= self.return_chance:
                            queue_length += 1
                    if handler_was_free:
                        handling_time = previous_generated_time + self.handler.get_time_interval()
                    else:
                        handling_time += self.handler.get_time_interval()
                else:
                    self.handler.free = True
            current_time += self.step

        return max_length

    def event_driven(self):
        max_length = 0
        queue_length = 0
        processed_amounts = 0
        processed = False
        self.handler.free = True

        events = [[self.generator.get_time_interval(), generation]]

        while processed_amounts < self.messages_amount:
            event = events.pop(0)

            if event[state] == generation:
                queue_length += 1
                if queue_length > max_length:
                    max_length = queue_length
                self.__insert_event(events, [event[time] + self.generator.get_time_interval(), generation])
                if self.handler.free:
                    processed = True

            if event[state] == handling:
                processed_amounts += 1
                return_chance = random()
                if return_chance <= self.return_chance:
                    queue_length += 1
                processed = True

            if processed:
                if queue_length > 0:
                    queue_length -= 1
                    self.__insert_event(events, [event[time] + self.handler.get_time_interval(), handling])
                    self.handler.free = False
                else:
                    self.handler.free = True

                processed = False

        return max_length

    def __insert_event(self, events, event):
        i = 0
        while i < len(events) and events[i][time] < event[time]:
              i += 1
        if 0 < i < len(events):
            events.insert(i - 1, event)
        else:
            events.insert(i, event)
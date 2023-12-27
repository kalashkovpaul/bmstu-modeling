class Event:
    def __init__(self, creator, time):
        self.creator = creator
        self.time = time

def sort_events(events):
    return sorted(events, key=lambda event: event.time)

class FlywheelRecorder(object):
    def __init__(self):
        self.flywheel_updates = []

    def update(self, elapsed_time):
        self.flywheel_updates.append(elapsed_time)

    def get_change(self):
        return len(self.flywheel_updates)

    def reset_change(self):
        self.flywheel_updates = []

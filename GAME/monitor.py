class Monitor(object):
    def __init__(self, num_required_samples):
        self.current_dist = 0
        self.current_speed = 0
        self.r_sample = 0
        self.samples_taken = 0
        self.num_required_samples = num_required_samples

    def update(self, r_change):
        self.r_sample += r_change
        self.samples_taken +=1

        if self.samples_taken >= self.num_required_samples:
            self.samples_taken = 0
            self.snapshot()
            self.r_sample = 0

    def snapshot(self):
        # use 1.03 if sample is 2 second
        self.current_speed = self.r_sample * 1.03
        self.current_dist += (self.current_speed/60)/30

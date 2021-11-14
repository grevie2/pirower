"""This class contains a generator that will batch flywheel updates into
time chunks of size display_sample."""
class FlywheelBatchGenerator(object):
    def __init__(self, ts_ary, display_sample):
        self.ts_ary = ts_ary
        self.ts_pos = 0
        self.max_ts_boundary = display_sample
        self.display_sample = display_sample
        self.current_sample_time_point = 0

    def generate(self):
        current_sample = 0
        while self.ts_pos < len(self.ts_ary) and \
            self.ts_ary[self.ts_pos] < self.max_ts_boundary:
            current_sample += 1
            self.ts_pos += 1

        self.current_sample_time_point += self.display_sample
        self.max_ts_boundary += self.display_sample
        yield current_sample

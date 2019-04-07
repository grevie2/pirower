"""This class is a generator."""
from strokesensorrecorder import StrokeSensorRecorder

class StrokeBatchGenerator(object):
    """My class docstring."""
    def __init__(self, ts_ary, display_sample):
        self.ir_timestamp_ary = ts_ary
        self.position = 0
        self.max_boundary = display_sample
        self.display_sample = display_sample
        self.current_sample_time_point = 0
        self.stroke_sensor_rec = StrokeSensorRecorder()

    def __iter__(self):
        return self

    def next(self):
        """Get the next sample's worth of data."""
        count = 0

        #while current_elapsed < self.max_boundary:
        while self.position < len(self.ir_timestamp_ary) and \
            self.ir_timestamp_ary[self.position][0] < self.max_boundary:

            current_elapsed = self.ir_timestamp_ary[self.position][0]
            ir_id = self.ir_timestamp_ary[self.position][1]
            count += self.stroke_sensor_rec.update(current_elapsed, ir_id)
            self.position += 1
            self.stroke_sensor_rec.reset_change()

        stroke_pos_change = count
        count = 0
        self.max_boundary += self.display_sample
        return stroke_pos_change

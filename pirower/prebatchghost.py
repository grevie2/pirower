from ghost_batch import Ghost
from timestampbatcher import TimestampBatcher
from irbatcher import IRBatcher

class PreBatchGhost(Ghost):
    def __init__(self, gst_img_path, data_filename, x, trial_length, display_sample, layer_multiplier=1):

        #super(PreBatchGhost, self).__init__(gst_img_path, data_filename, x, trial_length, display_sample)
        #can't use super on an old style class
        Ghost.__init__(self, gst_img_path, data_filename, x, layer_multiplier)

        tb = TimestampBatcher(self.timestamp_ary)
        self.batched_ts_ary = []
        self.batched_ts_ary = tb.convert_ts_array_to_display_array(trial_length, display_sample)

        irtb = IRBatcher(self.ir_timestamp_ary)
        self.batched_ir_ts_ary = []
        self.batched_ir_ts_ary = irtb.convert_stroke_array_to_display_array(display_sample)

        self.sample_index = 0
        self.stroke_index = 0

    def generate_next_flywheel_update(self):
        if self.sample_index < len(self.batched_ts_ary):
            update = int(self.batched_ts_ary[self.sample_index])
            self.sample_index += 1
            return update
        else:
            return 0

    def generate_next_ir_update(self):
        if self.stroke_index < len(self.batched_ir_ts_ary):
            stroke_pos_update = int(self.batched_ir_ts_ary[self.stroke_index])
            self.stroke_index += 1
            return stroke_pos_update
        else:
            return 0

    def update(self, viewable_min_r, viewable_max_r):
        self.r_y += self.generate_next_flywheel_update()
        
        #self.stroke_pos_current += self.generate_next_ir_update()
        self.stroke_pos_change = self.generate_next_ir_update()
        self.stroke_pos_current += self.stroke_pos_change
        
        #return super(PreBatchGhost, self).update(viewable_min_r, viewable_max_r)
        #can't use super on an old style class
        return Ghost.update(self, viewable_min_r, viewable_max_r)

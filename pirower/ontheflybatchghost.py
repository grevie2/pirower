from ghost_batch import Ghost

from FlywheelBatchGenerator import FlywheelBatchGenerator
from StrokeBatchGenerator import StrokeBatchGenerator

class OnTheFlyBatchGhost(Ghost):
    def __init__(self, gst_img_path, data_filename, x, trial_length, display_sample, layer_multiplier=1):
        #super(OnTheFlyBatchGhost, self).__init__(gst_img_path, data_filename, x, trial_length, display_sample)
        #can't use super on an old style class
        Ghost.__init__(self, gst_img_path, data_filename, x, layer_multiplier)

        self.flywheel_generator = FlywheelBatchGenerator(self.timestamp_ary, display_sample)
        self.stroke_generator = StrokeBatchGenerator(self.ir_timestamp_ary, display_sample)

    def generate_next_flywheel_update(self):
        return next(self.flywheel_generator.generate(), 0)

    def generate_next_ir_update(self):
        return next(self.stroke_generator, 0)

    def update(self, viewable_min_r, viewable_max_r):
        self.r_y += self.generate_next_flywheel_update()
        
        #self.stroke_pos_current += self.generate_next_ir_update()
        self.stroke_pos_change = self.generate_next_ir_update()
        self.stroke_pos_current += self.stroke_pos_change
        
        #return super(OnTheFlyBatchGhost, self).update(viewable_min_r, viewable_max_r)
        #can't use super on an old style class
        return Ghost.update(self, viewable_min_r, viewable_max_r)

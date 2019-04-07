"""This class collects data from the stroke sensor"""

from constants import IR_ONE, IR_TWO, IR_THREE, MAX_BACKWARD_RANGE, MAX_FORWARD_RANGE

class StrokeSensorRecorder(object):
    def __init__(self):
        self.old_ir = 0
        self.stroke_pos_change = 0
        self.ir_pos_change = 0
        self.ir_pos_updates = []
        self.ir_pos = 0

    def update(self, elapsed_time, new_ir):
        #this if needs to be here to remove any duplicate IRs
        if new_ir != self.old_ir:
            self.ir_pos_updates.append([elapsed_time, new_ir])

            if (self.old_ir == IR_ONE and new_ir == IR_TWO) \
            or (self.old_ir == IR_TWO and new_ir == IR_THREE) \
            or (self.old_ir == IR_THREE and new_ir == IR_ONE):
                if self.ir_pos < MAX_FORWARD_RANGE:
                    self.ir_pos_change += 1
                    self.ir_pos += 1
            else:
                if self.ir_pos > MAX_BACKWARD_RANGE:
                    self.ir_pos_change -= 1
                    self.ir_pos -= 1
                    #print "self.ir_pos_change now", self.ir_pos_change 
            self.old_ir = new_ir

        if self.ir_pos_change >= 3:
            #forward 1 frame
            self.stroke_pos_change += int(self.ir_pos_change/3)
            self.ir_pos_change = self.ir_pos_change % 3
            #self.ir_pos_change = 0
            #self.stroke_pos_change += 1
        elif self.ir_pos_change <= -3:
            #back 1 frame
            self.stroke_pos_change -= int(self.ir_pos_change/-3)
            self.ir_pos_change = self.ir_pos_change % -3
            #self.ir_pos_change = 0
            #self.stroke_pos_change -= 1

        return self.stroke_pos_change

    def get_ir_pos_updates(self):
        return self.ir_pos_updates

    def get_stroke_pos_change(self):
        return self.stroke_pos_change

    def reset_change(self):
        self.stroke_pos_change = 0
        self.ir_pos_updates = []

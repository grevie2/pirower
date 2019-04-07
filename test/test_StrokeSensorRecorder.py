#! /usr/bin/python3
import unittest
import sys
sys.path.insert(0, '../')
from strokesensorrecorder import StrokeSensorRecorder

#NOTE: You must go back before you go forward!!!

class TestStrokeSensorRecorder(unittest.TestCase):

    def test_one_stroke_pos_change_back(self):
        ssr = StrokeSensorRecorder()
        ssr.update('800',3)
        ssr.update('810',2)
        ssr.update('820',1)
        self.assertEquals(-1,ssr.get_stroke_pos_change())
        self.assertEquals([['800',3], \
                           ['810',2], \
                           ['820',1]],ssr.get_ir_pos_updates())

    def test_two_stroke_pos_change_back(self):
        ssr = StrokeSensorRecorder()
        ssr.update('800',3)
        ssr.update('810',2)
        ssr.update('820',1)
        ssr.update('830',3)
        ssr.update('840',2)
        ssr.update('850',1)
        self.assertEquals(-2,ssr.get_stroke_pos_change())
        self.assertEquals([['800',3], \
                           ['810',2], \
                           ['820',1], \
                           ['830',3], \
                           ['840',2], \
                           ['850',1]],ssr.get_ir_pos_updates())

    def test_one_stroke_pos_change_forwrd_and_two_back(self):
        ssr = StrokeSensorRecorder()
        ssr.update('800',1)
        ssr.update('810',2)
        ssr.update('820',3)
        ssr.update('830',2)
        ssr.update('840',1)
        ssr.update('850',3)
        ssr.update('860',2)
        ssr.update('870',1)
        ssr.update('880',3)
        self.assertEquals(-1,ssr.get_stroke_pos_change())
        self.assertEquals([['800',1], \
                           ['810',2], \
                           ['820',3], \
                           ['830',2], \
                           ['840',1], \
                           ['850',3], \
                           ['860',2], \
                           ['870',1], \
                           ['880',3]],ssr.get_ir_pos_updates())

    def test_no_stroke_pos_change(self):
        ssr = StrokeSensorRecorder()
        ssr.update('800',3)
        ssr.update('810',2)
        ssr.update('820',3)
        ssr.update('830',2)
        self.assertEquals(0,ssr.get_stroke_pos_change())
        self.assertEquals([['800',3], \
                           ['810',2], \
                           ['820',3], \
                           ['830',2]], ssr.get_ir_pos_updates())

    def test_moving_forward_cancels_out_moving_back(self):
        ssr = StrokeSensorRecorder()
        ssr.update('800',1)
        ssr.update('810',2)
        ssr.update('820',3)
        ssr.update('830',2)
        ssr.update('840',1)
        ssr.update('850',3)
        self.assertEquals(0,ssr.get_stroke_pos_change())
        self.assertEquals([['800',1], \
                           ['810',2], \
                           ['820',3], \
                           ['830',2], \
                           ['840',1], \
                           ['850',3]], ssr.get_ir_pos_updates())

    def test_moving_back_cancels_out_moving_forward(self):
        ssr = StrokeSensorRecorder()
        ssr.update('800',3)
        ssr.update('810',2)
        ssr.update('820',1)
        ssr.update('830',2)
        ssr.update('840',3)
        ssr.update('850',1)
        self.assertEquals(0,ssr.get_stroke_pos_change())
        self.assertEquals([['800',3], \
                           ['810',2], \
                           ['820',1], \
                           ['830',2], \
                           ['840',3], \
                           ['850',1]], ssr.get_ir_pos_updates())

    def test_no_activity(self):
        ssr = StrokeSensorRecorder()
        self.assertEquals(0,ssr.get_stroke_pos_change())
        self.assertEquals([],ssr.get_ir_pos_updates())

    def test_reset_the_recorder(self):
        ssr = StrokeSensorRecorder()
        ssr.update('800',3)
        ssr.update('810',2)
        ssr.update('820',1)
        ssr.reset_change()
        self.assertEquals(0,ssr.get_stroke_pos_change())
        self.assertEquals([],ssr.get_ir_pos_updates())

if __name__ == "__main__":
    unittest.main()

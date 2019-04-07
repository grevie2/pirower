#! /usr/bin/python3
import unittest
import sys
sys.path.insert(0, '../')

from FlywheelBatchGenerator import FlywheelBatchGenerator

class TestFlywheelBatchGenerator(unittest.TestCase):

    def test_no_revolutions_in_a_sample(self):
        ts_ary = []
        display_sample = 1000
        fbg = FlywheelBatchGenerator(ts_ary, display_sample)       
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 0)
    
    def test_one_revolution_in_a_sample(self):   
        ts_ary = [800]
        display_sample = 1000
        fbg = FlywheelBatchGenerator(ts_ary, display_sample)       
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 1)
        
    def test_multiple_revolutions_in_a_sample(self):   
        ts_ary = [800,810,820]
        display_sample = 1000
        fbg = FlywheelBatchGenerator(ts_ary, display_sample)       
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 3)
    
    def test_multiple_samples(self):    
        ts_ary = [800,810,1800,1810]
        display_sample = 1000
        fbg = FlywheelBatchGenerator(ts_ary, display_sample)       
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 2)  
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 2) 
        
    def test_no_activity_between_samples(self):
        ts_ary = [100,5100]
        display_sample = 1000
        fbg = FlywheelBatchGenerator(ts_ary, display_sample)       
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 1)  
        
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 0)  
        
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 0)  
        
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 0)  
        
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 0)  
        
        current_sample = next(fbg.generate(), 0)         
        self.assertEquals(current_sample, 1)  

if __name__ == "__main__":
    unittest.main()

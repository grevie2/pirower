#! /usr/bin/python3
import unittest
import sys
sys.path.insert(0, '../')

from StrokeBatchGenerator import StrokeBatchGenerator

class TestStrokeBatchGenerator(unittest.TestCase):
		
    def test_two_anticlockwise_turns(self):
        stroke_array = []
        stroke_array.append([800,2])
        stroke_array.append([810,1])
        stroke_array.append([820,3])
        stroke_array.append([830,2])
        stroke_array.append([840,1])
        stroke_array.append([850,3])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-2,current_sample)
        
    def test_full_anticlockwise_turn_partial_clockwise_turn(self):
        stroke_array = []
        stroke_array.append([800,3])
        stroke_array.append([810,2])
        stroke_array.append([820,1])
        stroke_array.append([830,2])
        stroke_array.append([840,3])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample)   
    
    def test_full_anticlockwise_turn_full_clockwise_turn(self):
        stroke_array = []
        stroke_array.append([800,3])
        stroke_array.append([810,2])
        stroke_array.append([820,1])
        stroke_array.append([830,2])
        stroke_array.append([840,3])
        stroke_array.append([850,1])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(0,current_sample) 
    
    def test_partial_anticlockwise_turn(self):
        stroke_array = []
        stroke_array.append([800,2])
        stroke_array.append([810,1])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(0,current_sample)  
        
    def test_one_full_anticlockwise_turn(self):          
        stroke_array = []
        stroke_array.append([800,3])
        stroke_array.append([810,2])
        stroke_array.append([820,1])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample)  
    
    def test_turn_then_no_turn_then_turn(self):
        stroke_array = []
        stroke_array.append([800,3])
        stroke_array.append([810,2])
        stroke_array.append([820,1])
        stroke_array.append([2800,3])
        stroke_array.append([2810,2])
        stroke_array.append([2820,1])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample)  
        
        current_sample = next(sbg, 0)   
        self.assertEquals(0,current_sample)  
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample) 
        
    def test_multiple_full_anticlockwise_turns_spread_over_more_than_1_sample(self):     
        stroke_array = []
        stroke_array.append([800,3])
        stroke_array.append([810,2])
        stroke_array.append([820,1])
        stroke_array.append([1800,3])
        stroke_array.append([1810,2])
        stroke_array.append([1820,1])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample)  
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample)  
        
    def test_clockwise_turn_spread_across_more_than_one_sample(self):
        stroke_array = []
        stroke_array.append([800,3])
        stroke_array.append([810,2])
        stroke_array.append([820,1])
        stroke_array.append([800,2])
        stroke_array.append([810,3])
        stroke_array.append([1110,1])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample)  
        
        current_sample = next(sbg, 0)   
        self.assertEquals(1,current_sample)     
    
    def test_anticlockwise_turn_spread_across_more_than_one_sample(self):
        stroke_array = []
        stroke_array.append([800,3])
        stroke_array.append([810,2])
        stroke_array.append([1110,1])
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(0,current_sample)  
        
        current_sample = next(sbg, 0)   
        self.assertEquals(-1,current_sample) 
    
    #this scenario should never happen unless I forget to attach the IR blocker
    #wheel, or if it falls off before I start
    def test_empty_stroke_array(self):
        stroke_array = []
        display_sample = 1000
        sbg = StrokeBatchGenerator(stroke_array, display_sample)
        
        current_sample = next(sbg, 0)   
        self.assertEquals(0,current_sample)  
    
if __name__ == "__main__":
    unittest.main()

from constants import WIN_HEIGHT, WIN_WIDTH, VIEWABLE_WIDTH_R
   
"""
# given screen width in pixels is 800
# and the screen width in R is 200
# and 4 pixels = 1r
# and the player has travelled 1r
# then mr has shifted left by 1 pixels
# then bg has shifted left by 2 pixels
# then p3 has shifted by 2 pixels
# then p2 has shifted by 6 pixels
# then p1 has shifted left by (the equivalent of 8) pixels, but remains stationary
# then fg has shifted left by 8 pixels
# then mg has shifted left by 16 pixels
"""

#WIDTH_IN_PIXELS = 800
#WIDTH_IN_R = 400
	


#TODO: P3 and P2 really need to be separate classes becasue of the perspective

#TODO: sort this new new ghost method out
#if self.r_x >= viewable_min_r and self.r_x <= viewable_max_r:	
	#temp = viewable_max_r - self.r_x	
	#shouldn't the above line be temp = self.r_x - viewable_min_r yes - i think it should)
#	temp = self.r_x - viewable_min_r
#	self.x = calc_pixel_change(temp)
#	return self.r_x
	

#TODO: make a new get_x_in_pixels and add a commment to make it clear it's not the r_total value that's passed in , but the diff from the stage left r	
#so the r value passed into get_r_in_pixels will be always be a value between 0 and 200 - this is true for ghost players

#TODO: add some test for this as its very complicated
#mr_layer_multiplier = 0.2
#bg_layer_multiplier = 2.5

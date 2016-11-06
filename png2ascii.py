import cv2
import numpy

class png2ascii:

	char_input_arr = []
	threshold_arr = []
	image = []	
	pixel_diversity = 0

	def __init__( self, char_arr, img ):
		self.char_input_arr = char_arr
		self.pixel_diversity = len( char_arr )
		self.image = img		

	def test( self ):
	 	print self.char_input_arr
		print self.pixel_diversity
		print self.image
		cv2.imshow('image',self.image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def resize( self, width, height ):
		self.image = cv2.resize( self.image, ( width, height ) )

	def resize_locked_x( self, width  ):
		current_height, current_width, channels = self.image.shape 
		self.image = cv2.resize( self.image, ( width, int((float(current_height)/current_width) * width)) )
	
	def resize_locked_y( self, height ):				
		current_height, current_width, channels = self.image.shape 
		self.image = cv2.resize( self.image, ( int((float(current_width)/current_height) * height), height) )

	def to_greyscale( self ):
		self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

	def partition_pixels( self ):
		# first we partition the threshhold values from 0 - 255 depending on the pixel diversity
		threshold_arr = []
		for i in range ( 0, self.pixel_diversity ):
			threshold_arr.append( (255/self.pixel_diversity) * (i+1) )
		self.threshold_arr = threshold_arr
		# we now have threshold values..... we will set the pixel values to these values depending on color
		for i in range( 0 , len(self.image) ):
			for j in range( 0, len(self.image[i]) ):
				for x in range ( 0, len(threshold_arr) ):
					if( ( x == 0 and self.image[i][j][0] <= threshold_arr[x])):
						self.image[i][j][0] = threshold_arr[x]-1
						self.image[i][j][1] = threshold_arr[x]-1
						self.image[i][j][2] = threshold_arr[x]-1
					elif( self.image[i][j][0] <= threshold_arr[x] and self.image[i][j][0] >= threshold_arr[x-1]):	
						self.image[i][j][0] = threshold_arr[x]-1
						self.image[i][j][1] = threshold_arr[x]-1
						self.image[i][j][2] = threshold_arr[x]-1


	def ascii_to_file( self, name ):
		complete_string = ""
		for i in range( 0, len(self.image) ):
			for j in range( 0, len(self.image[i]) ):
					for x in range ( 0, len(self.threshold_arr) ):
						if( ( x == 0 and self.image[i][j][0] <= self.threshold_arr[x])):
							complete_string += self.char_input_arr[x]
						elif( self.image[i][j][0] <= self.threshold_arr[x] and self.image[i][j][0] >= self.threshold_arr[x-1]):	
							complete_string += self.char_input_arr[x]
				
			complete_string += "\n"

		#print comlplete_string					
		
		f = open(name, "w")
		f.write(complete_string)
		f.close()


img = cv2.imread("Tux.png");
test = png2ascii( [' ','o', ".", "*", "X"], img )
test.resize_locked_y( 100 )
#test.to_greyscale()
test.partition_pixels()
#test.test()
test.ascii_to_file( "hello" )

import math

class MouseNav:
	def __init__(self):
		self.angle = 0.0
		self.LX = 0.0
		self.LY = 0.0
		self.RX = 0.0
		self.RY = 0.0

	def get_all(self):
		return self.LX, self.LY, self.RX, self.RY, self.angle

	def calc_dxdy(self, acc_LX, acc_LY, acc_RX, acc_RY):
		if(acc_LY == acc_RY):
			return acc_LX, acc_LY, acc_RX, acc_RY, 0
		else:
			fixed_distance = 1.0
			#if the center of rotation occures on either mouse the radius is equal to the fixed distance and we can simplify the math to either case
			if(acc_RY == 0):
				#theta in radians is equal to the arc (accumulated y) divided by the radius (fixed distance)
				theta = acc_LY / fixed_distance
				#solving a simple imaginary triangle gives us the y-part of the curve
				left_y = fixed_distance * math.sin(theta)
				#for the x-part we need the hypotonuse of the imaginary triangle, this can be found using cosine law
				left_x = math.pow( fixed_distance, 2 ) * (1 - math.cos( theta ) ) - left_y * left_y
				right_y = 0
				right_x = 0
			elif(acc_LY == 0):
				#see above
				theta = -acc_RY / fixed_distance
				right_y = fixed_distance * math.sin(theta)
				right_x = math.pow( fixed_distance, 2 ) * (1 - math.cos( theta ) ) - right_y * right_y
				left_y = 0
				left_x = 0
			else:
				#first we figure out the x and y values of the arc (accumulated y)
				#re-arrangment of L/R = (r + D) / r
				radius = (fixed_distance * acc_RY) / (acc_LY - acc_RY)
				#angle measurments done in radians
				theta = acc_LY / (fixed_distance + radius)

				left_y = (fixed_distance + radius) * math.sin(theta)
				left_x = math.pow( fixed_distance + radius, 2) * ( 1 - math.cos( theta ) ) - left_y * left_y
				right_y = radius * math.sin(theta)
				right_x = math.pow( fixed_distance, 2 ) * (1 - math.cos( theta ) ) - right_y * right_y

			#now we add the accumulated x under the assumption that the x value was accumulated evenly accross the time of the arc
			half_theta = theta / 2
			#in theory acc_LX should always equal acc_RX or atleast be within 1-2 dots
			if(acc_LX == acc_RX):
				X = acc_LX
			else:
				X = (acc_LX + acc_RX) / 2
			shift_x = X * math.cos(half_theta)
			shift_y = X * math.sin(half_theta)
			left_dx = left_x + shift_x
			left_dy = left_y + shift_y
			right_dx = right_x + shift_x
			right_dy = right_y + shift_y

			return left_dx, left_dy, right_dx, right_dy, theta

	def adjust_deltas(self, left_dx, left_dy, right_dx, right_dy, theta):
		s = math.sin(self.angle)
		c = math.cos(self.angle)
		self.LX += left_dy * s + left_dx * c
		self.LY += left_dy * c - left_dx * s
		self.RX += right_dy * s + right_dx * c
		self.RY += right_dy * c - right_dx * s
		self.angle -= theta #turning right is positive, left is negative


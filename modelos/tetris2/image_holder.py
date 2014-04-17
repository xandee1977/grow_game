class image_holder(object):
	def __init__(self, image, rect):
		self.image = image
		self.rect = rect
	
	def draw(self, surface):
		return surface.blit(self.image, self.rect)

class Camera(object):
    def __init__(self, x, y, w, h, margin):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.m = margin

    def inCamera(self, x, y, w, h):
        if x+w > self.x-self.m and x < self.x+self.w+self.m \
        and y+h > self.y-self.m and y < self.y+self.h+self.m:
            return True
        return False

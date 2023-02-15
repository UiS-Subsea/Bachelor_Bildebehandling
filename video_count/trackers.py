import math
from collections import OrderedDict

class EuclideanDistTracker:
    def __init__(self):
        self.center_points = {}
        self.idcount = 0

    def update(self, objects_rect):
        objects_bbs_ids = []
        for rect in objects_rect:
            x, y, w, h = rect
            center_x = (x+x + w) // 2
            center_y = (y+y + h) // 2
            same_object_found = False

            for id, point in self.center_points.items():
                distance = math.sqrt(( -point[0]  + center_x)**2 + (-point[1] + center_y)**2)
                if distance < 250:
                    self.center_points[id] = (center_x, center_y)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_found = True
                    break

            if not same_object_found:
                self.center_points[self.idcount] = (center_x, center_y)
                objects_bbs_ids.append([x, y, w, h, self.idcount])
                self.idcount += 1

            new_center_points = {}

            for obj_id in objects_bbs_ids:
                new_center_points[obj_id[4]] = self.center_points[obj_id[4]]

        self.center_points = new_center_points.copy()
        print(objects_bbs_ids)
        # Objects_bbs_ids will look like  [[x, y, w, h, id], [x, y, w, h, id], [x, y, w, h, id]]
        # List of all the bounding boxes and their ids of the objects in the frame
        return objects_bbs_ids




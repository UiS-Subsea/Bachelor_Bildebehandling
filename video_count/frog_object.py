class FrogObject:
    def __init__(self, frogID, centroid):
        # store the object ID, then initialize a list of centroids
        self.frogID = frogID
        self.centroids = [centroid]

        # initialize a boolean used to indicate if the object has been counted or not
        self.counted = False
        
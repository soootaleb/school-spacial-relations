from models.image import Image
from numpy import linspace

class Histogram(object):
    '''
        Represents a single histogram as a data structure.
        The data is stored in the "values" property which is like

        {
            "0": 12,
            "90": 24,
            "180": 0,
            ...
        }

        It's a python dictionary for which
            - the keys are the angle, computed depending on the cardinal with range(0, 360, 360 / self.cardinal)
            - the values are the computed value to display on the histogram, computed by the given relation
        
    '''

    cardinal = 16

    image_a = None
    image_b = None

    relation = None

    values = dict()

    def __getitem__(self, direction):
        return self.values[str(direction)]

    def __init__(self, image_a, image_b):
        if not isinstance(image_a, Image) \
            or not isinstance(image_b, Image):
            
            raise ValueError('Histogram works with two objects of type Image')

        self.image_a = image_a
        self.image_b = image_b

    def set_cardinal(self, cardinal):
        self.values = dict()
        self.cardinal = cardinal
        return self

    @property
    def directions(self):
        return linspace(0, 360, self.cardinal, dtype=int)

    def compute(self, relation):
        '''
            Computes the histogram of the relation depending on the cardinal (default is 16)
        '''

        for angle in self.directions:
            parallels = self.image_a.parallels(angle) # Optimized (0.0003 sec)
            self.values[str(int(angle))] = relation(parallels, self.image_a, self.image_b) # Optimized (0.00001 sec)

        return self

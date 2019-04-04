from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from models.image import Image
from models.histogram import Histogram
from descriptors import *
import relations
from canvas import *

import math, functions, os, sys, cv2 as cv, numpy as np, random

class App(QMainWindow):

    TITLE = 'SpaRe'
    MARGIN_LEFT = 30
    CARDINAL_MAXIMUM = 32
    VARIANCE_MAXIMUM = 50
    
    images = dict()
    variance = 30
    images_canvas = dict()
    image_resize_factor = 1/8

    descriptors = dict()
    histograms_canvas = dict()

    size = { 'WIDTH': 800, 'HEIGHT': 600 }
    position = { 'TOP': 100, 'LEFT': 100 }

    def __init__(self):
        super().__init__()        

        self.load_image('middle.png')
        self.load_image('other.png')

        self.images['merged_images'] = self.images['middle.png'].merge(self.images['other.png'])
        self.images_canvas['merged_images'] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas['merged_images'].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index('merged_images'), 10)

        self.load_descriptors('middle.png', 'other.png')
        
        self.init_ui()
        
        for (fname, image) in self.images_canvas.items():
            image.plot(self.images[fname])

    def init_ui(self):
        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.position['LEFT'], self.position['TOP'], self.size['WIDTH'], self.size['HEIGHT'])

        #DEBUG MODE
        self.radio_segment = QRadioButton("segment",self)
        self.radio_segment.setChecked(True)
        self.radio_segment.move(self.MARGIN_LEFT + 50, 140)

        self.radio_scan_lin = QRadioButton("parralleles", self)
        self.radio_scan_lin.move(250, 140)

        ##HITOGRAM TYPE
        self.check_hist_type = QCheckBox("Polar histogram", self)
        self.check_hist_type.move(self.MARGIN_LEFT + 420, 180)
        self.check_hist_type.setChecked(True)
        self.check_hist_type.resize(150, 20)

        self.check_hist_type.toggled.connect(self.change_hist_type)

        ##CARDINAL
        self.slider_cardinal = QSlider(Qt.Horizontal, self)
        self.slider_cardinal.setMinimum(1)
        self.slider_cardinal.setMaximum(self.CARDINAL_MAXIMUM)
        self.slider_cardinal.setValue(16)
        self.slider_cardinal.setSingleStep(1)
        self.slider_cardinal.move(self.MARGIN_LEFT, 180)
        self.slider_cardinal.resize(300, 20)

        self.label_cardinal = QLabel("16 angle", self)
        self.label_cardinal.move(350, 180)

        self.slider_cardinal.valueChanged.connect(self.slider_cardinal_changed)


        ##VARIANCE 
        self.slider_variance = QSlider(Qt.Horizontal, self)
        self.slider_variance.setMinimum(1)
        self.slider_variance.setMaximum(self.VARIANCE_MAXIMUM)
        self.slider_variance.setValue(self.variance)
        self.slider_variance.setSingleStep(1)
        self.slider_variance.move(self.MARGIN_LEFT, 220)
        self.slider_variance.resize(300, 20)
    
        self.label_variance = QLabel("Variance :{}".format(30), self)
        self.label_variance.move(self.MARGIN_LEFT + 300, 220)

        self.slider_variance.valueChanged.connect(self.slider_variance_changed)        

        ##ANGLE NUMBER : cardinal of the histogram (impacts performances)
        self.slider_angle = QSlider(Qt.Horizontal, self)
        self.slider_angle.setValue(16)
        self.slider_angle.setMinimum(0)
        self.slider_angle.setMaximum(360)
        self.slider_angle.setSingleStep(1)
        self.slider_angle.move(self.MARGIN_LEFT, 120)
        self.slider_angle.resize(300, 20)
        
        
        self.label_angle = QLabel("0 ° rays", self)
        self.label_angle.move(350, 120)

        self.slider_angle.valueChanged.connect(self.slider_angle_changed)        

        ##RESIZE FACTOR : cardinal of the histogram (greatly impacts performances)
        self.slider_resize_factor = QSlider(Qt.Horizontal, self)
        self.slider_resize_factor.setValue(8)
        self.slider_resize_factor.setMinimum(1)
        self.slider_resize_factor.setMaximum(12)
        self.slider_resize_factor.setSingleStep(1)
        self.slider_resize_factor.move(self.MARGIN_LEFT+500, 120)
        self.slider_resize_factor.resize(100, 20)
        
        
        self.label_resize_factor = QLabel('Resize factor {}'.format(str(self.image_resize_factor)), self)
        self.label_resize_factor.move(650, 120)
        self.label_resize_factor.resize(150, 20)

        self.slider_resize_factor.valueChanged.connect(self.slider_resize_changed)        


        ##ROTATION : moving the reference image in a circle
        self.slider_rotate = QSlider(Qt.Horizontal, self)
        self.slider_rotate.setMinimum(-180)
        self.slider_rotate.setMaximum(180)
        self.slider_rotate.setSingleStep(10)
        self.slider_rotate.move(self.MARGIN_LEFT + 150 * len(self.images_canvas.keys()), 50)
        self.slider_rotate.resize(200, 20)
        
        self.label_rotate = QLabel("0° rotation", self)
        self.label_rotate.move(self.MARGIN_LEFT + 150 * len(self.images_canvas.keys()) + 100, 20)

        self.slider_rotate.valueChanged.connect(self.slider_rotate_changed)

        ##TEXT INTERPRETATION : A is reference, B is relative
        self.label_interpretation = QLabel(self)
        self.label_interpretation.resize(600, 50)
        self.label_interpretation.move(self.MARGIN_LEFT, 240)


        self.show()

    def load_descriptors(self, reference, relative):
        desc = reference + relative
        self.descriptors[desc+"1"] = AngularPresenceDescriptor(self.images[reference], self.images[relative], variance= self.variance)
        self.descriptors[desc+"2"] = OverlappingDescriptor(self.images[reference], self.images[relative], variance= self.variance)

        self.histograms_canvas = HistogramCanvas(self, height = 3, width = 6)
        self.histograms_canvas.move(self.MARGIN_LEFT, 280) #+ 220 )* list(self.histograms_canvas.keys()).index("desc"))

    def load_image(self, fname):
        self.images[fname] = Image(fname).resize(self.image_resize_factor)
        self.images_canvas[fname] = ImageCanvas(self, width = 1, height = 1)
        self.images_canvas[fname].move(self.MARGIN_LEFT + 150 * list(self.images_canvas.keys()).index(fname), 10)

    @pyqtSlot()
    def slider_resize_changed(self):
        
        self.image_resize_factor = 1 / self.slider_resize_factor.value()

        self.label_resize_factor.setText('Resize factor 1/{}'.format(str(self.slider_resize_factor.value())))
        
        
        self.images['middle.png'] \
            .reset() \
            .resize(self.image_resize_factor)

        self.slider_rotate_changed()

    @pyqtSlot()
    def slider_rotate_changed(self):
        self.images['other.png'] \
            .reset() \
            .resize(self.image_resize_factor)

        self.images['merged_images'] \
            .reset() \
            .resize(self.image_resize_factor)

        rotation = self.slider_rotate.value()
        self.label_rotate.setText('{}° rotation'.format(rotation))
        self.images['merged_images'] = self.images['middle.png'].merge(self.images['other.png'].rotate(rotation))
        
        self.images_canvas['merged_images'].plot(self.images['merged_images'])
        self.images_canvas['merged_images'].draw()
        self.slider_cardinal_changed()

    @pyqtSlot()
    def slider_cardinal_changed(self):
        self.histograms_canvas.clear()
        cardinal = self.slider_cardinal.value()
        self.label_cardinal.setText('{} angle'.format(cardinal))

        for (dname, descriptor) in self.descriptors.items():
            descriptor.set_cardinal(cardinal) \
                .compute_histogram() \
                .describe()
            texual_interpretation = descriptor.interpret()

            #update textual interpretation
            self.label_interpretation.setText(texual_interpretation)

            #update the histograms values
            self.histograms_canvas.plot(descriptor.histogram)
        

    @pyqtSlot()
    def slider_angle_changed(self):
        self.images['merged_images'].reset()
        
        degree = self.slider_angle.value()
       
        self.label_angle.setText('{} °'.format(degree))
      
        if self.radio_scan_lin.isChecked():
            parallels = self.images['merged_images'].parallels(degree)
            for segment in parallels:
                self.images['merged_images'].draw(segment)
        else:
            segment = self.images['merged_images'].ray(degree)
            self.images['merged_images'].draw(segment)
        
        self.images_canvas['merged_images'].plot(self.images['merged_images'])
        self.images_canvas['merged_images'].draw()

    @pyqtSlot()
    def slider_variance_changed(self):
        '''
        change the variance in the interpretation of the descriptors (as we use gaussian density function)
        '''
        value = self.slider_variance.value()
        self.label_variance.setText("Variance :{}".format(value))
        for  desc in self.descriptors.values():
            desc.set_variance(value) 
        self.slider_cardinal_changed()
    @pyqtSlot()
    def change_hist_type(self):
        '''
            Change the histogram type : polar or linear.
        '''
        is_checked = self.check_hist_type.isChecked()
        
        for (dname, descriptor) in self.descriptors.items():
            self.histograms_canvas.lin_or_polar(is_checked)
            self.histograms_canvas.plot(descriptor.histogram)
        

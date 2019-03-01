# School Spacial Relations

This project aims to work on the fuzzy spacial relations.

# To Do

Those lists are the atomic steps to accomplish in order to produce a graphical application
that allows the user to load two binary images with objects and display the associated F-histogram

## Basic functions

  * ~~Implement the `bresenham` function~~
  * Implement the `scan_linear` function to execute Bresenham on all parallels
  * Implement the `scan_polar` function to execute Bresenham on all angles

## GUI functions

  * ~~Implement the image loading from a button~~ (may be twice for two images)
  * Implement the histogram display - classic
  * Implement the histogram display - radial

## Process functions

  * Move image to binary

# Resources

https://stackoverflow.com/questions/52869400/how-to-show-image-to-pyqt-with-opencv


#Bresenham functions specification

One of the idea we have:

* only to use starting point at (0, 0) in the image
  using only end point on the other side of the image (x = height, or y = height)

  by doing so, we ensure to have always  a segment that have the max lenght of the image, ensuring we can scan the whole image.

  for the other angles, we apply a rotation of a multiple of 90° on the image.
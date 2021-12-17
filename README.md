Picresizer

Python image re-sizing utility that uses Python library Pillow to look at images and 
command line tool ImageMagick to change them.

----------------------------------------------------------

This software has a particular purpose in mind, to convert and resize images 
to a more homogeneous format for posting to a webstore or online catalogue. 

Acknowledging that it's possible to have the online tool prepare images for 
presentation, the reality is that this isn't always an option. 
This software is designed to bridge the shortfall where needed.

Picresizer intends to
- allow user to set a maximum image dimension and reduce images to that size if they exceed it
- allow user to set a minimum image dimension and increase the largest edge to at least that
- allow user to set minimum size
    - and either stretch the image to the minimum size if below, 
    - or apply a canvas grow the image
- allow images to squared off with a white background
- convert images to JPG format
- allow JPG and PNG images to be compressed
- allow images to be stripped of EXIF data to reduce file size

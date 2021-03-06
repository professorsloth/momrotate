import os
import sys
import pyexiv2
import Image

use_new_api = ( pyexiv2.__version__[2] == '3' )

class Photo:
    def __init__(self, photo_path):
        self.allowed_extensions = ['.jpg', '.jpeg']
    
        self.filename = os.path.abspath( photo_path )

        if use_new_api:
            self.exif = pyexiv2.ImageMetadata( self.filename )
            self.exif.read()
        else:
            self.exif = pyexiv2.Image( self.filename )
            self.exif.readMetadata()

        self.image = Image.open( self.filename )
        
    def has_orientation_data(self):
        if use_new_api:
            return ( 'Exif.Image.Orientation' in self.exif.exif_keys )
        else:
            return ( 'Exif.Image.Orientation' in self.exif.exifKeys() )

    def get_orientation(self):
        if not self.has_orientation_data():
            raise Exception("Photo does not contain orientation data.")

        if use_new_api:
            return self.exif['Exif.Image.Orientation'].value
        else:
            return self.exif['Exif.Image.Orientation']

    def is_upright(self):
        self.exif.exif_keys

    def reorient(self, desired_orientation):
        if desired_orientation == 2:
            return self.image.transpose( Image.FLIP_LEFT_RIGHT )
        elif desired_orientation == 3:
            return self.image.transpose( Image.ROTATE_180 )
        elif desired_orientation == 4:
            return self.image.transpose( Image.FLIP_TOP_BOTTOM )
        elif desired_orientation == 5:
            return self.image.transpose( Image.FLIP_TOP_BOTTOM ).transpose( ROTATE_270 )
        elif desired_orientation == 6:
            return self.image.transpose( Image.ROTATE_270 )
        elif desired_orientation == 7:
            return self.image.transpose( Image.FLIP_LEFT_RIGHT ).transpose( Image.ROTATE_270 )
        elif desired_orientation == 8:
            return self.image.transpose( Image.ROTATE_90 )
        else:
            return self.image.copy()
			
    def has_allowed_file_extension(self):
        filname, extension = os.path.splitext( self.filename )
        if extension.lower() in self.allowed_extensions:
            return True
        return False

    def rotate_to_upright(self):
        if( not self.has_orientation_data() or self.is_upright() ):
            return False
        if not self.has_allowed_file_extension():
            return False

        orientation = self.get_orientation()
        self.image = self.reorient( orientation )
        self.image.save( self.filename, "JPEG", quality=90 )

        return True

def list_directory(path):

    if not os.path.exists(path):
        raise Exception("Path does not exist.")

    files = []
    
    for directory_name, directory_names, filenames in os.walk(path):
        for subdirectory_name in directory_names:
            files.append( os.path.join(directory_name, subdirectory_name) )
        for filename in filenames:
            files.append( os.path.join(directory_name, filename) )

    return files

def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s photo_directory' % sys.argv[0])
    directory_path = sys.argv[1]

    photo_paths = list_directory( directory_path )
    for photo_path in photo_paths:
        try:
            photo = Photo( photo_path )
            photo.rotate_to_upright()
        except IOError, e:
            continue

if __name__ == '__main__':
    main()


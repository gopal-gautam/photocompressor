from PIL import Image, ImageFile
from sys import exit, stderr
from os.path import getsize, isfile, isdir, join
from os import remove, rename, walk, stat
from stat import S_IWRITE
from shutil import move
from argparse import ArgumentParser
from abc import ABCMeta, abstractmethod
 
class ProcessBase:
    """Abstract base class for file processors."""
    __metaclass__ = ABCMeta
 
    def __init__(self):
        self.extensions = []
 
    @abstractmethod
    def processfile(self, filename):
        """Abstract method which carries out the process on the specified file.
        Returns True if successful, False otherwise."""
        pass
 
    def processdir(self, path):
        """Recursively processes files in the specified directory matching
        the self.extensions list (case-insensitively)."""
 
        filecount = 0 # Number of files successfully updated
 
        for root, dirs, files in walk(path):
            for file in files:
                # Check file extensions against allowed list
                lowercasefile = file.lower()
                matches = False
                for ext in self.extensions:
                    if lowercasefile.endswith('.' + ext):
                        matches = True
                        break
                if matches:
                    # File has eligible extension, so process
                    fullpath = join(root, file)
                    if self.processfile(fullpath):
                        filecount = filecount + 1
        return filecount
 
class CompressImage(ProcessBase):
    """Processor which attempts to reduce image file size."""
    def __init__(self):
        ProcessBase.__init__(self)
        self.extensions = ['jpg', 'jpeg', 'png']
 
    def processfile(self, filename):
        """Renames the specified image to a backup path,
        and writes out the image again with optimal settings."""
        try:
            # Skip read-only files
            if (not stat(filename)[0] & S_IWRITE):
                print 'Ignoring read-only file "' + filename + '".'
                return False
            
        except Exception as e:
            stderr.write('Skipping file "' + filename + ' ' + str(e) + '\n')
            return False
 
        ok = False
 
        try:
            # Open the image
            with open(filename, 'rb') as file:
                img = Image.open(file)
 
                # Check that it's a supported format
                format = str(img.format)
                if format != 'PNG' and format != 'JPEG':
                    print 'Ignoring file "' + filename + '" with unsupported format ' + format
                    return False
 
                # This line avoids problems that can arise saving larger JPEG files with PIL
                ImageFile.MAXBLOCK = img.size[0] * img.size[1]
                
                # The 'quality' option is ignored for PNG files
                size = 1024, 1024
                wsize , hsize = img.size
                if (wsize > size[0] or hsize > size[0]):
                    img.thumbnail(size, Image.ANTIALIAS)
                img.save(filename, quality=70, optimize=True, dpi=(72,72))
 
            ok = True
        except Exception as e:
            stderr.write('Failure whilst processing "' + filename + '": ' + str(e) + '\n')
       
        return ok
 
if __name__ == "__main__":
    # Argument parsing
    parser = ArgumentParser(description='Reduce file size of PNG and JPEG images.')
    parser.add_argument(
        'path',
         help='File or directory name')

    args = parser.parse_args()

    processor = CompressImage()
 
    # Run according to whether path is a file or a directory
    if isfile(args.path):
        processor.processfile(args.path)
    elif isdir(args.path):
        filecount = processor.processdir(args.path)
        print '\nSuccessfully updated file count: ' + str(filecount)
    else:
        stderr.write('Invalid path "' + args.path + '"\n')
        exit(1)
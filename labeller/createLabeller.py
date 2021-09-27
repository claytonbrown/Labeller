# labellerExec.py
# Author: Marcus D. Bloice <https://github.com/mdbloice>
# Licensed under the terms of the MIT Licence.
import argparse
import sys
import sqlite3
import os
from collections import OrderedDict
import glob
import pkg_resources

# Internal imports
from labeller.htmlElements import Footer, Navbar, Index

parser = argparse.ArgumentParser(description='Generate an image labelling application.', prog='python -m labeller')
# No need to actually pass the number of classes, we just get that from the number of class names
# parser.add_argument('n_classes', metavar='n_classes', type=int, nargs=1, help='the number of classes')
parser.add_argument('class_names', metavar='class_names', nargs='+', help='a list of class names seperated by spaces')
args = parser.parse_args()

# Get the number of classes provided
n_classes = len(args.class_names)

if n_classes <= 1:
    print('Minimum number of classes is 2, you provided %s: %s' % (n_classes, args.class_names))
    sys.exit(1)

#if n_classes != len(args.class_names):
#    print('Number of classes (%s) does equal number of class names provided (%s)' % (n_classes[0], len(args.class_names)))
#    sys.exit(1)

#So far so good
print("Attempting to generate application with %s classes: %s." % (n_classes, ', '.join(args.class_names)))

extensions = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]

im_dir = 'images'

if not os.path.exists(os.path.join('.', im_dir)):
    print("No directory named '%s' found in the current directory: %s). Aborting." % (im_dir, os.getcwd()))
    sys.exit(1)
else:
    print("Found a directory named %s: %s\nSearching for images with the following extensions: %s" % (im_dir, os.path.join(os.getcwd(), im_dir), ' '.join(extensions)))

image_paths = []
for ext in extensions:
    image_paths.extend(glob.glob(os.path.join('.', im_dir, ext)))

if len(image_paths) <= 0:
    print("No images found in %s. Aborting." % os.path.join(os.getcwd(), im_dir))
    sys.exit(1)
else:
    print("Found %s images in %s" %(len(image_paths), os.path.join(os.getcwd(), im_dir)))

print("Generating application with %s classes with the labels %s for %s images." % (n_classes, ', '.join(args.class_names), len(image_paths)))

# The first 9 classes get keyboard shortcuts from 1-9
#classes = OrderedDict()
#classes = {args.class_names[x]:x+1 for x in range(len(args.class_names))}

class TaggerPage():
    def __init__(self, buttons) -> None:
        self.buttons = buttons
    def get_html(self):
        return """
        <!doctype html>

        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Labeller</title>
        <meta name="description" content="A web app for labelling images.">
        <meta name="Labeller">

        </head>

        <body>
        %s
        </body>
        </html>
        """ % " ".join(self.buttons)

# Test of chaining
#print(TaggerPage([Button(btn_label='Label 1').get_html(), Button(btn_label='Label 2').get_html()]).get_html())

# Create a database using the class labels provided
os.makedirs(os.path.join('.', 'db'), exist_ok=True)
conn = sqlite3.connect(os.path.join('.', 'db', 'tags.db'))
conn.execute('CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, image STRING, label INTEGER, label_string STRING)')
conn.close()

# Create directory structure
os.makedirs(os.path.join('.', 'templates'), exist_ok=True)
os.makedirs(os.path.join('.', 'static', 'styles'), exist_ok=True)

# Use pkg_resources to open files or data installed with the package
app_py = pkg_resources.resource_string(__name__, os.path.join('resources', 'app.py'))
dashboard_css = pkg_resources.resource_string(__name__, os.path.join('resources', 'dashboard.css'))
about_html = pkg_resources.resource_string(__name__, os.path.join('resources', 'about.html'))
favicon_ico = pkg_resources.resource_string(__name__, os.path.join('resources', 'favicon.ico'))

# Copy any static files to their appropriate directories
with open(os.path.join('.', 'app.py'), 'wb') as to_write:
    to_write.write(app_py)

with open(os.path.join('.', 'static', 'styles', 'dashboard.css'), 'wb') as to_write:
    to_write.write(dashboard_css)

with open(os.path.join('.', 'static', 'favicon.ico'), 'wb') as to_write:
    to_write.write(favicon_ico)

with open(os.path.join('.', 'templates', 'about.html'), 'wb') as to_write:
    to_write.write(about_html)

# Create any dynamic content here.
footer = Footer()
with open(os.path.join('.', 'templates', 'footer.html'), 'w') as to_write:
    to_write.write(footer.get_html())

navbar = Navbar()
with open(os.path.join('.', 'templates', 'navbar.html'), 'w') as to_write:
    to_write.write(navbar.get_html())

index = Index()
with open(os.path.join('.', 'templates', 'index.html'), 'w') as to_write:
    to_write.write(index.get_html())

# See https://docs.python.org/3/library/__main__.html#module-__main__
# and https://docs.python.org/3/using/cmdline.html#cmdoption-m
# if __name__ == "__main__":
#     print("This is from labellerExec.py")

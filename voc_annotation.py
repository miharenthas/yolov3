import xml.etree.ElementTree as ET
import os
import argparse

ag = argparse.ArgumentParser();
ag.add_argument( '-c', '--classes', nargs='+', dest = 'c', type = str );
ag.add_argument( '-i', '--input-dir', dest = 'id', type = str );
ag.add_argument( '-o', '--output-dir', dest = 'od', type = str );
ag.add_argument( '-s', '--sets', nargs='+', dest = 's', type = str );

args = ag.parse_args();

if args.s:
    sets = args.s
else:
    sets=['train', 'val', 'trainval']

if args.c:
    classes = args.c
else:
    classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

if args.id:
    base_dir = args.d.strip();
else:
    base_dir = 'VOCdevkit/VOC2007/';

if args.od:
    output_dir = args.od.strip();
else:
    output_dir = 'listfiles/';

def convert_annotation( image_id, list_file ):
    in_file = open( base_dir + 'Annotations/%s.xml' % image_id)
    tree=ET.parse(in_file)
    root = tree.getroot()

    size = root.find( 'size' );
    w = int( size.find( 'width' ).text );
    h = int( size.find( 'height' ).text );

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        yolo_box = ( ((b[0]+b[2])/2. - 1.)/w, ((b[1]+b[3])/2. - 1.)/h, (b[2]-b[0])/w, (b[3]-b[1])/h )
        list_file.write( str( cls_id ) + " " + " ".join([str(a) for a in yolo_box]) + '\n' )

if not os.path.exists( output_dir + 'labels/' ):
    os.mkdir( output_dir + 'labels/' );

for image_set in sets:
    image_ids = open( base_dir + 'ImageSets/Layout/%s.txt' % image_set ).read().strip().split()
    for image_id in image_ids:
        list_file = open(output_dir + 'labels/%s.txt'% image_id, 'w')
        convert_annotation( image_id, list_file )
        list_file.close()

class_file = open( output_dir + 'classes.names', 'w' );
for c in classes:
    class_file.write( c + '\n' );
class_file.close();

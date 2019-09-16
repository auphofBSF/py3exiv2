# -*- coding: utf-8 -*-

# tutor.py
#
# This file is part of py3exiv2/docs
#
# Example script of usage of the lib py3exiv2

import sys
import os
import shutil

import datetime

import pyexiv2

from pyexiv2.metadata import ImageMetadata


IMAGE = 'DSCF_0273.JPG'
COPY = 'DSCF_0273(copy).JPG'
THUMB = 'DSCF_0273(thumbnail)'

def get_metadata():
    data = ImageMetadata(COPY)
    data.read()
    return data

def get_maker_infos(data):
    """Returns the camera infos"""
    values = []
    for key in ['Exif.Photo.DateTimeOriginal',
                'Exif.Image.Make',
                'Exif.Image.Model']:
        try:
            values.append(data[key].value)
        except KeyError:
            values.append("Unknow")

    return values

def get_shoot_infos(data):
    """Returns the shooting technical infos."""
    dct = {}
    for name, dkey in {"Exposure time:": "Exif.Photo.ExposureTime",
                       "FNumber:": "Exif.Photo.FNumber",
                       "ISO:": "Exif.Photo.ISOSpeedRatings"}.items():
        try:
            dct[name] = data[dkey].value
        except KeyError:
            dct[name] = "Unknow"

    return dct

def show_author_infos(data):
    """Prints the image's author infos."""
    print('\n Author Informations\n' + '-' * 20)
    try:
        author = data["Exif.Image.Artist"].value
    except KeyError:
        author = ''
    try:
        # Handle a `NotifyingList`
        author1 = " - ".join(data["Iptc.Application2.Byline"].value)
        author1 = " (%s)" % author1
    except KeyError:
        author1 = ''
    author += author1
    if not author:
        author = "Unknow"
    print(' Name:\t\t%s' % author)
    try:
        copy = " - ".join(data["Iptc.Application2.Copyright"].value)
    except KeyError:
        copy = "N-A"
    print(' Copyrights:\t%s' % copy)
    try:
        mail = data['Iptc.Application2.0x00d6'].value
    except KeyError:
        return
    if mail:
        print(' Contact:\t%s' % mail[0])

def show_description(data):
    """Print the scene description."""
    print('\n Scene Description\n' + '-' * 18)
    try:
        scene = " ".join(data['Iptc.Application2.Headline'].value)
    except KeyError:
        scene = "Undefined"
    print(' Title:\t\t%s' % scene)
    try:
        des = " ".join(data['Iptc.Application2.Caption'].value)
    except KeyError:
        des = "Undefined"
    print(' Caption:\t%s' % des)
    try:
        city = " ".join(data['Iptc.Application2.City'].value)
    except KeyError:
        city = "Undefined"
    print(' City:\t\t%s' % city)
    try:
        country = " ".join(data['Iptc.Application2.CountryName'].value)
    except KeyError:
        country = "Undefined"
    print(' Country:\t%s' % country)
    try:
        com = data['Exif.Photo.UserComment'].value
    except KeyError:
        com = 'No comment'
    print(' Comment:\t%s\n' % com)

def print_title(vals):
    line = '-' * len(COPY + str(vals[0])) + '-' * 6
    print('\n  %s  (%s)\n%s\n  %s %s' %(COPY, vals[0], line, vals[1], vals[2]))

def print_data(title, vals):
    print('\n %s\n-%s' %(title, '-'*len(title)))
    for k, v in vals.items():
        print(' %-25s%-11s' %(k, v))

def print_xmp(data):
    print('  XMP Tags\n----------')
    print('  Tag key\t\t\tTag type\t\t  Value\t\t\t\t\t\t\tPython type')
    keys = data.xmp_keys
    keys.sort()
    for key in keys:
        try:
            tag = data[key]
            type_ = tag.type if tag.type else 'text'
            print(' %-28s%-26s%-55s%s' % (key, type_, tag.value, type(tag.value)))
        except Exception as why:
            print('Error: %s\n\t%s' %(key, why))
    tag = data['Exif.Photo.UserComment']
    type_ = tag.type
    print(' %-28s%-26s%-55s%s' % ('Exif.Photo.UserComment', type_, tag.value, type(tag.value)))

def show_preview(data):
    print('  Previews\n----------')
    previews = data.previews
    if previews:
        for idx, preview in enumerate(previews):
            size = '%s x %s' % preview.dimensions
            print(' %s  type: %s  size: %s' %(idx+1, preview.mime_type, size))
        try:
            previews[0].write_to_file(THUMB)
            print(" Preview 1 saved to %s.jpg\n" % THUMB)
        except Exception as why:
            print(" Can't save the preview, reason: %s\n" % why)
    else:
        print(' No preview\n')

def create_new_data(data):
    # A Dublin Core namespace type `bag text`
    key = 'Xmp.dc.subject'
    # Play with non-ASCII
    value = ['Андрей', 'Иван', 'Тарас']
    data[key] = value
    # Create a new namespace
    pyexiv2.xmp.register_namespace('www.py3exiv2.org/', 'tutor')
    key = 'Xmp.tutor.lastEditDate'
    # Try with a date
    data[key] = datetime.datetime.today()
    # An other one new key
    key = 'Xmp.tutor.lastEditorName'
    # A langage written from right to left
    value = ' אלעד גרשגורן'
    data[key] = value
    data['Exif.Photo.UserComment'] = "Commentaire à èèèééïç accentué"

def main():
    # First, make a copy of our original image
    shutil.copy(IMAGE, COPY)
    # Get the image metadata
    data = get_metadata()
    print_title(get_maker_infos(data))
    show_author_infos(data)
    print_data('Shooting Informations', get_shoot_infos(data))
    show_description(data)
    show_preview(data)
    create_new_data(data)
    print('Write new data to the file and reload the metadata ...\n')
    # Apply the new tags to the file
    data.write()
    # Reload the data
    data = get_metadata()  
    print_xmp(data)

if __name__ == '__main__':
    main()




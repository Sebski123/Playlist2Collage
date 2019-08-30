from PIL import Image
import os
import argparse


def make_square(im, filename, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    new_im.save("./squared/{}.png".format(filename))


def main():
    
    parse = argparse.ArgumentParser(description='Makw images square')
    parse.add_argument('-f', '--folder', dest='folder', help='folder with images (*.jpg, *.jpeg, *.png)', default='.')

    args = parse.parse_args()
    
    # get images
    files = [os.path.join(args.folder, fn) for fn in os.listdir(args.folder)]
    images = {}
    for image in files:
        images[os.path.splitext(image)[0].split("\\")[-1]] = image

    if not os.path.exists('squared'):
        os.makedirs('squared')
    
    if not images:
        print('No images found! Please select other directory with images!')
        exit(1)
    
    for key in images.keys():
        make_square(Image.open(images[key]), key)



if __name__ == '__main__':
    main()
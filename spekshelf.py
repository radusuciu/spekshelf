from PIL import Image
from itertools import cycle
import statistics
import pathlib
import math
import click

SCALE_MAX = 22
SCALE_MIN = 0

@click.command()
@click.argument('files', nargs=-1, help='Files to determine shelf frequency for.', type=click.Path(exists=True, dir_okay=False))
def main(files):
    for file in files:
        process(file)

def process(file):
    box = (61, 61, 867, 892)
    im = Image.open(file).convert('L').crop(box)

    pixels = list(im.getdata())
    width, height = im.size

    # average horizontal stripes
    stripes = [statistics.mean(pixels[i * width:(i + 1) * width]) for i in range(height)]

    max_delta = 0
    slope_index = 0

    for i, el in enumerate(stripes):
        try:
            delta = stripes[(i + 1) % len(stripes)]  / el 
            if delta > max_delta:
                slope_index = i
                max_delta = delta
        except ZeroDivisionError:
            pass

    shelf = SCALE_MAX - (slope_index / im.height * (SCALE_MAX - SCALE_MIN))

    return math.floor(shelf)


if __name__ == 'main':
    main()

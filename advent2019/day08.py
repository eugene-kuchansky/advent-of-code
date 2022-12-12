from typing import List
from collections import Counter
from operator import itemgetter


BLACK = "0"
WHITE = "1"
TRANSPARENT = "2"

def split_layers(data: List[str], width: int, height: int) -> List[List[str]]:
    layers = []
    layer_size = width * height
    for x in range(0, len(data), layer_size):
        layer = data[x:x + layer_size]
        layers.append(layer)
    return layers


def calc1(layers: List[List[str]]) -> int:
    counters = []
    for layer in layers:
        cnt = Counter(layer)
        counters.append(cnt)
    target_layer_counter = sorted(counters, key=itemgetter("0"))[0]
    res = target_layer_counter["1"] * target_layer_counter["2"]
    return res


def calc2(layers: List[List[str]], width: int, height: int) -> List[str]:
    final_image = []
    for i in range(width * height):
        pixels = [layer[i] for layer in layers]
        for layer_pixel in pixels:
            if layer_pixel in (BLACK, WHITE):
                pixel = layer_pixel
                break
        else:
            pixel = TRANSPARENT
        final_image.append(pixel)

    return final_image


def show_image(image: List[str], width: int) -> None:
    for x in range(0, len(image), width):
        line = "".join("\33[37m" + "*" + '\033[0m' if pixel == WHITE else '\33[30m' + " " + '\033[0m' for pixel in image[x:x + width])
        print(line)

# image_data = list("123456789012")
# print(image_data)
with open("8.txt") as f:
    image_data = list(f.read().strip())

layers = split_layers(image_data, 25, 6)
res = calc1(layers)
print(res)
image = calc2(layers, 25, 6)
show_image(image, 25)

import sys
from PIL import Image


def main():
	images = map(Image.open, ['E0_01.png','E0_05.png','E0_10.png'])
	widths, heights = zip(*(i.size for i in images))

	total_width = max(widths)
	max_height = sum(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	y_offset = 0
	for im in images:
	  new_im.paste(im, (0,y_offset))
	  y_offset += im.size[1]

	new_im.save('errors.png')

	images = map(Image.open, ['L100.png','L500.png','L1000.png'])
	widths, heights = zip(*(i.size for i in images))

	total_width = max(widths)
	max_height = sum(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	y_offset = 0
	for im in images:
	  new_im.paste(im, (0,y_offset))
	  y_offset += im.size[1]

	new_im.save('lengths.png')

if __name__ == "__main__":
	main()
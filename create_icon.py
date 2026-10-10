from PIL import Image, ImageDraw

WIDTH = 256
HEIGHT = 256
img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Background blue rounded square
margin = 18
draw.rounded_rectangle(
    [margin, margin, WIDTH - margin, HEIGHT - margin],
    radius=48,
    fill=(30, 99, 235, 255),
)

# White stylized lightning / schematic symbol
# Main vertical stem
draw.rectangle([108, 36, 148, 175], fill=(255, 255, 255, 255))
# Top diagonal branch
draw.polygon([(148, 36), (180, 90), (152, 90), (190, 170), (108, 170), (126, 118), (106, 118)], fill=(255, 255, 255, 255))

# Small connector dots
for x, y in [(56, 96), (200, 96), (128, 206), (128, 48)]:
    draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 255, 255, 255))

img.save("app.ico")
print("Created app.ico")

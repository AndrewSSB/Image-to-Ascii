from PIL import Image, ImageDraw, ImageFont

density = 'Ñ@#W$9876543210?!abc;:+=-,._        '
charArray = list(density)
charLength = len(charArray)
scale_factor = 0.5 #scale of the image

oneCharWidth = 10 #giving the idea of a grid with a 10x10 each square to display characters nicely
oneCharHeight = 18

ascii_vals_brightness = {}
val = 0
increment = 255 // charLength

for x in charArray:
    ascii_vals_brightness[(val, val + increment)] = x #dictionary of intervals for each character
    val += increment + 1                              #Example: (0, 10) = Ñ
                                                      #         (11, 20) = @ etc

def getChar(inputInt): #function that takes an integer and returns a character based on the interval that belongs
    for low, high in ascii_vals_brightness.keys():
        if low <= inputInt <= high:
            return ascii_vals_brightness[(low, high)]

text_file = open("ascii_image.txt", "w")

im = Image.open("images.jpg")

fnt = ImageFont.truetype("C:\\Users\\enean\\Desktop\\Python Projects\\ImageToAscii\\Lucon.ttf", 15) #This is a font to write over an image

width, height = im.size
im = im.resize((int(scale_factor * width), int(scale_factor * height*(oneCharWidth/oneCharHeight))), Image.NEAREST) #resize based on the scale and the width and length of a charcacter
new_width, new_height = im.size #store the new size
pix = im.load() #load the image

outputImage = Image.new('RGB', (oneCharWidth * new_width, oneCharHeight * new_height), color=(0,0,0)) #create a new black image for drawing the characters
d = ImageDraw.Draw(outputImage)

for i in range(new_height):
    for j in range(new_width):
        r, g, b = pix[j, i]
        avg = int(r/3+g/3+b/3) #with this we convert the image to gray scale
        pix[j, i] = (avg, avg, avg)
        text_file.write(getChar(avg)) #write into file
        d.text((j*oneCharWidth, i * oneCharHeight), getChar(avg), font=fnt) #write into image (i * onecharwidth and j * onecharheight to have space between them, otherwise they would be like that: 12414!?)

    text_file.write('\n')

outputImage.save('output.png')

#Nokia 5110LCD Driver - Hardware SPI
#Author - matneee (Martin Allen) 20 Apr 2017, matneee@willitwork.co.uk

#Pin configuration for LCD -> microbit;
#RST -> PIN0
# CE -> PIN1
# DC -> PIN8
#DIN -> PIN15
#CLK -> PIN13
#VCC -> 3V, AND BL / GND TO GROUND (BL MAY GO TO 3V DEPENDING ON YOUR OWN LCD)

#The LCD is 84 x 48 pixels, broken up into 6 horizontal banks of 84 width & 8 height
#Each byte written to the LCD populates a column of 8 pixels in the current bank, then it moves to the next column of 8
#Once all 84 pixel columns are filled in one bank, it moves to the first pixel column on the next bank down.
#Once the final bank is filled, it returns to the start of the top bank

from microbit import *
import array
import gc

#127 character ascii font, 5x8 size characters
font = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x5f\x00\x00\x00\x07\x00\x07\x00\x14\x7f\x14\x7f\x14\x24\x2a\x7f\x2a\x12\x23\x13\x08\x64\x62\x36\x49\x55\x22\x50\x00\x05\x03\x00\x00\x00\x1c\x22\x41\x00\x00\x41\x22\x1c\x00\x14\x08\x3e\x08\x14\x08\x08\x3e\x08\x08\x00\x50\x30\x00\x00\x08\x08\x08\x08\x08\x00\x60\x60\x00\x00\x20\x10\x08\x04\x02\x3e\x51\x49\x45\x3e\x00\x42\x7f\x40\x00\x42\x61\x51\x49\x46\x21\x41\x45\x4b\x31\x18\x14\x12\x7f\x10\x27\x45\x45\x45\x39\x3c\x4a\x49\x49\x30\x01\x71\x09\x05\x03\x36\x49\x49\x49\x36\x06\x49\x49\x29\x1e\x00\x36\x36\x00\x00\x00\x56\x36\x00\x00\x08\x14\x22\x41\x00\x14\x14\x14\x14\x14\x00\x41\x22\x14\x08\x02\x01\x51\x09\x06\x32\x49\x79\x41\x3e\x7e\x11\x11\x11\x7e\x7f\x49\x49\x49\x36\x3e\x41\x41\x41\x22\x7f\x41\x41\x22\x1c\x7f\x49\x49\x49\x41\x7f\x09\x09\x09\x01\x3e\x41\x49\x49\x7a\x7f\x08\x08\x08\x7f\x00\x41\x7f\x41\x00\x20\x40\x41\x3f\x01\x7f\x08\x14\x22\x41\x7f\x40\x40\x40\x40\x7f\x02\x0c\x02\x7f\x7f\x04\x08\x10\x7f\x3e\x41\x41\x41\x3e\x7f\x09\x09\x09\x06\x3e\x41\x51\x21\x5e\x7f\x09\x19\x29\x46\x46\x49\x49\x49\x31\x01\x01\x7f\x01\x01\x3f\x40\x40\x40\x3f\x1f\x20\x40\x20\x1f\x3f\x40\x38\x40\x3f\x63\x14\x08\x14\x63\x07\x08\x70\x08\x07\x61\x51\x49\x45\x43\x00\x7f\x41\x41\x00\x02\x04\x08\x10\x20\x00\x41\x41\x7f\x00\x04\x02\x01\x02\x04\x40\x40\x40\x40\x40\x00\x01\x02\x04\x00\x20\x54\x54\x54\x78\x7f\x48\x44\x44\x38\x38\x44\x44\x44\x20\x38\x44\x44\x48\x7f\x38\x54\x54\x54\x18\x08\x7e\x09\x01\x02\x0c\x52\x52\x52\x3e\x7f\x08\x04\x04\x78\x00\x44\x7d\x40\x00\x20\x40\x44\x3d\x00\x7f\x10\x28\x44\x00\x00\x41\x7f\x40\x00\x7c\x04\x18\x04\x78\x7c\x08\x04\x04\x78\x38\x44\x44\x44\x38\x7c\x14\x14\x14\x08\x08\x14\x14\x18\x7c\x7c\x08\x04\x04\x08\x48\x54\x54\x54\x20\x04\x3f\x44\x40\x20\x3c\x40\x40\x20\x7c\x1c\x20\x40\x20\x1c\x3c\x40\x30\x40\x3c\x44\x28\x10\x28\x44\x0c\x50\x50\x50\x3c\x44\x64\x54\x4c\x44\x00\x08\x36\x41\x00\x00\x00\x7f\x00\x00\x00\x41\x36\x08\x00\x10\x08\x08\x10\x08\x00\x00\x00\x00\x00')

#Initialisation codes to be written for startup
LInit = bytearray(b'\x21\xBF\x04\x14\x0C\x20\x0C')

# Set up SPI interface
spi.init(baudrate = 328125, sclk = pin13, mosi = pin15)


#Write data to LCD via SPI.
#The LCD uses its DC input (pin8) to diffenentiate between COMMAND instructions (dc = 0) and DATA instructions (dc = 1)
#To write to the LCD, CE needs to be set to 0. While CE is on, the LCD will not accept any instructions
#Data is fed into a bytearray buffer,  then written to the LCD via SPI
#Finally CE is reset to 1, to indicate no further instructions
def LWrt(dc, data):
    pin8.write_digital(dc)
    pin1.write_digital(0)
    try:
        buff = bytearray (len(data))
    except TypeError:
        buff = bytearray(1)
    try:
        buff = data[:]
    except TypeError:
         buff = data
    spi.write(buff)
    pin1.write_digital(1)
    return


#Clear Screen
#Simply sends a series of zeros to be written to the LCD
def LClear():
    data = bytearray(504)
    LWrt(1, data)
    return


#Print Message - expects a text string in quotes as argument
#Converts each letter to its ASCII value, then looks up the corresponding 5 bytes for that letter in the font bytearray
#Standard ascii characters start at 32, hence subtract 32 from the value to correspond with the font bytearray starting at 0
#Font characters are 5 bytes long, and a further blank byte is added to each character as 1 pixel of padding
def LPrint (message):
    text = bytearray()
    for letter in message:
        i = (ord(letter) - 32) * 5
        for b in range (0,5):
            text.append(font[i+b])
        text.append(0x00)
    LWrt(1, text)
    return

     
#Load a bitmap to the screen (See PCD8544 for bitmap formatting)     
def LGraph(graph):
    LWrt(1,graph)
    return


#Send a COMMAND instruction   
def LCommand(value):
    LWrt(0,value)
    return
 

#Set the screen Y coordinate
#Expects an int of 0-5
def LSetY(y):
    val = bytearray()
    val.append (0x40 + y)
    LCommand(val)


#Set the screen X coordinate
#Expects an int of 0-83
def LSetX(x):
    val = bytearray()
    val.append (0x80 + x)
    LCommand(val)
    return


#Run at startup
pin0.write_digital(0)
pin0.write_digital(1)
LCommand(LInit)
LClear()
LPrint("Hello World")
LSetY(2)
LSetX(25)
LPrint("More Text!")

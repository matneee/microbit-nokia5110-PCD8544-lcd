#Nokia 5110LCD Driver - Hardware SPI,
#
#Font is held in I2C EEPROM chip (an 24lc128 in this case)
#
#Author - @matneee 29 Apr 2017

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

#96 standard ascii characters are stored on EEPROM
#each character 5 bytes (and thus 5 pixels) wide

#Pin configuration for EEPROM -> microbit:
#1 -> GND
#2 -> GND
#3 -> GND
#4 -> GND
#5 -> 20 (SDA)
#6 -> 19 (SCL)
#7 -> GND
#8 -> 3V

from microbit import *

#function for reading from EEPROM
def reep(eepAdr, num = 1):
    data = bytearray(2)
    data[0]=eepAdr >> 8
    data[1]=eepAdr & 0xFF
    i2c.write(0x50, data)
    value = (i2c.read(0x50, num, repeat=False))
    return value[:]

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
    spi.write(data)
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
            val = ord(reep(i+b))
#            text.append(font[i+b])
            text.append(val)

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

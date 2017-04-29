# microbit-nokia5110-PCD8544-lcd
A Fast Micro:bit micropython controller for Nokia 5110 LCDs

This is a collection of micropython scripts for controlling Nokia 5110 LCD screens (PCD8544 chip) on a Micro:bit. In order to achieve useful speeds, the Micro:bit's SPI interface is used.

The code is configured with the following LCD to Microbit connections in mind:

RST -> PIN0
 CE -> PIN1
 DC -> PIN8
DIN -> PIN15 (MOSI)
CLK -> PIN13 (SCK)
  and the power pins configured as per your particular LCD. On mine this is
  VCC -> 3V
  BL -> GND
  GND - GND
  although from what I understand it varies between LCDs whether the BL backlight pin should be connected to 3v or GND.
  
    Full hardware technical details are to be found in PCD8544LCD_manual.pdf
    
################

N5110_LCD_SPI.py
Text functions for the LCD. This includes a full 127 character ascii font, basic screen positioning, clearing etc.
This does not use a ser framebuffer per se - although one could be added if desired, for my purposes it wasn't really necessary. The Uridium demo gives an example of a more constant framebuffer being used
    
################

N5110_LCD_EEPROM.py
Essentially the same as N5110_LCD_SPI, *except* instead of being stored as a bytearray in the program, the font is stored on an EEPROM chip connected to the Micro:bit. This saves around half a kilobyte, which is a fairly significant amount considering the free memory available. Note that the same could be done to store any bitmaps required, opening up posibilities for relatively large numbers of bitmaps, or spritesheets for varied animation etc. EEPROM is quite cost effective (about 30p), and does not impact free memory in the way that opening  a file for reading could.

Note that this REQUIRES you to first have the font on an EEPROM chip - instructions for doing so can be found here - https://github.com/matneee/microbit-I2C-EEPROM-24LCxxx-Read-Write

################
  
uridium-demo.py
This is a demo to illustrate the use of the LCD as a graphical display. Essentially it works by creating  a framebuffer that is 6 horizontal strips of 8 x 84 pixels. 
  The list "Pics" contains 2 images in bytearray form (0-6 is image 1, 6-11 is image 2). 
  The LScrollL and LScrollR functions read the relevant sections of each image into the framebuffer. This then uses the SPI interface to
  write the framebuffer to the LCD.
I apologise for the lack of comments in this file, but it's really scraping the limits of what size can currently be uploaded to the microbit. I genuinely had to strip the comments out to get it to run!
  

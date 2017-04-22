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

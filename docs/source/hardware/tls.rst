===============
Adafruit TSL2561 Digital Luminosity/Lux/Light Sensor Breakout
===============

.. image :: /_static/imgs/tls.jpg


DESCRIPTION
-----

The TSL2561 luminosity sensor is an advanced digital light sensor, ideal for use in a wide range of light situations. Compared to low cost CdS cells, this sensor is more precise, allowing for exact lux calculations and can be configured for different gain/timing ranges to detect light ranges from up to 0.1 - 40,000+ Lux on the fly. The best part of this sensor is that it contains both infrared and full spectrum diodes! That means you can separately measure infrared, full-spectrum or human-visible light. Most sensors can only detect one or the other, which does not accurately represent what human eyes see (since we cannot perceive the IR light that is detected by most photo diodes)

New! As of June 3, 2014 we are shipping a version with a 3.3V regulator and level shifting circuitry so it can be used with any 3-5V power/logic microcontroller.

The sensor has a digital (i2c) interface. You can select one of three addresses so you can have up to three sensors on one board - each with a different i2c address. The built in ADC means you can use this with any microcontroller, even if it doesn't have analog inputs. The current draw is extremely low, so its great for low power data-logging systems. about 0.5mA when actively sensing, and less than 15 uA when in powerdown mode.

Of course, we wouldn't leave you with a datasheet and a "good luck!" - we wrote a detailed tutorial showing how to wire up the sensor, use it with an Arduino and example code that gets readings and calculates lux



TECHNICAL DETAILS
-----
 
Approximates Human eye Response
Precisely Measures Illuminance in Diverse Lighting Conditions
Temperature range: -30 to 80 *C
Dynamic range (Lux): 0.1 to 40,000 Lux
Voltage range: 2.7-3.6V
Interface: I2C
This board/chip uses I2C 7-bit addresses 0x39, 0x29, 0x49, selectable with jumpers
Downloads:

Datasheet
Arduino library and example code on github
To download. click the DOWNLOADS button in the top right corner, rename the uncompressed folder TSL2561. Check that the TSL2561 folder contains TSL2561.cpp and TSL2561.h
Place the TSL2561 library folder your /libraries/ folder. You may need to create the libraries subfolder if its your first library. Restart the IDE.
PCB layout files - public domain
We have a detailed tutorial showing how to wire up the sensor, use it with an Arduino and example code that gets readings and calculates Lux

LEARN
-----

TODO

Read More
-----

* http://www.adafruit.com/products/439
* https://learn.adafruit.com/tsl2561/
* https://github.com/adafruit/Adafruit_TSL2561
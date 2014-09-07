=================
CDS
=================

CdS cells are little light sensors. As the squiggly face is exposed to more light, the resistance goes down. When its light, the resistance is about 5-10KΩ, when dark it goes up to 200KΩ.

To use, connect one side of the photo cell (either one, its symmetric) to power (for example 5V) and the other side to your microcontroller's analog input pin. Then connect a 10K pull-down resistor from that analog pin to ground. The voltage on the pin will be 2.5V or higher when its light out and near ground when its dark.

.. image :: /_static/imgs/cds.jpg

Connecting CDS
""""""

.. image :: img/light_cds.gif

.. code-block:: javascript

	/* Photocell simple testing sketch. 
	 
	Connect one end of the photocell to 5V, the other end to Analog 0.
	Then connect one end of a 10K resistor from Analog 0 to ground 
	Connect LED from pin 11 through a resistor to ground 
	For more information see http://learn.adafruit.com/photocells */
	 
	int photocellPin = 0;     // the cell and 10K pulldown are connected to a0
	int photocellReading;     // the analog reading from the sensor divider
	int LEDpin = 11;          // connect Red LED to pin 11 (PWM pin)
	int LEDbrightness;        // 
	void setup(void) {
	  // We'll send debugging information via the Serial monitor
	  Serial.begin(9600);   
	}
	 
	void loop(void) {
	  photocellReading = analogRead(photocellPin);  
	 
	  Serial.print("Analog reading = ");
	  Serial.println(photocellReading);     // the raw analog reading
	 
	  // LED gets brighter the darker it is at the sensor
	  // that means we have to -invert- the reading from 0-1023 back to 1023-0
	  photocellReading = 1023 - photocellReading;
	  //now we have to map 0-1023 to 0-255 since thats the range analogWrite uses
	  LEDbrightness = map(photocellReading, 0, 1023, 0, 255);
	  analogWrite(LEDpin, LEDbrightness);
	 
	  delay(100);
	}

Source
------

* https://learn.adafruit.com/photocells/using-a-photocell
* http://www.adafruit.com/products/161
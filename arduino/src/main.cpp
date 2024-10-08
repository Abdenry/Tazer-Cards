#include <Arduino.h>
#include <MCP4251.h>
#define numBytes 5

char data[numBytes];
int player = 0;
int damage = 0;
int numSize = 0;

void setup()
{
	Serial.begin(9600);
	MCP4251init();
	MCP4251writeData(WIPER0ADD, 0);
	MCP4251writeData(WIPER1ADD, 0);
	DDRD |= (1 << 2);
	DDRD |= (1 << 3);
	PORTD &= ~(1 << 2);
	PORTD &= ~(1 << 3);
}

void loop()
{
	if (Serial.available() > 0)
	{
		damage = 0;
		memset(data, 0, numBytes);
		numSize = Serial.readBytesUntil('\n', data, numBytes);

		// Select player
		if ((data[0] - '0') == 1)
		{
			player = 1;
		}
		else
		{
			player = 2;
		}

		// Concatenate byte array to form single numer
		switch (numSize)
		{
		case 3:
			damage = data[2] - '0';
			numSize = 0;
			break;
		case 4:
			damage = (data[2] - '0') * 10 + (data[3] - '0');
			numSize = 0;
			break;
		case 5:
			damage = (data[2] - '0') * 100 + (data[3] - '0') * 10 + (data[4] - '0');
			numSize = 0;
			break;
		default:
			numSize = 0;
			break;
		}

		// Damage the selected player
		if (player == 1)
		{
			PORTD |= (1 << 2);
			delay(200);
			PORTD &= ~(1 << 2);
			delay(100);

			PORTD |= (1 << 2);
			delay(200);
			PORTD &= ~(1 << 2);
			delay(100);

			PORTD |= (1 << 2);
			delay(200);
			PORTD &= ~(1 << 2);

			MCP4251writeData(WIPER0ADD, damage);
			delay(1000);
			MCP4251writeData(WIPER0ADD, 0);
			player = 0;
		}
		else if (player == 2)
		{
			PORTD |= (1 << 3);
			delay(200);
			PORTD &= ~(1 << 3);
			delay(100);

			PORTD |= (1 << 3);
			delay(200);
			PORTD &= ~(1 << 3);
			delay(100);

			PORTD |= (1 << 3);
			delay(200);
			PORTD &= ~(1 << 3);

			MCP4251writeData(WIPER1ADD, damage);
			delay(1000);
			MCP4251writeData(WIPER1ADD, 0);
			player = 0;
		}
	}
}
from machine import Pin, SoftI2C
import ssd1306

# Initialize I2C interface with the correct pins for your setup
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))

# Initialize SSD1306 OLED display
oled_width = 128
oled_height = 32  # Adjusted for 128x32 OLED display
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


def update_display(line1, line2="Default Line 2", line3="Default Line 3"):
    # Clear the display
    oled.fill(0)

    # Display the provided text
    oled.text(line1, 0, 0)
    oled.text(line2, 0, 10)
    oled.text(line3, 0, 20)

    # Update the display
    oled.show()
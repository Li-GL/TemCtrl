# TemperatureControl
To set and read temperature from temperature-control device via serial communication

I. Main function

1. set the temperature whenever press ENTER

2. read the temperature

3. write data to csv file in "temperatureData" folder of current path

4. To exit, press ESC, then Ctrl + C


II. To compile using Pyinstaller 3.1 (Pyinstaller 3.2 won't work, seems bug there)

  command for UPX compressed, custom icon as below:

  pyinstaller --upx-dir=C:\Python27\UPX -F -i test.ico TemCtrl.py

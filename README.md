Title:
Main.py - Calculation of Pollutant Concentrations Under Adverse Weather Conditions

Description:
This repository contains the main.py file, which is a Python script that takes information from the dlya_rasschetov.txt file and calculates concentrations of pollutants under various weather conditions. The script considers parameters such as wind speed, wind direction, and pollutant characteristics to determine the maximum concentration and distance at which it occurs.

dlya_rasschetov.txt:
The dlya_rasschetov.txt file is a structured dataset with the following columns:

Source Number
Source Height (in meters)
Mouth Length (in meters)
Mouth Width (in meters)
Exit Rate of Gas-Air Mixture from the Source (in meters per second)
Flow of Gas-Air Mixture at the Source (in cubic meters per second)
Temperature of the Gas-Air Mixture (in degrees Celsius)
Pollutant Code according to SanPiN 1.2.3685-21 and Letters from the Atmosphere Research Institute regarding pollutant codes (10.03.2021 № 10-2-180/21-0 and 16.03.2021 № 10-2-201/21-0)
Name of the Pollutant
Coefficient that Takes into Account the Rate of Settling of the Pollutant
Power Source Emission of Pollutants (in grams per second)
Concentration of Pollutants in the Gas-Air Mixture (in milligrams per cubic meter)
Gross Source Emission of Pollutants (in tons per year)

Key Features:
Calculates pollutant concentrations under different weather conditions
Determines the wind speed at which pollutant concentration is maximal
Establishes the distance at which the maximum concentration occurs


# CPU Temperature Monitor

![App Screenshot](resources/app_screenshot.png)

## Background Info
My Lenovo T430 laptop heats up *alot* to the point where it shuts down without warning. Alot means 115 °C.
It doesn't always heat up that much, but when it does, it does so without warning, and I have lost data
because of it.

It heats up because it is connected to 3 monitors via a docking station which obstructs much of the cooling
ports. Silly design if you ask me, but alas laptops also were not designed to be used as desktops the way
I am using it.

## What this does
This applet reads my CPU temperatures every 2 seconds, and displays them. If the largest of the two
temperatures exceeds a "High" temperature threshold, it blares a siren and generates a desktop
notification.

The siren stops when the highest of the two core temperatures drops below a "Low" temperature threshold.

## Why this is useful
My computer doesn't always heat up obnoxiously to the point where it shuts down. It usually does so
if I'm gaming, or if I'm doing heavy media rendering like using CAD software or watching cat videos
during ~boring zoom meetings~ online classes.

When the siren activates, I use my can of compressed air to rapidly cool down my computer to a nominal
level. Is it the smartest solution? Probably not. But using a laptop cooler and keeping the laptop lid
open all the time actually isn't as helpful as one would expect, and I *need* my laptop to work as a desktop
because I also need it to work as a laptop when I go to school. So this is currently the best solution
¯\_(ツ)_/¯

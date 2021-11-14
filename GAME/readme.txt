#unzip the Roboto_Condensed.zip and extract the contents
I downloaded it from https://fonts.google.com/specimen/Roboto+Condensed#glyphs

#copy the true type fonts to the pi
sudo cp * /usr/local/share/font

#copy the GAME folder to the home folder on the PI

#add a command to .bashrc to instruct the game to run on startup
>sudo mousepad /home/pi/.bashrc
and add the following lines
cd /home/pi/GAME
sudo python pirower.py

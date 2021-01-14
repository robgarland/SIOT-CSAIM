# SIOT-CSAIM

My Sensing and IOT project based on creating a performance/game improvement tool for eSports players in CS:GO.

The project uses an accelerometer sensor found on the front of the mouse to get live information about changes in mouse direction and movement patterns combined with live data taken from inside the Counter-Strike:Global Offensive game itself in order to provide the player with insights for game improvement through some simple ML tools.

# File Structure

App Files <br />
repo location : main <br />
index.py <br />
  dashboard.py <br />
  navbar.py <br />
  apptest.py <br />
  dataanaysis.py <br />
  getpositions.py <br />
  faceit.py <br />
<br />
Storage <br />
repo location : main <br />
acceldata2.csv <br />
gamestatedata2.csv <br />
<br />
RaspberryPi <br />
repo location : main <br />
SIOTmain.py <br />
<br />
Gamestate Integration <br />
repo location: csgo-gsi-python-master/csgo-gsi-python/ <br />
server.py <br />
payloadparser.py <br />
information.py <br />
gamestate.py <br />
infogetter3.1.py <br />
repo loaction : csgo-gsi-python-master/ <br />
gamestate_integration_GSI.cfg <br />
<br />
Arduino Code <br />
repo location: main <br />
MMA8451test.ino <br />


 

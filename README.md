# europe_gliding_waypoints
This repository contains a python-script, which downloads the latest waypoint-data 
from the openflightmaps- and the XCsoar-Homepage.

The downloaded data is parsed into a cup-file, which can be utilized in several applications like XCsoar, an OUDIE, etc.
By using this script and the resulting file, the user does not have to switch between multiple cup-files during flight if
borders are crossed and the script automatically retrieves actively updated data. 
Thus, all frequencies should be up-to-date all the time.

The output-file can be found under /res/output/europe.cup. 
All directories are created automatically by the script, if they do not exist yet.

Have fun and always happy landings...

The code was developed and tested using Python 3.8.0.

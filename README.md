# applehealth
Analyze the exported data from the apple health app.

The script `readxml.py` takes the XML file exported from apple health, organizes the data in a more friendly format 
and saves it as an HDF5 format. The script `build_chartbook.py` grabs the HDF5 file, makes charts and saves them to a 
PDF. Hopefully, this last file is easy to understand and adjust to your own needs and preferences.
  

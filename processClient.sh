#!/bin/bash

# CSV given in format of

# "client name",,,"client number",,"JSON OBJECT STRING"
# remove everything till the ",," deliminator
# proceeds to remove trailing " at the end

sed -r 's/^.*",,"//g;s/^.*",[0-9],"//g;s/""/"/g;s/"$//g' 'clinical notes_2019_07_08_14-44.csv' 
  | tail -n +2 > clientNotes.json


# jenkins-job-editor
Edit config.xml &lt;command> &lt;/command parameter en mass.

This code is horrible, but it works for the VERY specific purpose I wrote it (add the VirusTotalAnalyser postprocessor to the autopkg command).  At the moment it makes no edits, just lists out the filename with the changes to be made.  Code that makes the edits is commented out.

The existing configuration slicer jenkins plugin was... confusing.  

The XML file is non-standard ('plutil -lint' on a Mac as well as Python's libraries) wouldn't read it.  

Because of the number of builds/files in an existing Jenkins instance, doing a plain OS Walk with matching the config.xml filename takes FOREVER.  Code was added (mostly by trial and error) to exit out of the loop once config.xml is located by blanking out the dirs and files array.

# improvements

   x have the config.xml backed up prior to making changes. 
   x overall code cleanup and documentation

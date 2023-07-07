# ads2ccv
Script to convert BiBTeX from ADS to the XML suitable for Canadian Common CV submission.

Disclaimers: This is a proof of concept script and not a really a robust pacakge.  But a litle hacking here might save you a couple hours of dealing with an laggy website.  There are also a lot of custom overrides and you might need to put in more journals in the beginning.  The principle is good though!  That being said:

* CCV XML import is destructive so test this out before going all in.
* There is no duplication checking.  The script takes the entries in the BiBTeX files and forces them into the XML.

# How do do

1. Export the bibliography entries you want to export from NASA's Abstract Data System as a BiBTeX file.  Save this as a file (default `export-bibtex.bib`) in the same directory as the script.  If you pick a different name, edit the script.
2. Export your CCV into XML and add it into the same directory.  You will need to edit the script to match the CCV XML filename.
3. Run script to insert the bibliography entries into the XML.
4. Import the CCV XML back into the CCV system.





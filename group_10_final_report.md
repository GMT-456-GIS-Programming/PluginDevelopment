Github Repo URL : https://github.com/emreabao/PluginDevelopment.git
We created another branches but we didn't add a file in it.
We studied as all group members together.


    All group members have contributed to plugin setup. We got together
and worked as a team. While generating a plugin, Plugin Builder is used
and vector data selection is done based on our data which is also vector.
The aim was finding the shortest distance and choosen line string distance
(real distance) between two points. After that compile.bat file created.
Then, user interface for widget has created by QT Designer for QGIS.
This UI had basics and it was the primary version. In this step QGIS needed
to be restarted again. For the dialog, draft code was created.
Connections have done for the UI such as choosing a shape file or
clicking on "Run" or "Cancel" button. 


Emre: Imported the library packages. Dialog code edited. Error corrected
for the Qgis.core. "editting" class created to add attributes. 

Üftade : For the line geometry, first and last coordinates determined.
Ellipsoid created for the calculation.Minimum distance and real distance
calculated and displayed in gui.Number of processed "lineseries" displayed in gui. I
Corrected the syntax errors. UI design improved in general. 


Merve : Edits have done to open a shape file by using the Qfile dialog module.
To open specially shape files, ESRI shapefile created. With ogr method,
geometric layers in the file have reached. Control class created to not to
select any other file type except geometry.



Salient features of Plugin- RasterTool

Input Raster Data: The input data has to be fed to the plugin, user has to select raster input data in GeoTiff ( .tif ) Format. By clicking on the browse button on the proposed plug it will give the user access to the Browser Window

In the Browser Window, based on the choice made, user has to find the path of file in the system by clicking on the browse button on the window. The plugin checks for the extension of the file selected if the extension is .tif the user can select the raster file considered for processing.

Output CSV File Location: The location of the processed data must be specified by the user by clicking on the browse button.  Based on all the inputs taken from user, tool starts to process the raster data. Once the output folder is selected tool creates a new CSV file called “RasterTool*data* *time*” in the output location.


If the browse directory already consists a file named above, tool creates a new name every second in order to avoid overwriting of data. Now in the output file location string is replaced by the location of the newly created folder.

Convert Raster Dataset to CSV File: The User has to click on the Push Button to extract all the coordinate and pixel value from the the input raster Dataset into the output CSV File whose location is specified by the user. The CSV file will have XYZ attribute of each of the pixel in raster dataset.
Convert Raster to Point Shapefile: The user has to check the checkbox, this function is optional. When the user click on the checkbox the Point shapefile of each of the pixel of input raster dataset is created in the QGIS Canvas. The user can save the Points as shapefile having XYZ attributes (Latitude, Longitude, PixelValue)
Plot 3D Graph for Input Raster: The user has to check the checkbox, this function is optional. To get a graphical representation of  the input raster dataset and also to understand the variation of pixel value in the dataset the user can go with this option. The X and Y Axis will represent the latitude and longitude of the raster file. Each plot in the graph will show the variation in pixel in the raster file. The graph can be saved in SVG(Scalable Vector Graphic), JPEG (Joint Photographic Export Group), PNG(Portable Network Graphic), PDF(Portable Document Format),TIF(Tagged Image Format). The Name of the axis, Title can be edited from the pop-up window and then be saved as per user requirement.





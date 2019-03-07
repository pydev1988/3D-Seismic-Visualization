# 3D-Seismic-Visualization #
Small GUI program to Plot a 3D seismic volume as slices along the x,y,z axis.Plots any regular 3D volume,requires IL,XL range and spacing.

## Requires: ##
* numpy
* tkinter
* obspy
* mayavi
  
## GUI : This will pop up after you execute the script ##



* Enter xline and inline range this needs to come from opendetect (we need to know this before hand)

![GUI](https://raw.githubusercontent.com/pydev1988/3D-Seismic-Visualization/master/3d_plot_GUI.jpeg)

* Press plot to see how much data needs to be padded based on IL , XL input

![GUI_MESSAGE](https://raw.githubusercontent.com/pydev1988/3D-Seismic-Visualization/master/3d_plot_GUI_message.jpeg)

* Once you press ok the scipt will continue to plot the 3D cube 

![3d_plot](https://raw.githubusercontent.com/pydev1988/3D-Seismic-Visualization/master/3D_volume_plot.png)



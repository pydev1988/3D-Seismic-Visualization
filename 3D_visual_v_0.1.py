import numpy as np
import tkinter as tk
from tkinter import font
import tkinter.messagebox
import sys
from os.path import join, dirname
import copy
from obspy.io.segy.segy import _read_segy  #library to read Seg-Y data
from mayavi import mlab #library for 3D visualization
import time 
sys.argv = [''] #Mayavi needs it 

'''
Small GUI program to plot any regularly shaped 3D seismic cube
I haven't dealt with any jagged tooth survey yet
'''

#GUI Part 

master = tk.Tk()
master.title("3D Seg-Y Viewer")
# master.geometry('800x500')

rows = 0
while rows < 5000:
    master.rowconfigure(rows, weight=1)
    master.columnconfigure(rows, weight=1)
    rows += 1

master.resizable(False, False)

# create font
fnt = font.Font(family='Helvetica', size=12, weight='bold')
font.families()
# create space around internal frame
master['padx'] = 15
master['pady'] = 15

# --- ROW (0)
cmd_frame = tk.LabelFrame(master, text="3D Seismic viewer based on Mayavi", relief=tk.RIDGE)

cmd_frame.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

# --- ROW (1)

var_lbl_1 = "Input file location and IL and XL bounds"

lbl_1 = tk.Label(cmd_frame, text=var_lbl_1)

lbl_1.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (2)

var_lbl_2 = "Enter complete location of the 3D volume that you need to visualize"

lbl_2 = tk.Label(cmd_frame, text=var_lbl_2)

lbl_2.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (3)


segy_dir_path = tk.Entry(cmd_frame, relief=tk.SUNKEN, width=80, justify=tk.LEFT )

segy_dir_path.grid(row=3, column=2, columnspan=300, sticky=tk.W, padx=5, pady=5)

# --- ROW (4)

var_lbl_3 = "Enter Minimum INLINE"

lbl_3 = tk.Label(cmd_frame, text=var_lbl_3)

lbl_3.grid(row=4, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (5)

min_inline = tk.Entry(cmd_frame, relief=tk.SUNKEN, width=30, justify=tk.LEFT )
min_inline.grid(row=5, column=2, columnspan=300, sticky=tk.W, padx=5, pady=5)


# --- ROW (6)

var_lbl_4 = "Enter Maximum INLINE"

lbl_4 = tk.Label(cmd_frame, text=var_lbl_4)

lbl_4.grid(row=6, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (7)

max_inline = tk.Entry(cmd_frame, relief=tk.SUNKEN, width=30, justify=tk.LEFT )
max_inline.grid(row=7, column=2, columnspan=300, sticky=tk.W, padx=5, pady=5)


# --- ROW (8)

var_lbl_5 = "Enter INLINE Spacing"

lbl_5 = tk.Label(cmd_frame, text=var_lbl_5)

lbl_5.grid(row=8, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (9)

inline_step = tk.Entry(cmd_frame, relief=tk.SUNKEN, width=10, justify=tk.LEFT )
inline_step.grid(row=9, column=2, columnspan=300, sticky=tk.W, padx=5, pady=5)


# --- ROW (10)

var_lbl_6 = "Enter Minimum XLINE"

lbl_6 = tk.Label(cmd_frame, text=var_lbl_6)

lbl_6.grid(row=10, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (11)

min_xline = tk.Entry(cmd_frame, relief=tk.SUNKEN, width=30, justify=tk.LEFT )
min_xline.grid(row=11, column=2, columnspan=300, sticky=tk.W, padx=5, pady=5)


# --- ROW (12)

var_lbl_7 = "Enter Maximum XLINE"

lbl_7 = tk.Label(cmd_frame, text=var_lbl_7)

lbl_7.grid(row=12, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (13)

max_xline = tk.Entry(cmd_frame, relief=tk.SUNKEN, width=30, justify=tk.LEFT )
max_xline.grid(row=13, column=2, columnspan=300, sticky=tk.W, padx=5, pady=5)


# --- ROW (14)

var_lbl_8 = "Enter XLINE Spacing"

lbl_8 = tk.Label(cmd_frame, text=var_lbl_8)

lbl_8.grid(row=14, column=2, sticky=tk.W, padx=5, pady=5)

# --- ROW (15)

xline_step = tk.Entry(cmd_frame, relief=tk.SUNKEN, width=10, justify=tk.LEFT )
xline_step.grid(row=15, column=2, columnspan=300, sticky=tk.W, padx=5, pady=5)


var_lbl_8 = "---------------------"

lbl_8 = tk.Label(cmd_frame, text=var_lbl_8)
lbl_8.grid(row=16, column=2, sticky=tk.W, padx=5, pady=5)



# Functions to plot the seismic data in 3D and destroy window


def read_seismic():
    try:
        t0 = time.time()
        data = segy_dir_path.get()
        #use obspy to read data
        stream = _read_segy(data, headonly=True)
        #create stream object
        num_trace = len(stream.traces)
        #get ns from binary header
        ns = stream.binary_file_header.number_of_samples_per_data_trace
       
        min_il = int(min_inline.get())
        max_il = int(int(max_inline.get()) + 1)
        il_step = int(inline_step.get())
        min_xl = int(min_xline.get())
        max_xl = int(int(max_xline.get()) + 1 )
        xl_step = int(xline_step.get())

        inline_range = np.arange(min_il, max_il, il_step)
        xline_range = np.arange(min_xl, max_xl, xl_step)

        total_traces_calculated = (len(inline_range) * len(xline_range))
        total_missing_traces = int(total_traces_calculated - num_trace)

        lines = ["Total no of traces read     : {}".format(num_trace), "Total number of calculated traces :{}".format(total_traces_calculated), "Total traces to pad: {}".format(total_missing_traces)]

        tkinter.messagebox.showinfo("INFO", "\n".join(lines))
        

        data = np.stack(t.data for t in stream.traces)
        #get z dim
        bounds , nt = data.shape
        data_t =  data.T
        #Pad data with zero traces
        data_padded = np.pad(data_t, [(0,0), (0,total_missing_traces)], mode='constant' )
        data_padded = data_padded.T
        #Reshape data to a 3d cube
        shaped_data = np.reshape(data_padded,(inline_range.size, xline_range.size, nt ))
        #calculate the right colorbar scale
        vm = np.percentile(shaped_data,99)

        #Define the mayavi data source
        source = mlab.pipeline.scalar_field(shaped_data)
        source.spacing = [il_step, xl_step, -4]

        for axis in ['x', 'y', 'z']:
            plane = mlab.pipeline.image_plane_widget(source, 
                                    plane_orientation='{}_axes'.format(axis),
                                     colormap="gray", vmin= -vm , vmax = vm, slice_index=20)
            plane.module_manager.scalar_lut_manager.reverse_lut = True
            mlab.xlabel("XLINE")
            mlab.ylabel("INLINE")
            mlab.zlabel("TIME/DEPTH")
            #mlab.title("3D Seismic Cube : {}".format(str(segy_dir_path.get())))
            #mlab.colorbar()

        mlab.show()



    except ValueError:
        tk.messagebox.showinfo("ERROR", "Please check your input bounds")
        close_window()

    except FileNotFoundError:
        tk.messagebox.showinfo("ERROR", "Please check your input File")
        close_window()



def close_window():
    master.destroy()



plot_mayavi = tk.Button(cmd_frame, text="SHOW PLOT", relief=tk.RAISED, command=read_seismic)
plot_mayavi.grid(row=18, column=2, sticky=tk.W, padx=5, pady=5)

close_mayavi = tk.Button(cmd_frame, text="EXIT", relief=tk.RAISED, command=close_window)
close_mayavi.grid(row=19, column=2, sticky=tk.W, padx=5, pady=5)



master.mainloop()

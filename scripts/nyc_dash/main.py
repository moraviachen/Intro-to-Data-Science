import pandas
import numpy as np
import csv
import re
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure,show
from numpy.random import random, normal, lognormal



data=pandas.read_csv("ziplineAverage.csv")
data['str']=data['zip'].astype(str)
f=open("ziplineAverage.csv",'r')
reader=csv.reader(f)
datas=list(reader)

zips=data['str'].tolist()



zipcode1 = Select(options=zips,value='none', title='Zipcode1')
zipcode2 = Select(options=zips,value='none', title='Zipcode2')

average_=[39.85275817250289,70.91295978640147,82.34366875407711,78.52451247748056,93.62494317774248,111.92904687527033,106.70994674708291,122.85084388829594,170.1975542644955,0,0,0]

#initiate graph
#plot the constant line
p = figure(plot_width=600, plot_height=600,x_axis_label='Month',y_axis_label='Average responce time (h)')
p.line([1,2,3,4,5,6,7,8,9,10,11,12], average_, line_width=2,legend_label="average",line_color='red')
p.circle([1,2,3,4,5,6,7,8,9,10,11,12], average_,line_color='red',fill_color=None)

#zipcode1 line
data = {'x': [1, 2, 3, 4, 5,6,7,8,9,10,11,12],'y': [0,0,0,0,0,0,0,0,0,0,0,0]}
source1 = ColumnDataSource(data=data)
p.line('x','y', line_width=2,source=source1,line_color='green', legend_label="Zipcode1")
p.circle('x','y',source=source1,line_color='green',fill_color=None)

#zipcode2 line
dataa = {'x': [1, 2, 3, 4, 5,6,7,8,9,10,11,12],'y': [0,0,0,0,0,0,0,0,0,0,0,0]}
source2 = ColumnDataSource(data=dataa)
p.line('x','y', line_width=2,source=source2,line_color='blue', legend_label="Zipcode2")
p.circle('x','y',source=source2,line_color='blue',fill_color=None)

def update_plot1(attr, old, new):
    update=find_array((int)(new))
    source1.data={'x': [1, 2, 3, 4, 5,6,7,8,9,10,11,12],'y': update}

def update_plot2(attr, old, new):

    update=find_array((int)(new))
    source2.data={'x': [1, 2, 3, 4, 5,6,7,8,9,10,11,12],'y': update}


zipcode1.on_change('value', update_plot1)
zipcode2.on_change('value',update_plot2)

layout = column(zipcode1, zipcode2,p)
curdoc().add_root(layout)


def find_array(num):
    ret=[]

    data=pandas.read_csv("ziplineAverage.csv")

    lis= data['zip']== num

    lis = np.flatnonzero(lis)[0]+1

    for i in range(1,9):
        if re.search("[0-9]",datas[lis][i]):
            ret.append((float)(datas[lis][i]))
        else:
            ret.append(0.0)

    ret.append(0.0)
    ret.append(0.0)
    ret.append(0.0)
    ret.append(0.0)

    return ret


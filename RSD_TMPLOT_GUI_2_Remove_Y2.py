from cgi import print_arguments
from appJar import gui
import os
import logging
import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import collections

Date = '(10-07-2023)'
print("\n>>>>>Telemetry Data Ploting Application {}!!\n".
      format(Date))

#logging configuration
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#GUI initialization part
ui = gui("Range System Division {}".format(Date), "650x750") #, useTtk=True)
#ui.setTtkTheme('winnative')
ui.increaseButtonFont()
ui.setFont(12)
ui.setFg('Black', override=False)
ui.setBg('darkgray', override=False, tint=False)
ui.resizable = False

#appJar UI logging settings
# ui.setLogLevel('DEBUG')

#InputFile
def inputFiletoDF(inputFile):
    try:
        if inputFile.lower().endswith('.txt'):
            df = pd.read_csv(inputFile, sep='\t')  # Assuming it's a TSV file
        elif inputFile.lower().endswith('.xlsx'):
            df = pd.read_xlsx(inputFile)
        else:
            ui.error('Invalid file format: %s', inputFile)
            return None  # Return None for unsupported formats
        return df
    except Exception as e:
        ui.critical('%s', e)
        ui.exception('Error loading file: %s', inputFile)
        return None  # Return None for any exceptions

#change trace_mode values to correct format
def convertTraceModeToID(trace_mode):
    if trace_mode == 'Lines+Markers':
        trace_mode_id = 1
    elif trace_mode == 'Lines':
        trace_mode_id = 2
    elif trace_mode == 'Markers':
        trace_mode_id = 3
    return trace_mode_id
def createPlotDict(y_keys, trace_mode_id):
    plotDict = collections.defaultdict(dict)
    #graph line marking definitions
    if trace_mode_id == 1:
        trace_mode = 'lines+markers'
    elif trace_mode_id == 2:
        trace_mode = 'lines'
    elif trace_mode_id == 3:
        trace_mode = 'markers'

    #build keys from y_List to all primary y-axis plots
    for key in y_keys:
        plotDict[key]['name'] = key
        plotDict[key]['axis'] = 'y'
        plotDict[key]['mode'] = trace_mode
    return plotDict

#plotEngine builds plots based on items in plot dictionary
def plotEngine(fig, plotDict, X, Y1, df2):
    #iterate through all dictionary keys
    """"
    # print("===> ",plotDict)
    for k in plotDict:
        #plot y-axis keys
        if plotDict[k]['axis'] == 'y' :
            pName = plotDict[k]['name']
            pMode = plotDict[k]['mode']
            fig.add_trace(go.Scattergl(x=np.transpose(np.array(df2[X]))[0], y=np.transpose(np.array(df2[Y1]))[0],
                                        mode=pMode,
                                        name=pName),secondary_y=True,)
    """    
    print('==Y1===>', Y1, len(Y1))
    if len(Y1) > 1:
        # pass
        for i in range(len(Y1)):
            # print(Y1[i])
            k = np.transpose(np.array(df2[Y1[i]]))
            print("Y1==>",k, len(k))
            # print("=={}==>".format(i),k)
            # print(np.transpose(np.array(df2[Y1[i]]))[i])
            for k in plotDict:
                if plotDict[k]['axis'] == 'y':
                    pName = plotDict[k]['name']
                    pMode = plotDict[k]['mode']
            fig.add_trace(go.Scattergl(x=np.transpose(np.array(df2[X]))[0], y=k,
                                            # mode='lines+markers',
											name=Y1[i].split(" ")[0],
                                            mode=pMode,
											# name=pName,                                          
                                            ))
    else:
            for k in plotDict:
                if plotDict[k]['axis'] == 'y':
                    pName = plotDict[k]['name']
                    pMode = plotDict[k]['mode']

            fig.add_trace(go.Scattergl(x=np.transpose(np.array(df2[X]))[0], y=np.transpose(np.array(df2[Y1]))[0],
                                            # mode='lines+markers',
                                            name=Y1[0].split(" ")[0],
                                            mode=pMode,
                                            # name=pName,
                                            ))
    print("returning from plotEngine")
    # """


#loading plot settings from UI to generate the plot
def loadPlotSettings():
    ui.info('Retrieving plotting settings')
    listBoxes = ui.getAllListBoxes()
    try:
        x_items = listBoxes['X-Axis']
        ui.info('Plot X-Axis: %s', x_items)
        y_items = listBoxes['Y-Axis']
        ui.info('Plot Y-Axis: %s', y_items)

        sec_y = True
            #ui.debug('Secondary axis items selected')

        trace_mode = ui.getRadioButton('trace_mode')
        trace_mode_id = convertTraceModeToID(trace_mode)
        titles_all = ['', '', '', '']
        titles_all[0] = ui.getEntry('Title:')
        titles_all[1] = ui.getEntry('X-Axis title:')
        titles_all[2] = ui.getEntry('Y-Axis title:')
        #ui.debug('titles gathered: %s', titles_all)
        
        # print("@=>", sec_y, x_items, y_items )
        # Return only the necessary values
        return sec_y, x_items, y_items,trace_mode_id, titles_all

    except Exception as e:
        ui.critical('%s', e)
        ui.error('ERROR!! Cannot retrieve settings for plotting!')
        ui.queueFunction(ui.setLabel, 'output', 'ERROR retrieving settings')
        ui.queueFunction(ui.setLabelBg, 'output', 'red')
        return None, None, None, None, None  # Return None values in case of an error

    
#data drop function to set file location based on data drop
def externalDrop(data):
    if data[0] == '{':
        ofile = data.split('{', 1)[1].split('}')[0]
    else:
        ofile = data
    ui.info('Data drop used: %s', ofile)
    ui.setEntry('file', ofile, callFunction=True)

#generates most of needed data and preparations needed for plotting and save as html from GUI parts
def plotPreparations():
    ifile2 = ui.getEntry('file')
    df_inputfile = inputFiletoDF(ifile2)
    sec_y, x_items, y_items, trace_mode_id, titles_all = loadPlotSettings()
    df2 = df_inputfile
    print(df2.head())
    try:
        plotDict = createPlotDict(y_items, trace_mode_id)
    except Exception as e:
        ui.critical('%s', e)
        ui.error('ERROR!! Cannot create dictionary for plotting!!!')

    return  sec_y, plotDict, x_items, y_items, df2, titles_all
            
#createFig creates a figure from the data and displays the figure
def createFig(sec_y, plotDict, x_axis, y_axis,df2, titles_all):
    #debug messages before plotting
    #ui.debug('plotting dataframe...')
    #ui.debug('dataframe dtypes: \n%s', df2.dtypes)

    x  = x_axis
    y1 = y_axis
    
    #create figure
    fig = make_subplots(specs=[[{"secondary_y": sec_y}]])

    plotEngine(fig, plotDict, x, y1, df2)

    fig.update_layout(
                        showlegend=True,
                        title=titles_all[0],
                        title_x=0.5,
                        xaxis_title=titles_all[1],
                        yaxis_title=titles_all[2],
                    )

    fig.update_yaxes(title_text=titles_all[3], secondary_y=True)

    fig.show()
    #ui.debug('Showing plot')

#saveFigAsHTML works the same as createFig, except it produces a HTML file with all the data plotted
def saveFigAsHTML(sec_y, plotDict, x_axis, df, HTML_name_path, titles_all):
    #debug messages before plotting
    #ui.debug('plotting dataframe...')
    #ui.debug('dataframe dtypes: \n%s', df.dtypes)

    #create figure
    fig = make_subplots(specs=[[{"secondary_y": sec_y}]])

    plotEngine(fig, plotDict, x_axis, df)

    fig.update_layout(
                        showlegend=True,
                        title=titles_all[0],
                        title_x=0.5,
                        xaxis_title=titles_all[1],
                        yaxis_title=titles_all[2],)

    fig.update_yaxes(title_text=titles_all[2],secondary_y=True)

    fig.write_html('{}.html'.format(HTML_name_path))
    # ui.debug('Saved HTML file: %s', HTML_name_path)

#button press actions
def press(btn):
    ui.info('User pressed --> %s', btn)
    if btn == 'Plot':
        # df2 = None  # Initialize df2
        # titles_all = None 
        # sec_y = None
        x_axis = None
        y_axis = None
        try:
            sec_y, plotDict, x_items, y_items, df2, titles_all = plotPreparations()
            createFig(sec_y, plotDict, x_items, y_items, df2, titles_all)  # Pass X-Axis data without conversion 
            # print("=-=-=-=-=-=>",sec_y, "\n",plotDict, "\n", x_items, "\n", y_items, "\n", df2, titles_all)

            ui.info('Plotting figure completed!')
            ui.queueFunction(ui.setLabel, 'output', 'Plotting figure completed!')
            ui.queueFunction(ui.setLabelBg, 'output', 'green')
        except ValueError as v:
            # print("ERROR==>",v)
            ui.error("Could not plot the data!")
            ui.queueFunction(ui.setLabel, 'output', 'Could not plot the data!')
            ui.queueFunction(ui.setLabelBg, 'output', 'red')
        except Exception as e:
            ui.critical('%s', e)
            ui.error("Issues with plotting")
            ui.queueFunction(ui.setLabel, 'output', 'ERROR plotting!!!')
            ui.queueFunction(ui.setLabelBg, 'output', 'red')

    elif btn == 'Save As HTML':
        #similar to plot except save the output as html file
        save_location = ui.getEntry('output_location')
        #ui.debug('Save location given: %s', save_location)
        HTML_entry = ui.getEntry('HTML filename')
        #ui.debug('HTML filename given: %s', HTML_entry)
        if not save_location:
            ui.setFocus('output_location')
            ui.error('No save directory given to save as HTML!!')
            ui.queueFunction(ui.setLabel, 'output', 'Need save directory to save as HTML...')
            ui.queueFunction(ui.setLabelBg, 'output', 'yellow')
            return
        if not HTML_entry:
            ui.setFocus('HTML filename')
            ui.error('No filename given to save as HTML!!')
            ui.queueFunction(ui.setLabel, 'output', 'Need filename to save as HTML...')
            ui.queueFunction(ui.setLabelBg, 'output', 'yellow')
            return
        else:
            if HTML_entry.endswith('.html'):
                HTML_split = HTML_entry.split('.')
                HTML_name = HTML_split[0]
            else:
                HTML_name = HTML_entry     
        try:
            sec_y, plotDict, x_items, y_items, df2, titles_all = plotPreparations()
            saveFigAsHTML( y_items,df2[x_items[0]], df2, os.path.join(save_location, HTML_name), titles_all)
            ui.info('Saving figure as HTML completed!')
            ui.queueFunction(ui.setLabel, 'output', 'Saving figure as HTML completed!')
            ui.queueFunction(ui.setLabelBg, 'output', 'green')
        except Exception as e:
            ui.critical('%s', e)
            ui.error("Issues with Saving as HTML file")
            ui.queueFunction(ui.setLabel, 'output', 'ERROR saving as HTML!!!')
            ui.queueFunction(ui.setLabelBg, 'output', 'red') 
    elif btn == "Load file":
        #load dropped or selected file and update axis listing
        ifile = ui.getEntry('file')
        ui.info('Loading file %s', ifile)
        ui.queueFunction(ui.setLabel, 'output', 'Loading file...')
        ui.queueFunction(ui.setLabelBg, 'output', 'yellow')
        try:
            df = inputFiletoDF(ifile)
            # print('sujit>>>>',type(df))
            # print('sujit>>>>',df.keys())

            colList = df.columns
            #ui.debug(colList)
            numColumns = str(len(colList))
            ui.info('Read columns from %(filename)s ---> Number of columns %(columns)s', {'filename': ifile, 'columns': numColumns})
            if numColumns == 0:
                ui.error('Loaded file has no data!!')
                ui.queueFunction(ui.setLabel, 'output', 'Loaded file has no data!!')
                ui.queueFunction(ui.setLabelBg, 'output', 'red')
            else:
                ui.clearListBox('X-Axis', callFunction=True)    
                ui.updateListBox('X-Axis', colList, select=False)
                ui.clearListBox('Y-Axis', callFunction=True)    
                ui.updateListBox('Y-Axis', colList, select=False)
                ui.info('File loaded!')
                ui.queueFunction(ui.setLabel, 'output', 'File loaded!')
                ui.queueFunction(ui.setLabelBg, 'output', 'yellow')
        except Exception as e:
            ui.critical('%s', e)
            ui.error('Could not parse input file to dataframe!!')
            ui.queueFunction(ui.setLabel, 'output', 'ERROR loading file...')
            ui.queueFunction(ui.setLabelBg, 'output', 'red')
   
    elif btn == 'Debug':
        #activate Debug logging to file
        ui.setButton('Debug', 'Debug ON')
        ui.queueFunction(ui.setLabel, 'output', 'Debug ON')
        ui.queueFunction(ui.setLabelBg, 'output', 'yellow')
        ui.setLogFile('debug.log') #the activation by appJar function
        ui.info(' RANGE SYSTEM DIVISION (RSD)%s', Date)
    elif btn == 'Insert Program location -->':
        ui.setEntry('output_location', os.path.abspath(os.getcwd()), callFunction=True)
    elif btn == 'Insert Datafile location -->':
        inputfile = ui.getEntry('file')   
        if inputfile != '': 
            splitted = os.path.split(inputfile)
            ui.setEntry('output_location', os.path.abspath(splitted[0]), callFunction=True)
        else:
            ui.queueFunction(ui.setLabel, 'output', 'No Datafile Loaded!...')
            ui.queueFunction(ui.setLabelBg, 'output', 'yellow')
#-------------------------------------------------------UI START ----------------------------------------------------------------#
#UI START
##General TAB and TAB start      
ui.startTabbedFrame("TabbedFrame")
ui.startTab("General")
#Data input 
ui.startFrame('Data Input', row=0, column=0, colspan=3)
ui.startLabelFrame('Drag & Drop datafile here')
ui.addLabel("dropLab", "\t\t\tDrag & Drop datafile here (or use File)\t\t\t")
ui.setLabelBg('dropLab', 'light cyan')
ui.setLabelFg('dropLab', 'grey')
try:
    ui.setLabelDropTarget("dropLab", externalDrop)
except Exception as e:
    ui.critical('%s', e)
    pass
ui.stopLabelFrame()
ui.addFileEntry("file")
ui.getEntryWidget('file').config(font="Helvetica 12")
ui.addButton('Load file', press)
ui.getButtonWidget('Load file').config(font="Helvetica 12")
ui.stopFrame()
#Axis information and data selection
ui.startFrame('Axis Frame', row=1, column=0, colspan=3)
ui.startLabelFrame('Select by clicking add multiple items')# and use CTRL or SHIFT to
ui.addLabel('EmptyAxisLabel', '\t') #to remove overcrowding in the axis setting frame
ui.startFrame('X_Pane', row=1, column=0)
ui.addLabel("X_select", "Select X-Axis:")
ui.addListBox('X-Axis', '')
ui.setListBoxGroup('X-Axis', group=True)
ui.setListBoxRows('X-Axis', 14)
ui.stopFrame()
ui.startFrame('Y_Pane', row=1, column=1)
ui.addLabel("Y_select", "Select Y-Axis items:")
ui.addListBox('Y-Axis', '')
ui.setListBoxMulti('Y-Axis', multi=True)
ui.setListBoxGroup('Y-Axis', group=True)
ui.setListBoxRows('Y-Axis', 14)
ui.stopFrame()
ui.addCheckBox("Get Bit", row=0, column=3)
ui.setCheckBoxChangeFunction("Get Bit",press)
ui.setCheckBoxSelectColour("Get Bit", "red")
check_box = int(ui.getCheckBox("Get Bit"))
print(check_box)
ui.stopLabelFrame()
ui.stopFrame()
ui.stopTab() #End General Tab

##Settings TAB
ui.startTab("Settings") 

#trace mode settings
ui.startLabelFrame('Plot trace mode') 
ui.startFrame('Trace_M_1', row=2, column=0, colspan=1)
ui.addRadioButton("trace_mode", "Lines+Markers")
ui.stopFrame()
ui.startFrame('Trace_M_2', row=2, column=1, colspan=1)
ui.addRadioButton("trace_mode", "Lines")
ui.stopFrame()
ui.startFrame('Trace_M_3', row=2, column=2, colspan=1)
ui.addRadioButton("trace_mode", "Markers")
ui.stopFrame()
ui.stopLabelFrame()

# Titles
ui.startLabelFrame('Titles')
ui.startFrame('Axis_options_1', row=6, column=0, colspan=2)
ui.addLabelEntry('Title:')
ui.stopFrame()
ui.startFrame('Axis_options_2', row=6, column=2, colspan=2)
ui.addLabelEntry('X-Axis title:')
ui.stopFrame()
ui.startFrame('Axis_options_3', row=7, column=0, colspan=2)
ui.addLabelEntry('Y-Axis title:')
ui.stopFrame()
ui.stopLabelFrame()
ui.stopTab() #End settings tab

##About TAB
ui.startTab("About")
#ui.addLabel(Tlemetry Data ploting)
ui.addImage("test","DRDL.gif")
ui.zoomImage("test",-13)
ui.addLabel('Version', 'RANGE   SYSTEM   DIVISION (RSD)\n\n\n {}'.format(Date))
ui.addButton('Debug', press)
ui.setButton('Debug', 'Debug OFF')
ui.addEmptyMessage('Debug Messages')
ui.setMessageWidth('Debug Messages', 900)
ui.stopTab() #End about tab
ui.stopTabbedFrame() #END tabbing

##Bottom parts styling
ui.startFrame('Bottom', row=3, column=0, colspan=3)
ui.setBg('ghost white')


#Plot command, 
ui.addButton('Plot', press)
ui.getButtonWidget('Plot').config(font="Helvetica 12")

#SaveAsHTML directory
ui.startLabelFrame('Save as HTML save directory')
ui.startFrame('output_choise_1', row=5, column=0, colspan=1)
# ui.addButton('Insert Program location -->', press)
ui.addButton('Insert Datafile location -->', press)
ui.stopFrame()
ui.startFrame('output_choise_2', row=5, column=1, colspan=3)
ui.addDirectoryEntry("output_location")
ui.stopFrame()
ui.stopLabelFrame()

#SaveAsHTML filename and button
ui.addLabelEntry('HTML filename')
ui.getLabelWidget("HTML filename").config(font="Helvetica 12")
ui.addButton('Save As HTML', press)
ui.getButtonWidget('Save As HTML').config(font="Helvetica 12")

#Output label
ui.addLabel('output')
ui.setLabel('output', "Ready - Waiting Command")
ui.setLabelBg("output", "yellow")
ui.getLabelWidget("output").config(font="Helvetica 14")

ui.stopFrame() #End bottoms part

ui.go()
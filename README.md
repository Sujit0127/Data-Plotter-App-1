# Data-Plotter-App-1
Telemetry Data Plotting Application

This Python application, built using appJar, is designed to plot telemetry data from files (TXT, XLSX). The app provides an intuitive graphical user interface (GUI) for selecting X and Y axes for the plot, applying various trace modes (Lines, Markers, Lines+Markers), and generating plots with Plotly.

Features:
Drag & Drop File Input: Easily load telemetry data files by drag-and-drop.
Axis Selection: Allows users to select the X and multiple Y axes for plotting data.
Bit-wise Plotting: Optional bit-wise plotting of Y-axis data by selecting a specific bit.
Interactive Plot Generation: Choose from multiple trace modes (lines, markers, or both) for your plots.
Save as HTML: Save plots as interactive HTML files.
Real-time Logging: Log important events like loading files, plotting, and errors.
Supports Multiple File Formats: Works with both .txt and .xlsx files.
How to Use:
Load a Data File: Drag and drop a telemetry data file or load it via the file input.
Select Axes: Choose the X and Y axes from the file's data columns.
Customize Plot: Select trace modes, titles, and bit manipulation options.
Generate Plot: Press "Plot" to generate the graph.
Save as HTML: Optionally save the plot as an interactive HTML file.
Requirements:
  1.appJar
  2.pandas
  3.numpy
  4.plotly

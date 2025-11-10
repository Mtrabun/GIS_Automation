# Import necessary modules for ArcPy, file handling, and timestamps

# ----------------------------------------------------------
# Script Name: Log_Spatial_Ref.py
# Purpose: Logs the number of features in each feature class
#          within a specified File Geodatabase (.gdb) or
#          Enterprise Geodatabase (.sde) connection.
# Author: Matthew Trbun; Kevin Romero Sanchez
# Date: 2025-11-10
# ----------------------------------------------------------

# Set the ArcPy workspace to the target GDB or SDE path

# Define the path for the output log file that will store results

# Open the log file in append mode so that new logs are added
# without erasing previous entries

# Write a header to the log file with the current date and time

# List all feature classes that exist directly within the workspace

# List any feature datasets within the workspace (used in SDEs or complex GDBs)

# Initialize a list to hold all feature class names,
# including those inside feature datasets

# Loop through each dataset and retrieve its feature classes

# Add the dataset feature classes to the main list,
# including the dataset name for clarity

# Loop through each feature class in the combined list

# Use ArcPy's GetCount tool to get the number of features in the feature class

# Write the feature class name and its feature count to the log file

# Optionally print the feature count to the console for real-time feedback

# If an error occurs (e.g., permission issue or corrupted dataset),
# catch the exception and log an error message instead of stopping the script

# Close the log file automatically when finished (handled by the 'with' block)

# Print a final confirmation message to indicate logging is complete

# ----------------------------------------------------------
# Script Name: Log_Spatial_Ref.py
# Purpose: Logs the number of features and spatial reference
#          for each feature class within a specified
#          File Geodatabase (.gdb) or Enterprise
#          Geodatabase (.sde) connection.
#
#          NOTE: This script is strictly READ-ONLY and does
#          not alter any source data or schema.
#
# Author: Matthew Trbun; Kevin Romero Sanchez
# Date: 2025-11-10
# ----------------------------------------------------------

# Import necessary Python and ArcPy modules
import arcpy              # Core ArcGIS geoprocessing library
import os                 # Provides path and file utilities
import datetime           # Used to timestamp log entries

# ----------------------------------------------------------
# USER INPUTS (EDIT THESE VALUES AS NEEDED)
# ----------------------------------------------------------

# Set the ArcPy workspace to the target GDB or SDE path.
# This can be a path to:
#   - A File Geodatabase: r"C:\Path\To\Your.gdb"
#   - An SDE connection file: r"C:\Path\To\YourConnection.sde"
workspace = r"C:\Path\To\YourWorkspace.gdb"

# Define the path for the output log file that will store results.
# The log file will be opened in APPEND mode, so new runs will
# be added to the bottom of the same file.
log_file_path = r"C:\Path\To\Logs\Log_Spatial_Ref.txt"

# If you want to use this script as an ArcGIS Pro script tool,
# you can replace the above with:
# workspace = arcpy.GetParameterAsText(0)
# log_file_path = arcpy.GetParameterAsText(1)

# ----------------------------------------------------------
# ENVIRONMENT SETUP
# ----------------------------------------------------------

# Set the ArcPy workspace environment to the user-defined path.
# This tells ArcPy where to look for feature classes and datasets.
arcpy.env.workspace = workspace

# Disable overwrite of outputs just for safety.
# (This is mostly relevant if you later add tools that create data.)
arcpy.env.overwriteOutput = False

# ----------------------------------------------------------
# OPEN LOG FILE AND WRITE HEADER
# ----------------------------------------------------------

# Ensure the folder for the log file exists before trying to write.
# If it does not exist, raise a clear error instead of failing silently.
log_folder = os.path.dirname(log_file_path)
if log_folder and not os.path.exists(log_folder):
    raise OSError(f"Log folder does not exist: {log_folder}")

# Open the log file in append mode so that new logs are added to
# the end of the file and previous logs are preserved.
with open(log_file_path, "a", encoding="utf-8") as log_file:
    # Generate a timestamp for this logging session.
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write a simple header for this run, including workspace and time.
    log_file.write("\n")
    log_file.write("------------------------------------------------------------\n")
    log_file.write(f"Log run at: {current_time}\n")
    log_file.write(f"Workspace: {workspace}\n")
    log_file.write("FeatureClass | FeatureCount | SpatialReference\n")
    log_file.write("------------------------------------------------------------\n")

    # ------------------------------------------------------
    # COLLECT FEATURE CLASSES
    # ------------------------------------------------------

    # List all feature classes that exist directly in the
    # top level of the workspace (i.e., not inside datasets).
    # Returns a list of feature class names or None.
    top_level_fcs = arcpy.ListFeatureClasses() or []

    # List any feature datasets within the workspace.
    # Feature datasets are containers that may hold multiple
    # feature classes, often used in SDEs or complex GDBs.
    datasets = arcpy.ListDatasets(feature_type="Feature") or []

    # Initialize a list to hold the full "relative" paths (within
    # the workspace) of all feature classes we will inspect.
    # This will include both:
    #   - Top-level feature classes (e.g., "Parcels")
    #   - Dataset feature classes (e.g., "Transportation/RoadCenterlines")
    all_feature_classes = []

    # Add the top-level feature classes directly to the master list.
    for fc_name in top_level_fcs:
        # For top-level feature classes, their relative path is just the name.
        all_feature_classes.append(fc_name)

    # For each feature dataset, list its feature classes and add them
    # to the master list with the dataset name for clarity.
    for ds_name in datasets:
        # List feature classes inside this dataset.
        # The "feature_dataset" parameter tells ArcPy to search
        # specifically within the given dataset.
        ds_feature_classes = arcpy.ListFeatureClasses(feature_dataset=ds_name) or []

        for fc_name in ds_feature_classes:
            # Construct a relative path like "DatasetName/FeatureClassName".
            # This makes it easier to identify where the feature class lives.
            relative_path = os.path.join(ds_name, fc_name)
            all_feature_classes.append(relative_path)

    # ------------------------------------------------------
    # PROCESS EACH FEATURE CLASS
    # ------------------------------------------------------

    # Loop through every collected feature class path.
    for rel_fc_path in all_feature_classes:
        # Wrap processing in a try/except block so that a problem
        # with a single feature class (e.g., permissions, corruption)
        # does not stop the entire script.
        try:
            # Build the full path to the feature class by combining
            # the workspace path with the relative feature class path.
            # This is safe and READ-ONLY; it simply identifies the data.
            full_fc_path = os.path.join(workspace, rel_fc_path)

            # --------------------------------------------------
            # GET FEATURE COUNT (READ-ONLY)
            # --------------------------------------------------

            # Use ArcPy's GetCount tool to retrieve the number of
            # rows (features) in the feature class.
            # GetCount returns a Result object; we cast it to int.
            count_result = arcpy.GetCount_management(full_fc_path)
            feature_count = int(count_result[0])

            # --------------------------------------------------
            # GET SPATIAL REFERENCE (READ-ONLY)
            # --------------------------------------------------

            # Use ArcPy's Describe function to get metadata about
            # the feature class. This is also READ-ONLY.
            desc = arcpy.Describe(full_fc_path)

            # Safely obtain the spatial reference. Some rare datasets
            # may have a None spatialReference, so we guard against that.
            spatial_ref_name = "Unknown"
            if hasattr(desc, "spatialReference") and desc.spatialReference:
                # Use the spatial reference name (e.g., "NAD 1983 StatePlane ...")
                spatial_ref_name = desc.spatialReference.name or "Unnamed Spatial Reference"

            # --------------------------------------------------
            # WRITE TO LOG FILE
            # --------------------------------------------------

            # Build a single line of output with the relative path,
            # feature count, and spatial reference name.
            log_line = f"{rel_fc_path} | {feature_count} | {spatial_ref_name}\n"

            # Write the line to the log file.
            log_file.write(log_line)

            # --------------------------------------------------
            # OPTIONAL CONSOLE OUTPUT
            # --------------------------------------------------

            # Print to the console for real-time feedback if
            # running this as a standalone script.
            print(log_line.strip())

            # If you are running this as an ArcGIS Pro script tool,
            # you could also send the message to the geoprocessing
            # pane using:
            # arcpy.AddMessage(log_line.strip())

        except Exception as ex:
            # If ANY error occurs while processing this feature class,
            # capture the message and log it instead of raising.
            error_message = f"{rel_fc_path} | ERROR: {str(ex)}\n"
            log_file.write(error_message)
            print(error_message.strip())
            # For script tool usage, you might also do:
            # arcpy.AddWarning(error_message.strip())

    # ------------------------------------------------------
    # END OF WITH BLOCK
    # ------------------------------------------------------
    # When the 'with' block ends, the log file is automatically
    # and safely closed, even if errors occurred during processing.

# ----------------------------------------------------------
# FINAL CONFIRMATION MESSAGE
# ----------------------------------------------------------

# Print a final confirmation so the user knows the script finished.
print(f"Logging complete. Results written to: {log_file_path}")
# For script tool usage:
# arcpy.AddMessage(f"Logging complete. Results written to: {log_file_path}")

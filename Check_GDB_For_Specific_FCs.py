# Script: CheckGDBForFeatureClasses.py
# Description: This script checks a gdb for user-specified feature classes,
# generates a report, and logs the results.

import arcpy
import os
import logging

# Set up logging
logging.basicConfig(filename='script_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to search for feature classes in a geodatabase
def find_feature_classes(gdb_path, feature_classes):
    arcpy.env.workspace = gdb_path
    found_classes = []
    missing_classes = []

    for fc in feature_classes:
        if arcpy.Exists(fc):
            found_classes.append(fc)
        else:
            missing_classes.append(fc)

    return found_classes, missing_classes

# Main script
if __name__ == '__main__':
    try:
        # Specify the geodatabase path
        gdb_path = r'C:\Path\to\your\geodatabase.gdb'

        # Specify the feature classes to search for
        feature_classes_to_search = ['FeatureClass1', 'FeatureClass2', 'FeatureClass3']

        # Call the function to find feature classes
        found_classes, missing_classes = find_feature_classes(gdb_path, feature_classes_to_search)

        # Generate a report
        print("Found Feature Classes:")
        for fc in found_classes:
            print(fc)

        print("\nMissing Feature Classes:")
        for fc in missing_classes:
            print(fc)

        # Log the results
        logging.info("Found Feature Classes: %s", ', '.join(found_classes))
        logging.info("Missing Feature Classes: %s", ', '.join(missing_classes))

        print("\nScript completed successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"An error occurred: {str(e)}")

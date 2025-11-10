import arcpy  # ArcPy is ESRI's Python site package for geoprocessing
import os     # Used to manipulate file paths
import logging  # Standard Python logging module

# -------------------------------
# Set up logging to print messages to the console
# -------------------------------
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)  # Create a logger instance

def get_coord_system_info(feature_class):
    """
    Retrieves the projected and geographic coordinate systems of a feature class.
    Returns:
        - Projected coordinate system name (or 'None')
        - Geographic coordinate system name (or 'None')
    """
    try:
        # Describe the feature class to access its metadata
        desc = arcpy.Describe(feature_class)
        spatial_ref = desc.spatialReference

        # Determine if it has a projected coordinate system
        projected_cs = spatial_ref.name if spatial_ref.type == "Projected" else "None"

        # Safely get geographic coordinate system if it exists
        geographic_cs = spatial_ref.GCS.name if hasattr(spatial_ref, 'GCS') else "None"

        return projected_cs, geographic_cs

    except Exception as e:
        # Log any error that occurs while retrieving coordinate system info
        logger.error(f"Error getting spatial reference for {feature_class}: {e}")
        return "Unknown", "Unknown"

def log_all_feature_classes(sde_path):
    """
    Logs the name and coordinate systems for all feature classes in an SDE workspace.

    Args:
        sde_path (str): Full path to the .sde connection file
    """
    try:
        # Set ArcPy's workspace to the provided SDE connection
        arcpy.env.workspace = sde_path

        # Extract just the SDE file name for logging (e.g., 'SPW_GDBA@SPW_GIS_TEST')
        sde_name = os.path.splitext(os.path.basename(sde_path))[0]

        logger.info(f"\nScanning ALL feature classes in SDE: {sde_name}")
        logger.info("=" * 60)

        # -----------------------------------------------
        # Step 1: List and log all standalone feature classes (not inside datasets)
        # -----------------------------------------------
        for fc in arcpy.ListFeatureClasses():
            # Construct the full path to the feature class
            full_fc_path = os.path.join(arcpy.env.workspace, fc)

            # Retrieve spatial reference information
            projected_cs, geographic_cs = get_coord_system_info(full_fc_path)

            # Log the results
            logger.info(f"SDE: {sde_name}")
            logger.info(f"Feature Class: {fc}")
            logger.info(f"  Projected Coordinate System: {projected_cs}")
            logger.info(f"  Geographic Coordinate System: {geographic_cs}")
            logger.info("-" * 60)

        # -----------------------------------------------
        # Step 2: List datasets and feature classes within each dataset
        # -----------------------------------------------
        datasets = arcpy.ListDatasets(feature_type="Feature") or []  # Fall back to empty list if no datasets
        for ds in datasets:
            # Get feature classes inside this dataset
            feature_classes = arcpy.ListFeatureClasses(feature_dataset=ds)

            for fc in feature_classes:
                # Build full path to dataset-based feature class
                full_fc_path = os.path.join(arcpy.env.workspace, ds, fc)

                # Retrieve spatial reference information
                projected_cs, geographic_cs = get_coord_system_info(full_fc_path)

                # Log the results, including dataset context
                logger.info(f"SDE: {sde_name}")
                logger.info(f"Feature Class: {ds}\\{fc}")
                logger.info(f"  Projected Coordinate System: {projected_cs}")
                logger.info(f"  Geographic Coordinate System: {geographic_cs}")
                logger.info("-" * 60)

    except Exception as main_err:
        # Catch any unexpected errors in the process
        logger.error(f"Error scanning SDE '{sde_path}': {main_err}")

if __name__ == "__main__":
    # Replace this path with your actual .sde file path
    sde_connection_path = r"C:\Users\you\your@SDE.sde"

    # Call the logging function with your SDE connection
    log_all_feature_classes(sde_connection_path)

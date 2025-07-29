# Import required libraries
import os  # For working with file paths and directories

# Import the report-saving function from your processing module
from loader_reports import save_msd_report


# Define the path to your cleaned MSD CSV files
report_dir = "../../Data/MSD/cleaned"


# Loop through every file in the specified directory
for file in os.listdir(report_dir):
    # Only process files that are CSVs
    if file.endswith(".csv"):
        # Build the full file path
        full_path = os.path.join(report_dir, file)

        # Call the function to transform and insert this report into the database
        save_msd_report(full_path)

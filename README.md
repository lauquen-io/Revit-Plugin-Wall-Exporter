# PyRevit Plugin: Wall Exporter

## Overview

This PyRevit plugin is designed to export wall geometry data in JSON format for use in other applications. The exported JSON file contains information about the walls' dimensions, angles, and surface areas.

## Usage

1. Install PyRevit: Ensure that PyRevit is installed in your Autodesk Revit environment.

2. Open your Revit project.

3. Run the script: Execute the provided Python script in the Revit Python Shell or any Python environment within Revit.

4. JSON Export: The script identifies walls in the active document, processes their geometry, and exports a JSON file containing two main sections:
   - **Recortes (Cuts):** Information about walls without 'E' in the 'Marca' parameter, including their names, vertices, and calculated surface area.
   - **Enrases (Screeds):** Information about walls with 'E' in the 'Marca' parameter, including their names, vertices, height, and length.

## Script Details

The script utilizes the Revit API and PyRevit library to collect wall geometry and process it. Here is a brief breakdown of the script:

- **Geometry Processing:**
  - Walls are filtered based on the 'OST_Walls' category.
  - For each wall, the script extracts relevant geometry information, such as edges and their directions.

- **Data Calculation:**
  - For walls without 'E' in the 'Marca' parameter, the script calculates angles, vertices, and surface area using the Shoelace Formula.
  - For walls with 'E' in the 'Marca' parameter, the script calculates angles, vertices, height, and length, excluding the shortest and longest edges.

- **JSON Export:**
  - The calculated data is stored in a Python dictionary.
  - The dictionary is serialized into JSON format with proper indentation.
  - The JSON file is saved in the same directory as the Revit project, named after the project with a '.json' extension.

## Output

After running the script, a JSON file is generated, providing a structured representation of the wall data. This file can be utilized in other applications according to the specific needs of your workflow.

**Note:** Ensure that the 'Marca' parameter is appropriately set for walls to be included in the export.

Feel free to customize and integrate this plugin into your Revit workflows as needed. If you encounter any issues or have suggestions for improvement, please contribute to the development of this plugin.

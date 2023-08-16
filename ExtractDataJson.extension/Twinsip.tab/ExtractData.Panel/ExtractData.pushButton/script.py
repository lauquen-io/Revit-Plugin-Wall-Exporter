import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Options, Solid, XYZ
from pyrevit import revit

# Get the active document
doc = revit.doc

# Define a filter to collect walls
wall_filter = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()

# Create an instance of the Options class
options = Options()

def convert_to_px(lenght):
    return lenght / 5

# Loop through the collected walls and print their length, height and mark
for wall in wall_filter:
    edges = []
    mark_param = wall.LookupParameter('Mark').AsString()
    
    # Get the geometry of the wall
    geometry = wall.get_Geometry(options)
    
    # Loop through the geometry objects
    for obj in geometry:
        # Check if the object is a Solid
        if isinstance(obj, Solid):
            # Loop through the edges of the solid
            for edge in obj.Edges:
                # Get the direction of the edge
                edge_dir = (edge.AsCurve().GetEndPoint(1) - edge.AsCurve().GetEndPoint(0)).Normalize()
                
                # Check if the edge direction is perpendicular to the wall's normal
                if abs(edge_dir.DotProduct(wall.Orientation)) < 0.001:
                    # Get the length of the edge
                    edge_length = edge.ApproximateLength * 304.8
                    
                    edge_length = convert_to_px(int(round(edge_length, 0)))
                    
                    edges.append(edge_length)
                
    for i in range(len(edges) / 2):
        edges.pop()
        
    print('Wall Mark: ', mark_param)
    
    # Print the length of the edge
    print(edges)
    
    

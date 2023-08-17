import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

import math

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

def get_angles(edges_dir_array):
    angles = []
    for i in range((len(edges_dir_array) - 1)):
        edge1 = edges_dir_array[i]
        edge2 = edges_dir_array[i + 1]
        
        dir1 = (edge1.AsCurve().GetEndPoint(1) - edge1.AsCurve().GetEndPoint(0)).Normalize()
        dir2 = (edge2.AsCurve().GetEndPoint(1) - edge2.AsCurve().GetEndPoint(0)).Normalize()
        
        angle = dir1.AngleTo(dir2)
        angles.append(round(angle))
        
    edge1 = edges_dir_array[-1]
    edge2 = edges_dir_array[0]
    
    dir1 = (edge1.AsCurve().GetEndPoint(1) - edge1.AsCurve().GetEndPoint(0)).Normalize()
    dir2 = (edge2.AsCurve().GetEndPoint(1) - edge2.AsCurve().GetEndPoint(0)).Normalize()
    
    angle = dir1.AngleTo(dir2)
    angles.append(round(angle))
        
    return angles

def get_vertices(edges, angles):
    vertices = [{"x": 0, "y": 0}]
    angle = 0
    
    for i in range(len(edges)):
        x = edges[i] * math.cos(math.radians(angle))
        y = edges[i] * math.sin(math.radians(angle))
        prev = vertices[-1]
        vertices.append({"x": round(prev["x"] + x), "y": round(prev["y"] + y)})
        angle += angles[i]
    
    vertices.pop(0)
        
    return vertices
        

# Loop through the collected walls and print their length, height and mark
for wall in wall_filter:
    edges = []
    edges_dir_array = []
    angles = []
    vertices = []
    
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
                    
                    edges_dir_array.append(edge)
                
    for i in range(len(edges) / 2):
        edges.pop()
        edges_dir_array.pop()
    
    angles = get_angles(edges_dir_array)
    
    vertices = get_vertices(edges, angles)
    
    # Final object to return
    dict = {'name': mark_param,
            'points': vertices}
    
    print(dict)
    


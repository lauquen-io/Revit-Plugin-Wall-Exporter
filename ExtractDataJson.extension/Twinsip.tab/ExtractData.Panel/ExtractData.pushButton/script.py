import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

import math
import json

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Options, Solid, XYZ
from pyrevit import revit

# Variable where the walls will be stored
walls = []
screeds = []

# Get the active document
doc = revit.doc

# Define a filter to collect walls
wall_filter = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()

# Create an instance of the Options class
options = Options()

def save_json(panel):
    # Serializing json
    json_data = json.dumps(panel, indent=3)
    
    path = doc.PathName[:-3] + 'json'
    
    # Writing to random_data.json
    with open(path, "w") as walls_data:
        walls_data.write(json_data)

def get_angles(edges_dir_array):
    angles = []
    for i in range((len(edges_dir_array) - 1)):
        edge1 = edges_dir_array[i]
        edge2 = edges_dir_array[i + 1]
        
        dir1 = (edge1.AsCurve().GetEndPoint(1) - edge1.AsCurve().GetEndPoint(0)).Normalize()
        dir2 = (edge2.AsCurve().GetEndPoint(1) - edge2.AsCurve().GetEndPoint(0)).Normalize()
        
        angle = dir1.AngleTo(dir2)
        angles.append(angle)
    
    edge1 = edges_dir_array[-1]
    edge2 = edges_dir_array[0]
    
    dir1 = (edge1.AsCurve().GetEndPoint(1) - edge1.AsCurve().GetEndPoint(0)).Normalize()
    dir2 = (edge2.AsCurve().GetEndPoint(1) - edge2.AsCurve().GetEndPoint(0)).Normalize()
    
    angle = dir1.AngleTo(dir2)
    angles.append(angle)
        
    return angles

def get_vertices(edges, angles):
    for i in range(1, len(angles)):
        angles[i] += angles[i - 1]
        
    vertices = [{"x": 0, "y": 0}, {"x": edges[0], "y": 0}]
    
    for i in range(1, len(edges) - 1):
        angle = angles[i - 1]
            
        y_value = math.sin(angle) * edges[i]
        x_value = math.cos(angle) * edges[i]
        
        prev_x = vertices[-1]["x"]
        prev_y = vertices[-1]["y"]
        
        another_vertice = {"x": round(x_value + prev_x), "y": round(y_value + prev_y)}
        
        vertices.append(another_vertice)
            
    
    return vertices

def calculate_surface_area(points):
    if len(points) < 3:
        return 0

    def shoelace_formula(x_coords, y_coords):
        n = len(x_coords)
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += (x_coords[i] * y_coords[j]) - (y_coords[i] * x_coords[j])
        return abs(area) / 2

    x_coords = [point['x'] for point in points]
    y_coords = [point['y'] for point in points]

    return shoelace_formula(x_coords, y_coords) / 1000000
        
# Loop through the collected walls and print their length, height and mark
for wall in wall_filter:
    edges = []
    edges_dir_array = []
    angles = []
    vertices = []
    
    if wall.LookupParameter('Marca') is not None:
        mark_param = wall.LookupParameter('Marca').AsString()
    
        if mark_param and 'E' not in mark_param:
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
                            
                            edges.append(round(edge_length))
                            
                            edges_dir_array.append(edge)
                        
            for i in range(len(edges) / 2):
                edges.pop()
                edges_dir_array.pop()
                
            if len(edges_dir_array) != 0:
                angles = get_angles(edges_dir_array)

                vertices = get_vertices(edges, angles)
                
                area = calculate_surface_area(vertices)
                
                # Final object to return
                dict = {'name': mark_param,
                        'points': vertices,
                        'area': area}

                walls.append(dict)
                
    elif mark_param and 'E' in mark_param:
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
                        
                        edges.append(round(edge_length))
                        
                        edges_dir_array.append(edge)
                    
        for i in range(len(edges) / 2):
            edges.pop()
            edges_dir_array.pop()
            
        edges.sort()
            
        if len(edges_dir_array) != 0:
            # Final object to return
            
            angles = get_angles(edges_dir_array)

            vertices = get_vertices(edges, angles)
            
            dict = {'name': mark_param,
                    'points': vertices,
                    'height': edges[0],
                    'length': edges[-1]} 
            
            screeds.append(dict)
                    
file = {'recortes': walls,
        'enrases': screeds}
                
save_json(file)
print('JSON file saved at: ', doc.PathName)
    


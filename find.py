### first option ###

import arcpy

# set the workspace and the input datasets
arcpy.env.workspace = r"path\to\your\geodatabase.gdb"
points_fc = "points_feature"
terrain_fc = "terrain_layer"

# create a new feature class to store the nearest points
nearest_points_fc = "nearest_points"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nearest_points_fc, "POINT", points_fc, spatial_reference=points_fc)

# perform the near analysis
arcpy.analysis.Near(points_fc, terrain_fc)

# iterate through the points feature and update the nearest points feature class
with arcpy.da.SearchCursor(points_fc, ["SHAPE@", "NEAR_FID", "NEAR_DIST"]) as cursor:
    for row in cursor:
        point = row[0]
        near_fid = row[1]
        near_dist = row[2]
        near_point = arcpy.management.MakeFeatureLayer(terrain_fc, where_clause=f"OBJECTID = {near_fid}").getOutput(0)
        arcpy.management.Append([near_point], nearest_points_fc)


        
### second option ###


import arcpy

# set the workspace and the input datasets
arcpy.env.workspace = r"path\to\your\geodatabase.gdb"
points_fc = "points_feature"
terrain_fc = "terrain_layer"

# create a new feature class to store the nearest points
nearest_points_fc = "nearest_points"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nearest_points_fc, "POINT", points_fc, spatial_reference=points_fc)

# get the geometry of each point in the terrain feature class
terrain_points = []
with arcpy.da.SearchCursor(terrain_fc, "SHAPE@") as cursor:
    for row in cursor:
        for point in row[0]:
            terrain_points.append(point)

# iterate through the points feature and find the nearest point in the terrain layer
with arcpy.da.SearchCursor(points_fc, ["SHAPE@"]) as cursor:
    for row in cursor:
        point = row[0]
        min_dist = None
        nearest_point = None
        for terrain_point in terrain_points:
            dist = point.distanceTo(arcpy.PointGeometry(terrain_point))
            if min_dist is None or dist < min_dist:
                min_dist = dist
                nearest_point = terrain_point
        arcpy.management.Append([arcpy.Geometry("POINT", nearest_point)], nearest_points_fc)

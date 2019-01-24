import arcpy
import os, sys
from arcgis.gis import GIS

### Start setting variables
# Set the path to the project
prjPath = r"<<PATH>>"

# Update the following variables to match:
# Feature service/SD name in arcgis.com, user/password of the owner account
sd_fs_name = '<<NAME_OF_FEATURE_SERVICE>>'
portal = "https://www.arcgis.com" # Can also reference a local portal
user = '<<USERNAME>>'
password = '<<PASSWORD>>'

# Set sharing options
shrOrg = False
shrEveryone = False
shrGroups = ""
### End setting variables

# Local paths to create temporary content
relPath = r"<<LOCAL_PATH>>"
sddraft = os.path.join(relPath, "WebUpdate.sddraft")
sd = os.path.join(relPath, "WebUpdate.sd")

# Create a new SDDraft and stage to SD
print("Creating SD file")
arcpy.env.overwriteOutput = True
prj = arcpy.mp.ArcGISProject(prjPath)
m = prj.listMaps('<<NAME_OF_MAP>>')[0]

for map in prj.listMaps():
	print("map: {0} Layers".format(map.name))
	for lyr in map.listLayers():
		if lyr.isBroken:
			print("(BROKEN) " + lyr.name)
		else:
			print(" " + lyr.name)


arcpy.mp.CreateWebLayerSDDraft(m, sddraft, sd_fs_name, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS','', True, True)
arcpy.StageService_server(sddraft, sd)

print("Connecting to {}".format(portal))
gis = GIS(portal, user, password)

# Find the SD, update it, publish /w overwrite and set sharing and metadata
print("Search for original SD on portal…")
sdItem = gis.content.search("{} AND owner:{}".format(sd_fs_name, user), item_type="Service Definition")[0]
print("Found SD: {}, ID: {}. Uploading and overwriting…".format(sdItem.title, sdItem.id))
sdItem.update(data=sd)
print("Overwriting existing feature service…")
fs = sdItem.publish(overwrite=True)

if shrOrg or shrEveryone or shrGroups:
  print("Setting sharing options…")
  fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

print("Finished updating: {} – ID: {}".format(fs.title, fs.id))

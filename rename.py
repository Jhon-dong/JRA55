import glob
import os

res   = "145x288"
baseDir = "/tank/utsumi/data/JRA55"
for root, dirnames, filenames in os.walk(baseDir):
    for filename in filenames:
        if filename.lower().endswith("." + "bn"):
            ofilename = os.path.splitext(filename)[0] + ".%s"%(res)
            oPath = os.path.join(root, ofilename)
            iPath = os.path.join(root, filename)
            #print iPath
            #print oPath
            #os.rename(iPath, oPath) 

from numpy import *
import calendar
import subprocess
import os, sys
import matplotlib.pyplot as plt

#iyear    = 1958
iyear    = 1980
eyear    = 2009
lyear    = range(eyear,iyear-1,-1)
#lyear    = range(iyear,eyear+1)
lmon     = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon     = [1]
#lmon     = arange(1,12+1)
tstp     = "Monthly"
singleday   = False  # True or False
miss_out    = -9999.0
#stype  = "fcst_surf125"
#lvar   = ["BRTMP"]
#stype  = "anl_column125"
#lvar   = ["PWAT"]
stype  = "fcst_phy2m125"
lvar   = ["APCP"]
res    = "145x288"
#--- LAT & LON & NX, NY : Original  ------------------------------
dlat_org      = 1.25
dlon_org      = 1.25

lat_first_org = -90.0
lat_last_org  = 90.0
lon_first_org = 0.0
lon_last_org  = 360.0 - 1.25
a1lat_org     = arange(lat_first_org, lat_last_org + dlat_org*0.1, dlat_org)  
#-----------
a1lon_org     = arange(lon_first_org, lon_last_org + dlon_org*0.1, dlon_org)

#-----------
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass

#---------------------------------------------------------------
ny_org     = len(a1lat_org)
nx_org     = len(a1lon_org)
nz_org     = 1
print ny_org, nx_org


#********************************************
#********************************************
for year in lyear:
  for mon in lmon:
    for var in lvar:
      #idir      =  "/mnt/mizu.tank/utsumi/JRA55/Monthly/%s/%04d"%(stype,year)
      #idir      =  "/data2/JRA55/Hist/Monthly/%s/%04d"%(stype,year)
      idir      =  "/data2/JRA55/Hist/Monthly/%s"%(stype)
      ctlname   = idir + "/%s.monthly.ctl"%(stype)

      #odir_root =  "/media/disk2/data/JRA55/%s.%s/%s"%(res, stype, tstp)
      odir_root =  "/tank/utsumi/data/JRA55/%s.%s/%s"%(res, stype, tstp)
      odir_temp = odir_root  +  "/%s"%(var)
      odir      = odir_temp  +  "/%04d"%(year)
      odir_meta = "/".join(odir_root.split("/")[:-1])
      #-- make directory ---
      mk_dir(odir_root)
      mk_dir(odir_temp)
      mk_dir(odir)
      print odir    
    
      #-- discription file ----------------
      #< dims >
      sout   = "lev %d\nlat %d\nlon %d"%(nz_org, ny_org, nx_org)
      f      = open( odir_meta + "/dims.txt", "w")
      f.write(sout)
      f.close()
    
      #< lat >
      sout   = "\n".join(map( str, a1lat_org))
      f      = open( odir_meta + "/lat.txt", "w")
      f.write(sout)
      f.close()
    
      #< lon >
      sout   = "\n".join(map( str, a1lon_org))
      f      = open( odir_meta + "/lon.txt", "w")
      f.write(sout)
      f.close()
    
      #< dump >
      tempname = idir + "/%s.%04d%02d"%(stype, year, mon)
      dumpname = odir_meta + "/%s/dump.txt"%(var)
    
      ptemp  = subprocess.call("wgrib -V %s | grep -A 6 %s > %s"%(tempname, var.upper(), dumpname), shell=True)
      #  
      #---------
      stime     = "%04d%02d"%(year, mon)
      #----- Names ------------
      gribname  = idir + "/%s.%s"%(stype, stime)
      oname     = odir + "/%s.%s.%s.%s"%(stype, var, stime, res)
    
      print gribname
      if not os.access(gribname, os.F_OK): 
        print "no file"
        print gribname
        sys.exit()
      #-- grib --> binary -----
    
      args      = "wgrib %s | grep %s | wgrib %s -i -nh -o %s"%(gribname, var.upper(), gribname, oname)
       
      ptemp     = subprocess.call(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       
      #-- Flipud --------
      print oname
      a2org     = flipud(fromfile(oname, float32).reshape(ny_org, nx_org))
      #
      a2org.tofile( oname ) 
      print oname
    


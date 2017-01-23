from numpy import *
import calendar
import subprocess
import os, sys
import matplotlib.pyplot as plt

flgave   = True
lmon     = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon     = [1]
#lmon     = arange(1,12+1)
singleday   = False  # True or False
miss_out    = -9999.0
stype  = "anl_surf125"
lvar   = ["PRMSL"]
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
for var in lvar:
  for mon in lmon:
    idir      =  "/data2/JRA55/clim8110/Monthly/%s"%(stype)
    ctlname   = idir + "/%s.monthly.ctl"%(stype)

    odir_root =  "/tank/utsumi/data/JRA55/%s.%s/clim8110"%(res, stype)
    odir      = odir_root
    #odir_meta = "/".join(odir_root.split("/")[:-1])
    odir_meta = odir
    #-- make directory ---
    mk_dir(odir_root)
    #mk_dir(odir_temp)
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
  
    ##< dump >
    #tempname = idir + "/%s_%s.clim8110.mon%02d"%(stype, var, mon)
    #dumpname = odir_meta + "/%s/dump.txt"%(var)


    ##ptemp  = subprocess.call("wgrib -V %s | grep -A 6 %s > %s"%(tempname, var.upper(), dumpname), shell=True)

    ##  
    #---------
    stime     = "%02d"%(mon)
    #----- Names ------------
    gribname  = idir + "/%s.clim8110.mon%s"%(stype, stime)
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

  #---- annual clim --------     
  if flgave != True:
    continue

  a2ann = zeros([ny_org,nx_org], float32)
  for mon in lmon:
    days  = calendar.monthrange(1999,mon)[1]
    stime = "%02d"%(mon)
    iname = odir + "/%s.%s.%s.%s"%(stype, var, stime, res) 
    a2mon = fromfile(iname, float32).reshape(ny_org, nx_org)
    a2ann = a2ann + a2mon*days

  a2ann = a2ann / 365.0
  oname = odir + "/%s.%s.00.%s"%(stype, var, res) 
  a2ann.tofile(oname)
  print oname

 

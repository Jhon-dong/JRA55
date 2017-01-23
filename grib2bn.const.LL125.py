from numpy import *
import calendar
import subprocess
import os, sys
import matplotlib.pyplot as plt

singleday   = False  # True or False
miss_out    = -9999.0
stype  = "LL125"
#lvar   = ["topo"]
lvar   = ["land","topo"]
dvarcode = {"topo":"GP", "land":"LAND"}
res    = "145x288"
#--- const ----
g = 9.80665  # m/s^2
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

#---------------------------------------------------------------
ny_org     = len(a1lat_org)
nx_org     = len(a1lon_org)
nz_org     = 1

print ny_org, nx_org

##-- modify a1lat_rog for interpolation at polar region --
#a1lat_org[0]  = -90.0
#a1lan_org[-1] = 90.0
#-----------
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass

#********************************************
#********************************************
for var in lvar:
  varcode   = dvarcode[var]
  #idir      =  "/mnt/mizu.tank/utsumi/JRA55/const"
  idir      =  "/data2/JRA55/Const"
  ctlname   = idir + "/%s.ctl"%(stype)

  #odir_root =  "/media/disk2/data/JRA55/%s.%s/const"%(res, stype)
  odir_root =  "/tank/utsumi/data/JRA55/%s.%s/const"%(res, stype)
  odir      = odir_root 
  #-- make directory ---
  mk_dir(odir_root)
  mk_dir(odir)
  print odir    

  #-- discription file ----------------
  #< dims >
  sout   = "lev %d\nlat %d\nlon %d"%(nz_org, ny_org, nx_org)
  f      = open( odir + "/dims.txt", "w")
  f.write(sout)
  f.close()

  #< lat >
  sout   = "\n".join(map( str, a1lat_org))
  f      = open( odir + "/lat.txt", "w")
  f.write(sout)
  f.close()

  #< lon >
  sout   = "\n".join(map( str, a1lon_org))
  f      = open( odir + "/lon.txt", "w")
  f.write(sout)
  f.close()

  #< dump >
  tempname = idir + "/%s.grib"%(stype)
  dumpname = odir + "/dump.txt"

  ptemp  = subprocess.call("wgrib -V %s | grep -A 6 'rec %s' > %s"%(tempname, varcode, dumpname), shell=True)
  #  
  #----- Names ------------
  gribname  = idir + "/%s.grib"%(stype)
  oname     = odir + "/%s.%s"%(var, res)

  print gribname
  if not os.access(gribname, os.F_OK): 
    print "no file"
    print gribname
    sys.exit()
  #-- grib --> binary -----

  args      = "wgrib %s | grep %s | wgrib %s -i -nh -o %s"%(gribname, varcode, gribname, oname)
   
  ptemp     = subprocess.call(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   
  #-- Flipud --------
  a2bn     = flipud(fromfile(oname, float32).reshape(ny_org, nx_org))

  #-- geopotential (m^2/s^2) --> geopoteitial height (m) --
  if var == "topo":
    a2bn     =  a2bn / g
  #------------------
  a2bn.tofile( oname ) 
  print oname

  #------------------------------------
  




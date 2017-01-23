from numpy import *
import calendar
import subprocess
import os, sys
import matplotlib.pyplot as plt

#iyear    = 1980
iyear    = 1981
eyear    = 1989
lmon     = arange(1,12+1)
#lmon     = [9]
tstp     = "6hr"
res      = "145x288"
singleday   = False  # True or False
miss_out    = -9999.0
#lplev       = [250]   # pressure level (hPa)
#lplev       = [850]
#lplev       = [850,700,500,300,250]
#lplev       = [250,300,500,600,700,850,925]
#lplev       = [300,600,700,925]
#lplev       = [850,500,250]
#lplev       = [500,250]
#lplev       = [500]
#lplev       = [850,250]
lplev       = [700]

#*******************
# u, v : 850, 500, 250
# tmp  : 850, 500, 250
# spfh : 850
#*******************
#lvar   = ["tmp","ugrd","vgrd"]
#lvar   = ["ugrd","vgrd"]
#lvar   = ["tmp"]
lvar   = ["spfh"]
stype    = "anl_p125"

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

#-- modify a1lat_rog for interpolation at polar region --
#a1lat_org[0]  = -90.0
#a1lat_org[-1] = 90

#********************************************
#********************************************
for year in range(iyear, eyear + 1):
  for mon in lmon:
    for plev in lplev:
      for var in lvar:
        #idir      = "/mnt/mizu.tank/utsumi/JRA55/Daily/%s_%s/%04d%02d"%(stype,var,year,mon)
        idir      = "/data2/JRA55/Hist/Daily/%s/%04d%02d"%(stype,year,mon)
        ctlname   = idir + "/%s_%s.ctl"%(stype, var)

        odir_root =  "/tank/utsumi/data/JRA55/%s.%s/%s"%(res, stype, tstp)
        odir_temp = odir_root  +  "/%s"%(var)
        odir      = odir_temp  +  "/%04d/%02d"%(year, mon)
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
        tempname = idir + "/%s_%s.%04d%02d0100"%(stype, var, year, mon)
        dumpname = odir_meta + "/dump.txt"
    
        ptemp  = subprocess.call("wgrib -V %s | grep -A 6 %s | grep -A 6 '%d mb' > %s"%(tempname, var.upper(), plev, dumpname), shell=True)
        #  
        #---------
        eday  = calendar.monthrange(year, mon)[1]
        if singleday == True:
          eday   = 1
        #-----------------
        for day in range(1, eday+1):
          #---
          if singleday == True:
            print "*****************"
            print "   single day !!"
            print "*****************"
          #---
          print year, mon, day 
          for hour in [0, 6, 12, 18]:
            stime     = "%04d%02d%02d%02d"%(year, mon, day, hour)
            #----- Names ------------
            gribname  = idir + "/%s_%s.%s"%(stype, var, stime)
            oname     = odir + "/%s.%s.%04dhPa.%s.%s"%(stype, var, plev, stime, res)
    
            print gribname
            if not os.access(gribname, os.F_OK): 
              print "no file"
              print gribname
              sys.exit()
            #-- grib --> binary -----
    
            args      = "wgrib %s | grep %s | grep '%d mb' | wgrib %s -i -nh -o %s"%(gribname, var.upper(), plev, gribname, oname)
             
            ptemp     = subprocess.call(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
             
            #-- Flipud --------
            a2org     = flipud(fromfile(oname, float32).reshape(ny_org, nx_org))
            #-- write ---------
            a2org.tofile( oname ) 
            print oname
    
            #------------------------------------
  




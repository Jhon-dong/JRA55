import subprocess 
import calendar, os
hostname  = "ds.data.jma.go.jp"
#sidir_root = "/data01/Grib/anl_p"
#sodir_root = "/media/disk2/temp"
#dattype   = "anl_surf125"
dattype   = "anl_p125"
sidir_root = "/data19/JRA-55/Clim8110/Monthly/%s"%(dattype)
#sodir_root = "/tank/utsumi/JRA55/clim8110/Monthly/%s"%(dattype)
sodir_root = "/data2/JRA55/clim8110/Monthly/%s"%(dattype)

#lvar      = ["vvel","vpot","vgrd","ugrd","tmp","strm","spfh","rh","relv","reld","hgt","depr"]
lvar      = ["reld"]
#lmon      = [1,2,3,4,5,6,7]
#lmon      = [8,9,10,11,12]
lmon      = range(1,12+1)
myid      = "jra02177"
mypass    = "suimongaku"
#----------------------------------
def mk_dir(sodir):
  try:
    os.makedirs(sodir)
  except OSError:
    pass
#----------------------------------
for var in lvar:
  for mon in lmon:
    #--- directory -----------
    sidir = sidir_root 
    sodir = sodir_root 
    mk_dir(sodir)
    #--- ctl file ------------
    ctlname = sidir + "/%s_%s.monthly.ctl"%(dattype,var)
    idxname = sidir + "/%s_%s.monthly.idx"%(dattype,var)
  
    scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, ctlname, sodir, ctlname.split("/")[-1])
    print scmd
    subprocess.call(scmd, shell=True)
  
    scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, idxname, sodir, idxname.split("/")[-1])
    print scmd
    subprocess.call(scmd, shell=True)
  
    #-------------------------
    siname  = sidir + "/%s_%s.clim8110.mon%02d"%(dattype, var, mon)
    scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, siname,sodir, siname.split("/")[-1])
    print scmd
    subprocess.call(scmd, shell=True)

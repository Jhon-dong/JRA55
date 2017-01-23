import subprocess 
import calendar, os
hostname  = "ds.data.jma.go.jp"
#sidir_root = "/data01/Grib/anl_p"
#sodir_root = "/media/disk2/temp"
#dattype   = "fcst_surf125"
#dattype   = "anl_column125"
dattype   = "fcst_phy2m125"
sidir_root = "/data20/JRA-55/Hist/Monthly/%s"%(dattype)
#sodir_root = "/tank/utsumi/JRA55/Monthly"
sodir_root = "/data2/JRA55/Hist/Monthly"

##iyear     = 1958
iyear     = 1958
eyear     = 2015
lyear     = range(eyear,iyear-1,-1)
#iyear     = 2004
#eyear     = 2004

lmon      = [1,2,3,4,5,6,7,8,9,10,11,12]
iday      = 1
myid      = "jra02177"
mypass    = "suimongaku"
#----------------------------------
def mk_dir(sodir):
  try:
    os.makedirs(sodir)
  except OSError:
    pass
#----------------------------------
for year in lyear:
  #--- directory -----------
  sidir = sidir_root 
  #sodir = sodir_root + "/%s/%04d"%(dattype, year) 
  sodir = sodir_root + "/%s"%(dattype) 
  mk_dir(sodir)
  #--- ctl file ------------
  ctlname = sidir + "/%s.monthly.ctl"%(dattype)
  idxname = sidir + "/%s.monthly.idx"%(dattype)
  
  scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, ctlname, sodir, ctlname.split("/")[-1])
  print scmd
  subprocess.call(scmd, shell=True)
  
  scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, idxname, sodir, idxname.split("/")[-1])
  print scmd
  subprocess.call(scmd, shell=True)
  
  for mon in lmon:
    siname  = sidir + "/%s.%04d%02d"%(dattype, year,mon)
    scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, siname,sodir, siname.split("/")[-1])
    print scmd
    subprocess.call(scmd, shell=True)

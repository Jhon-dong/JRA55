import subprocess 
import calendar, os
hostname  = "ds.data.jma.go.jp"
#sidir_root = "/data01/Grib/anl_p"
#sodir_root = "/media/disk2/temp"
dattype   = "anl_surf125"
sidir_root = "/data18/JRA-55/Hist/Daily/%s"%(dattype)
#sodir_root = "/tank/utsumi/JRA55/Daily"
sodir_root = "/data2/JRA55/Hist/Daily"

iyear     = 1959
eyear     = 2014
lyear     = range(iyear, eyear+1)
lmon      = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon      = [1]
iday      = 1
lhour     = [0,6,12,18]
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
  for mon in lmon:
    #--- directory -----------
    sidir = sidir_root + "/%04d%02d"%(year, mon)
    sodir = sodir_root + "/%s/%04d%02d"%(dattype, year, mon) 
    mk_dir(sodir)
    #--- ctl file ------------
    ctlname = sidir + "/%s.ctl"%(dattype)
    idxname = sidir + "/%s.idx"%(dattype)
  
    scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, ctlname, sodir, ctlname.split("/")[-1])
    print scmd
    subprocess.call(scmd, shell=True)
  
    scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, idxname, sodir, idxname.split("/")[-1])
    print scmd
    subprocess.call(scmd, shell=True)
  
    #-------------------------
    eday = calendar.monthrange(year, mon)[1]
    for day in range(iday, eday+1):
      for hour in lhour:
        siname  = sidir + "/%s.%04d%02d%02d%02d"%(dattype, year,mon,day,hour)
        print year, mon, day, hour
        scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, siname,sodir, siname.split("/")[-1])
        print scmd
        subprocess.call(scmd, shell=True)

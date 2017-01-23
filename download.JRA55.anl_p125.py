import subprocess 
import calendar, os
hostname  = "ds.data.jma.go.jp"
#sidir_root = "/data01/Grib/anl_p"
sidir_root = "/data18/JRA-55/Hist/Daily/anl_p125"
#sodir_root = "/media/disk2/temp"
sodir_root = "/tank/utsumi/JRA55/Daily"
dattype   = "anl_p125"

iyear     = 2004
eyear     = 2007
lmon      = [1,2,3,4,5,6,7,8,9,10,11,12]
iday      = 1
lhour     = [0,6,12,18]
myid      = "jra02177"
mypass    = "suimongaku"
#lvar      = ["tmp","ugrd","vgrd"]
lvar      = ["spfh"]
#----------------------------------
def mk_dir(sodir):
  try:
    os.makedirs(sodir)
  except OSError:
    pass
#----------------------------------
for year in range(iyear, eyear+1):
  for mon in lmon:
    for var in lvar:
      #--- directory -----------
      sidir = sidir_root + "/%04d%02d"%(year, mon)
      sodir = sodir_root + "/%s_%s/%04d%02d"%(dattype, var, year, mon) 
      mk_dir(sodir)
      #--- ctl file ------------
      ctlname = sidir + "/%s_%s.ctl"%(dattype, var)
      idxname = sidir + "/%s_%s.idx"%(dattype, var)
  
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
          siname  = sidir + "/%s_%s.%04d%02d%02d%02d"%(dattype, var, year,mon,day,hour)
          print year, mon, day, hour
          scmd  = "wget ftp://%s:%s@%s%s -O %s/%s"%(myid, mypass, hostname, siname,sodir, siname.split("/")[-1])
          print scmd
          subprocess.call(scmd, shell=True)

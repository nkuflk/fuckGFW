fuckGFW
=======

由于GFW对于google的封锁，国内用户访问google通常可以采用两种方法：    
1.使用vpn。免费的vpn通常速度比较慢，速度快的vpn一般使用费用都比较高    
2.修改本地的hosts文件，绕过GFW的封锁

但是第二个做法往往由于google ip的变动或者封锁策略的调整导致访问google失败

So，本脚本解决的问题就是，自动寻找可用的google ip，并筛选出最快的加入hosts，达到突破GFW的目的

脚本依赖：    
python 2.x    
py-curl

脚本功能说明：    
getIpRange.py   获取google可用的ip段    
pingIp.py   在可用的ip段内获取可以ping通的domain信息    
selectHost.py   寻找速度最快的ip    
autoSetHosts.py   自动将找到的hosts信息加入你的本地hosts文件    

说明：    
由于pingIp.py会对所有可能的ip进行处理，所以运行一次速度较慢。虽然脚本已经采用多线程的处理方法，但是全都获取完仍需要8个小时的时间。因此，output文件是已经ping好的文件信息，可以使用。output文件会不定时更新。

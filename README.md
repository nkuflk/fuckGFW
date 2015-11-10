fuckGFW
=======

为了突破万恶的GFW对于google的封锁，国内用户通常可以采用两种方法：  
1.使用vpn。但是免费的vpn通常速度比较慢，速度快的vpn一般使用费用都比较高(土豪随意)  
2.修改本地的hosts文件，绕过GFW的封锁

但是第二个做法往往由于google ip的变动或者封锁策略的调整导致访问google失败

本脚本可以自动寻找可用的google ip，并筛选出最快的加入hosts，达到突破GFW的目的

### Dependency:
> * python 2.x    
> * pycurl  
> * pydns

### Usage:
> * python fuck.py

### Description:
> * 脚本开了500个线程抓取可用ip，并筛选，建议根据本机情况调整线程数量

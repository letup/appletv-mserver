#Porting AppleTV-MServer to other Platform

# Introduction #

AppleTV-MServer should be platform independent application. I think it can running on lot of NAS or PC.


# Details #

Porting AppleTV-MServer to your platform, you need following enviroment at least.

1 Device with root access
2 You can running compile enviroment on it.(GCC)
3 Maybe at least 600Mhz CPU & 128M memory.
4 A web service with cgi and dir-index and rewrite support(Apache is better).
5 Python.

After you prepare your enviroment.
Download libav code from inmethod

http://www.inmethod.com/forum/posts/list/1856.page

Compile your own binary version of you device.

Then checkout my source code, all you need to do is change path in the source files.
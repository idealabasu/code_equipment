# **Static IP setup**

## **on ur5**

set ur5 IP as 192.168.1.xxx. For example: 192.168.1.101, subnet mask 255.255.255.0

## **on pc**

open Control Panel\Network and Internet\Network and Sharing Center find the ethernet card plugged with ur5 internet cable.In ethernet status> properities> internet protocol version 4(TCP/IPv4)>Use the following IP{ Address)set the static ip of the Ethernet card as 192.168.1.xxy (Not the same) for example 192.168.1.102 (in same range with ur5)Set the subnet mask as 255.255.255.0 (same with ur5)

Your setting should be something like this:

![alt text](https://github.com/idealabasu/code_equipment/blob/main/media/static_ip.png)

## **test connection**

Open CMD
```
ping 192.168.1.101
```
If the settings are correct, you should be able to get response from the cmd

## **use urx to connect**

works with polyscope 3.10+ and 5.8

```
import urx
ur5 = urx.Robot("192.168.1.101")
if ur5.host = "192.168.1.101"
  print("Connected")

```
# **URX function**

[https://github.com/dli-sys/hardwares_code/blob/main/ur5_control.py](https://github.com/dli-sys/hardwares_code/blob/main/ur5_control.py)

# **Wifi connection (never tested)**

[https://www.daacoworks.com/blog/how-to-connect-the-ur-cobots-to-factory-wi-fi-network](https://www.daacoworks.com/blog/how-to-connect-the-ur-cobots-to-factory-wi-fi-network)


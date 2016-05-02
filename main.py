from pyadb import ADB
from struct import *
import os
os_path=os.getcwd()
#file_path=raw_input("please input .thumbdata file path:")

print "initializing ADB... Please allow the permission on your phone."
adb = ADB('/usr/bin/adb')
print "Waiting for device..."
adb.wait_for_device()
print "getting devices list..."
error,lst_device=adb.get_devices()
print "found " + str(len(lst_device)/2) + " devices."
print lst_device
#device_id=raw_input("input device id:")
print "locating thumbdata files.."
thumbfiles=adb.shell_command("ls -a /storage/emulated/0/DCIM/.thumbnails/ ")
thumbfiles=[""]
lst_thumb=thumbfiles.split("\n")

for item in lst_thumb:
    if item.find(".thumbdata")!=-1:
        print "found:" + item
        print "copying..."
        #adb.run_cmd("pull /storage/emulated/0/DCIM/.thumbnails/" + item[:-1] + " " + os.getcwd() + "/tmp/" + item[:-1] )
        if not  os.path.isfile(os.getcwd() + "/tmp/" + item[:-1]):
            adb.get_remote_file("/storage/emulated/0/DCIM/.thumbnails/" + item[:-1] ,os.getcwd() + "/tmp/" + item[:-1] )
            print "copy OK!"
        else:
            print "cache found. skipping..."
        print "extracting thumb pictures..."
        if not os.path.exists(os.getcwd() + "/extract/" + item[:-1] ): # make a new dir
            os.makedirs(os.getcwd() + "/extract/" + item[:-1]  )
        file_size=os.path.getsize(os.getcwd() + "/tmp/" + item[:-1])
        print "file size:" + str(file_size)
        f=open(os.getcwd() + "/tmp/" + item[:-1],"rb")
        offset=0
        while(offset<file_size):
            f.seek(offset)
            tmp=f.read(10000)
            if tmp[0]=="\x01":
                #print offset
                tmp_magic_code=tmp[1:9]
                tmp_jpg_size=tmp[9:13]
                #magic_code=unpack("i",tmp_magic_code[::-1])
                jpg_size=unpack("I",tmp_jpg_size[::-1])
                #print jpg_size
                f2=open(os.getcwd() + "/extract/" + item[:-1] + "/" + str(offset/10000) + ".jpg","wb")
                f.seek(offset + 13)
                f2.write(f.read(int(jpg_size[0])))
                print "extracting " + str(offset/10000) + ".jpg"
            offset+=10000
print "All Done!"





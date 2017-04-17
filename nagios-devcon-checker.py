#!/usr/bin/python
import sys
import optparse
import os, re
import shlex, subprocess

__author__ = 'Meir Finkelstine'
__version__= '0.1'
__program__= 'devcon emulator'




devcon_path = 'C:\\'
devcon_name = "devcon.exe"
debug = False

def parse_args():
    usage = "\tusage: %prog <command> arg1\n\
             \tClass \
             \tClassType : most \
             \tSearch Type are : \tnet,usb,hid"
    parser = optparse.OptionParser(usage=usage)
    '''
    parser.add_option("-H", "--host",   dest="hostname", type="string", help="specify hostname to run on" , default="localhost" )
    '''
    parser.add_option("-c", "--class",   dest="classname", type="string", help="Class Search" , default="find")
    parser.add_option("-t", "--classtype",   dest="classtype", type="string", help="Class Type Search" )
    parser.add_option("-s", "--search", dest="search", type="string", help="Search String" )
    parser.add_option("-m", "--message", dest="message", type="string", help="adding message to check" )
    (options, args) = parser.parse_args()

    if options.classtype is None or options.search is None:
        parser.error("incorrect number of arguments")
    return options.classname , options.classtype , options.search , options.message

def runCmd(classtype):
    #args = shlex.split(cmd)

    devcon_command = devcon_path+devcon_name+" find  *"+classtype+"*"
    try:
        if debug : print "[+] command args %s"%devcon_command
        p = subprocess.Popen(devcon_command.split(),shell=True,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
        return p.communicate()

    except OSError as e:
        print >>sys.stderr, "Execution failed", e


def devcon_status(device_id,device_name=None):
    #devcon status "@PCI\VEN_8086&DEV_1130&SUBSYS_00000000&REV_02\3&29E81982&0&00"
    device = re.sub(r'\\x0', "\\\\", repr(device_id))
    device_hwid = device.replace('\\\\','\\').replace("'","")
    devcon_cmd = devcon_path + devcon_name + " status \"@" + device_hwid.replace('\\\\', '\\') + "\""
    #print("\n[+] devcon_status : {0} device_name {1}\nCOMMAND {2}\n".format(device_hwid.replace('\'',''), device_name,devcon_cmd))

    try:
        p = subprocess.Popen(devcon_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results = p.communicate()
        r = results[0]
        #print("devcon_status output_results {0}\n".format(type(r)))
        for r in r.split('\r\n'):
            #print("status {0}".format(r.strip()))
            if "Driver is" in r and "running." in r:
                #print("status {0}".format(r))
                return True
    except:
        print("CRITICAL - Device is not Connected {0}|'Device is Offline'={1} ".format(device_name,"DOWN"))
        sys.exit(3)

def main():
    results = {}
    '''
    devcon listclass net
    '''
    ( className , classType , stringSearch, comments ) = parse_args()

    if not stringSearch:
        print "CRITICAL - You Most define string to Search"
        sys.exit(2)

    results = runCmd(classType)

    if not results:
        print "CRITICAL - devcon did not return results "
        sys.exit(3)
    c = 0
    typo = False
    tuple_list_devices = list(results)
    devices = tuple_list_devices[0]
    device_list = []

    for device in devices.split('\r\n'):
        #print( "[+] cc [{0}] data {1}".format(c,device))
        c+=1

        if stringSearch in device:
            #print("[+] stringSearch : {0} device_name {1}".format(stringSearch,device))
            d,n = device.split(":")
            device_status = devcon_status(d.strip(),n)
            device_list.append(d.strip())
            device_list.append(n.strip())
            #print("[+] device_List {0}".format(device_list[0]))
            typo = device_status

    if typo :
        print "OK - Device is Connected|'%s'=%s" %( device_list[1],"UP")
        sys.exit(0)
    else:
        if comments :
            print "CRITICAL - Device is not Connected %s|'Device is Offline'=%s " %( stringSearch, comments,"DOWN")
        else:
            print "CRITICAL - Device is not Connected %s|'Device is Offline'=%s " %( stringSearch,"DOWN")
        sys.exit(2)

if __name__ == '__main__':
    main()
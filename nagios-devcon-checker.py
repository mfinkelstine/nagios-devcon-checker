#!/usr/bin/python
import sys
import optparse
import os, re
import shlex, subprocess

__author__ = 'Meir Finkelstine'
__version__= '0.1'
__program__= 'devcon emulator'



devcon = 'devcon'
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
    devcon = "devcon.exe"
    devcon_command = "C:\\"+devcon+" find  *"+classtype+"*"
    try:
        if debug : print "[+] command args %s"%devcon_command
        p = subprocess.Popen(devcon_command.split(),shell=True,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
        return p.communicate()

    except OSError as e:
        print >>sys.stderr, "Execution failed", e


def devcon_status(device_hwid,device_name=None):
    devcon = "devcon.exe"
    #devcon status "@PCI\VEN_8086&DEV_1130&SUBSYS_00000000&REV_02\3&29E81982&0&00"
    devcon_cmd = "C:\\"+devcon+" status \"@"+device_hwid+"\""
    try:
        p = subprocess.Popen(devcon_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results = p.communicate()
        #print("results status {0} command {1}".format(results,devcon_cmd))
        output_results = results.split(' ')
        print("output_results {0}".format(output_results))
        #for r in output_results:
        #    print("status {0}".format(r))
        #    if "Driver is" in r:
        #        print("status {0}".format(r))


    except:
        print("CRITICAL - Device is not Connected {0}|'Device is Offline'={1} ".format(device_name,"DOWN"))
        sys.exit(3)



def main():
    results = {}
    win32path = os.path.realpath(__file__)+"\\lib\\"
    #devconExec  = win32path+"devcon.exe"
    devconExec = "C:\\devcon.exe"

    # to check touch screen
    # c:\devcon.exe listclass HIDClass

    if debug: print "[+] devcon execute on %s " % (devconExec)
    '''
    devcon listclass net
    '''
    ( className , classType , stringSearch, comments ) = parse_args()

    if not stringSearch:
        print "CRITICAL - You Most define string to Search"
        sys.exit(2)

    #if not os.path.isfile(devconExec):
    #    if debug : print "[+] file does not exist on %s on platform %s sep %s " %(file,sys.platform,sys.stdout.isatty())
    #    print "CRITICAL - devcon file does not exist "
    #    sys.exit(3)
        
    if debug : print "[+] Results are search type %s find string %s String to Search %s" %(classType, className , stringSearch)


    results = runCmd(classType)

    if not results:
        print "CRITICAL - devcon did not return results "
        sys.exit(3)
    c = 0
    typo = False
    tuple_devices = list(results)
    # convert tuple to string
    devices = tuple_devices[0]
    device_list = []
    #device_list = {}

    #for i in range(len(devices)):
    #    cc+=1
    #    print("[{0}] deviceList {1}".format(cc,devices[i]))

    for device_name in devices.split('\r\n'):
        if debug: print( "[+] cc [{0}] data {1}".format(c,device_name))
        c+=1

        if stringSearch in device_name:
            print("[+] stringSearch : {0} device_name {1}".format(stringSearch,device_name))
            d,n = device_name.split(":")

            devcon_status(d.strip())
            device_list.append(d.strip())
            device_list.append(n.strip())
            print("[+] device_List {0}".format(device_list[0]))

            typo = True
    sys.exit(1000)
    if typo :
        print "OK - Device is Connected|'%s'=%s" %( deviceList[1],"UP")
        sys.exit(0)
    else:
        if comments :
            print "CRITICAL - Device is not Connected %s|'Device is Offline'=%s " %( stringSearch, comments,"DOWN")
        else:
            print "CRITICAL - Device is not Connected %s|'Device is Offline'=%s " %( stringSearch,"DOWN")
        sys.exit(2)

if __name__ == '__main__':
    main()
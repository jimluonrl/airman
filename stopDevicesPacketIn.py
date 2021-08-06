#stopDevicesPacketIn.py
import airs_config


import airs_config 
import sys
import makeDropRules
import airs_flows


def stopPacketIn():
	global base_url, timeout, restUser, restPassword

	isRemove = false;
    try:
       opts, args = getopt.getopt(argv,"hb:u:p:t:r",[])
    except getopt.GetoptError:
       print('test.py -i <inputfile> -o <outputfile>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print('usage -b <baseURL> -u <restUser> -p <restpassword> -t <timeout> -r (remove stopDevicesPacketIn flow rule)')
          sys.exit()
       elif opt in ("-b"):
          base_url = arg
       elif opt in ("-u"):
          restUser = arg
       elif opt in ("-p"):
          restPassword = arg
       elif opt in ("-t"):
          timeout = int(float(arg))
       elif opt in ("-r"):
          isRemove = true

    print('Base url is: ', base_url)
    print('Rest user is: ', restUser)
    print('Rest password is: ', restPassword)
    print('Timeout is: ', timeout)

	if (!isRemove):
      makeDropRules.buildInputFile(base_url, ethTypes, priority, timeout, ifile)
      makeDropRules.py2Json(makeDropRules.buildDropFlows(ifile), ofile)
      airs_flows.post_flows(base_url, ofile)
  	else:
  	  airs_flows.clear_flowsByAppId(base_url, nrlAppId)

if __name__ == '__main__':

   stopPacketIn()

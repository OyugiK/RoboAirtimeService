
#!/usr/bin/python
#
# Instructions:
#  - read data from csv file row by row
#  - assign msisdn and amount to variables
#  - send airtime to msisdn and amount
#


#imports
import csv
import sys
import logging
import time
import datetime
from ConfigParser import SafeConfigParser
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

# parsing configs from jumo.ini
parser = SafeConfigParser()
parser.read('jumo.ini')

# set config varibles
filename = parser.get('file_config', 'path')

# create logger
lgr = logging.getLogger('AIRTIME')
lgr.setLevel(logging.DEBUG)
# add a file handler
fh = logging.FileHandler('/tmp/jumo-sms.log')
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
# add the Handler to the logger
lgr.addHandler(fh)

# declaring the timestamp variable
timestamp = datetime.datetime.now()

def main():
	# call the send sms method 
	lgr.info('**** Starting AIRTIME Service *****%s' %(timestamp))
	sendSMS()
	lgr.info('**** Stopping AIRTIME Service *****%s' %(timestamp))

def sendSMS():		
	# Specifying login credentials for africastalking
	username = "sandbox"
	apikey   = "e4a50ee75eef129462a24e809a20d0876c960c5e2d4daa358bb*********e" # enter your sandbox apikey

	# First thing we do is initiate the AfricasTalking method from the provided class
	# by creating a new instance of our awesome gateway class
	gateway = AfricasTalkingGateway(username, apikey)

	# enclose the entire algo on try/catch block to handle errors/exception that may occur on file opening
	try:

		# open the file and put it memory
		with open(filename) as f:
		    f_csv = csv.reader(f) 
		    # skip the first row that containts headers
		    headers = next(f_csv)  
		    # loop throught data row by row
		    for row in f_csv: # Time Complexity worst case scenario  [ O(n) ]
		    	# assign the variable for phone number
		    	msisdn = "+" + row[1]      
		    	masked_msisdn = row[1][6:]
		    	lgr.debug('sending airtime for msisdn = +254***%s' %(masked_msisdn))
		    	# assign the variable for amount
		    	amount = row[2]
		    	lgr.debug('amount = %s' %(amount))
		    	# Specify an array of dicts to hold the recipients and the amount to send
		    	recipients = [{"phoneNumber" : msisdn, 
		               "amount"      : "KES " + amount}]
		        # enclose the operation in try/catch to handle errors on the loop block       
		    	try:
		    		# Thats it, hit send and africastalking takes care of the rest.
		    		responses = gateway.sendAirtime(recipients) # O(n)
		    		for response in responses: # Time Complexity worst case scenario  [ O(n) ]
		    			lgr.debug( "phoneNumber=%s; amount=%s; status=%s; discount=%s; requestId=%s" % (
		                                                                       response['phoneNumber'],
		                                                                       response['amount'],
		                                                                       response['status'],
		                                                                       response['discount'],
		                                                                       response['requestId']
		                                                                      ))
		    	except Exception as e:
		    		lgr.fatal( 'Encountered an error while sending airtime: %s' % str(e))
	except Exception as e:
		    		lgr.fatal('Encountered an error on initialiasation: %s' % str(e))
		    			   
if __name__ == "__main__":
    main() # will call the 'main' function only when you execute this from the command line.
	   



	



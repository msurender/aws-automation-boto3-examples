import boto3
import time
from time import strftime
from datetime import datetime 
from time import gmtime

class AWSAutomation:

	def invoke_build(self,buildProjectName):

		client = boto3.client(service_name='codebuild', region_name='us-east-1')
		new_build = client.start_build(projectName=buildProjectName)
		buildId = new_build['build']['id']

		# NOTE - there is no waiter for code build, so for now we need to have our own loop
		counter = 0
		while counter < 6:   #capped this, so it just fails if it takes too long
			time.sleep(60)
			counter = counter + 1
			theBuild = client.batch_get_builds(ids=[buildId])
			buildStatus = theBuild['builds'][0]['buildStatus']
			
			if buildStatus == 'SUCCEEDED':
				break
			elif buildStatus == 'FAILED' or buildStatus == 'FAULT' or buildStatus == 'STOPPED' or buildStatus == 'TIMED_OUT':
				break
		
		return buildStatus

def start_time_():    
	start_time = time.time()
	return(start_time)

def end_time_():
	end_time = time.time()
	return(end_time)
    
def execution_time(start_time,end_time):
	return(strftime("%H:%M:%S",gmtime(int('{:.0f}'.format(float(str((end_time-start_time))))))))

def main():

	start_time = start_time_()

	auto = AWSAutomation()
	# NOTE - update value to pass the existing build name here.
	response = auto.invoke_build("BuildName")
	
	end_time = end_time_()
	print("Response:"+response + '| Time Taken:'+execution_time(start_time,end_time)  )

	
if __name__ == '__main__':
	main()

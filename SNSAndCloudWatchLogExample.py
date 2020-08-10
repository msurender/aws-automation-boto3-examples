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

		# there is no waiter for code build, so for now we need to have our own loop
		counter = 0
		while counter < 12:   #capped this, so it just fails if it takes too long
			time.sleep(180)
			counter = counter + 1
			theBuild = client.batch_get_builds(ids=[buildId])
			buildStatus = theBuild['builds'][0]['buildStatus']
			
			if buildStatus == 'SUCCEEDED':
				break
			elif buildStatus == 'FAILED' or buildStatus == 'FAULT' or buildStatus == 'STOPPED' or buildStatus == 'TIMED_OUT':
				break
		
		return buildStatus

	def sendSNS(self,jsonResponse):
		# NOTE - add sns topic ARN - Update below value with your sns arn
		snsTopicArn = 'arn:aws:sns:us-east-1:123456789:codebuild'		
		client = boto3.client('sns',region_name='us-east-1')
		response = client.publish(
			TopicArn=snsTopicArn,
			Message=json.dumps({'default': json.dumps(jsonResponse)}),
			MessageStructure='json'
		)

	def addToCloudWatch(self,jsonResponse):
		# NOTE - if you want to added to existing group and stream, update the values below
		logGroup='logGroupName'
		logStream='logStreamName'

		timestamp = int(round(time.time() * 1000))
		client = boto3.client('logs',region_name='us-east-1')
		
		try:
			client.create_log_group(logGroupName=logGroup)
		except client.exceptions.ResourceAlreadyExistsException:
			pass

		try:
			client.create_log_stream(logGroupName=logGroup, logStreamName=logStream)
		except client.exceptions.ResourceAlreadyExistsException:
			pass
		
		response = client.describe_log_streams(
			logGroupName=logGroup,
			logStreamNamePrefix=logStream
		)
		
		event_log = {
			'logGroupName': logGroup,
			'logStreamName': logStream,
			'logEvents': [
				{
					'timestamp': int(round(time.time() * 1000)),
					'message': time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+json.dumps(jsonResponse)
				}
			],
		}

		if 'uploadSequenceToken' in response['logStreams'][0]:
   			event_log.update({'sequenceToken': response['logStreams'][0] ['uploadSequenceToken']})

		response = client.put_log_events(**event_log)
		print(response)

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
	# pass the build name here.
	respV = auto.invoke_build("BuildName")
	
	end_time = end_time_()
	
	# create a json message for build status and send an sns notification and also add to cloud watch logs
	finalMessage = {
		"Status" : "Success",
		"Message" : "Code Build Successful",
		"ExecutionTime": execution_time(start_time,end_time)
	}
			
	print(json.dumps(finalMessage));
	auto.sendNotif(finalMessage)
	auto.putCloudWatchLogs(finalMessage)
	
if __name__ == '__main__':
	main()

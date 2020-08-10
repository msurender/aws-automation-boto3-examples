import boto3
import time
from time import strftime
from datetime import datetime 
from time import gmtime

class AWSAutomation:

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

def main():

	auto = AWSAutomation()
	
	# create a json message for build status and send an sns notification and also add to cloud watch logs
	finalMessage = {
		"Status" : "Status",
		"Message" : "Message to be sent"
	}
			
	print(json.dumps(finalMessage));
	auto.sendNotif(finalMessage)
	auto.putCloudWatchLogs(finalMessage)
	
if __name__ == '__main__':
	main()

import json
import boto3
 
# Define the client to interact with AWS Lambda
client = boto3.client('lambda')
 
def lambda_handler(event,context):
    
    records = [x for x in event.get('Records', []) if x.get('eventName') == 'ObjectCreated:Put']
    sorted_events = sorted(records, key=lambda e: e.get('eventTime'))
    latest_event = sorted_events[-1] if sorted_events else {}
    info = latest_event.get('s3', {})
    file_key = info.get('object', {}).get('key')
    bucket_name = info.get('bucket', {}).get('name')
 
    # Define the input parameters that will be passed
    # on to the child function
    
    inputParams1 = {
        "VideoName": file_key,
        "StartFrame": "1",
        "EndFrame": "10"
    }
    inputParams2 = {
        "VideoName": file_key,
        "StartFrame": "11",
        "EndFrame": "20"
    }
    inputParams3 = {
        "VideoName": file_key,
        "StartFrame": "21",
        "EndFrame": "33"
    }
    client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:497471076542:function:video-processing-child-1',
        InvocationType = 'Event',
        Payload = json.dumps(inputParams1)
    )
    
    client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:497471076542:function:video-processing-child-2',
        InvocationType = 'Event',
        Payload = json.dumps(inputParams2)
    )
    client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:497471076542:function:video-processing-child-3',
        InvocationType = 'Event',
        Payload = json.dumps(inputParams3)
    )
    
 
    return {
        "status": True
    }

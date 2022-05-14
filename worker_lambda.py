import json
import logging
import boto3
import botocore
import os
import numpy
import cv2
    

def process_video(video_file_name, start_frame, end_frame):
    
    s3 = boto3.client('s3')
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Read video file
    cap = cv2.VideoCapture('/tmp/' + video_file_name)

    # get height, width and frame count of the video
    width, height = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    
    i = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            i += 1
            if i >= start_frame and i <= end_frame:
                im = frame
                # Perform face detection of frame
                # Convert into grayscale
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                # Detect faces
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                    # Draw rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # write the frame
                cv2.imwrite('/tmp/'+str(i)+'.jpg', im)
                s3.upload_file('/tmp/'+str(i)+'.jpg',BUCKET_NAME,str(i)+'.jpg')


    except Exception as e:
        # Release resources
        print(e)
        cap.release()


    # Release resources
    cap.release()

def lambda_handler(event, context):
    
    s3 = boto3.resource('s3')
    
    
    video_file_name = event['VideoName']
    start_frame = event['StartFrame']
    end_frame = event['EndFrame']
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('event parameter: {}'.format(event))
    
    
    try:
        s3.Bucket('opencv-videos-bucket').download_file(video_file_name, '/tmp/' + video_file_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist in s3")
        else:
            raise
        
    process_video(video_file_name, int(start_frame), int(end_frame))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "images saved"
        }),
    }



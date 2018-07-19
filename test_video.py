# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from twilio.rest import Client
import pyimgur

#imgur information
CLIENT_ID = 'INSERT_HERE'
PATH = 'image.png'

#Account Sid and Auth Token From Twilio
account_sid = 'INSERT_HERE'
auth_token = 'INSERT_HERE'
client = Client(account_sid, auth_token)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 180
camera.led = False
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
face_cascade = cv2.CascadeClassifier('face.xml')
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            #minSize(30,30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
	
	print(len(faces))
        
        #print(len(faces))
        
#    if faces > 0:
#        do somethi

	
#    print("Found {0} faces!".format(len(faces)))

	for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
	
    
                
 
	# show the frame
	cv2.imshow("Frame", image)
	cv2.imwrite("image.png", image)
	key = cv2.waitKey(1) & 0xFF
	
	if len(faces) > 0:
                im = pyimgur.Imgur(CLIENT_ID)
                uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
            
                message = client.messages.create(
                        to="+19147145641",
                        from_="+15162611824",
                        media_url="%s" %(uploaded_image.link),
                        body="A face was detected!"),
                
                
                time.sleep(5)
    
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

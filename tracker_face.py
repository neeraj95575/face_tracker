import cv2
import pigpio     #this library helps to overcome the jitter problem of servo
servo = 23  #GPIO pin
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )
position = 1500  #90 degree

######## for servo motor when using pigpio ########
# 500 -> 0 degree                                                                   #
# 1500 -> 90 degree                                                               #
# 2500 -> 180 degree                                                             #
#########################################

pwm.set_servo_pulsewidth( servo, 1500 );

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #detect face
font = cv2.FONT_HERSHEY_SIMPLEX
video_capture = cv2.VideoCapture(0)


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    rows, cols, _ = frame.shape
    frame = cv2.flip(frame, 1) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(20, 20),  #  size of face  (move far the size of face decreases)
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 6)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        x_medium = int((x + x + w )/ 2)   #it is the centre of the rectangle which cover the face
        center = int(cols / 2)
        if   x_medium > center - 30:     #this condition means motor moving left
              position += 12
        elif x_medium < center + 30:   #this condition means motor moving right
              position -= 12

        if position > 540 and position < 2480: 
                print(position)
                pwm.set_servo_pulsewidth( servo, position);   #servo start moving same as face until condition is true 
                
        if position <= 540 or position >= 2480:  #if position is satisfy this condition then positon set to 1500 (90 degree)
               position = 1500

    # Display the resulting frame
        break
    
        cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    cv2.imshow('Video', frame)   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    
# When everything is done, release the capture
video_capture.release()
pwm.set_servo_pulsewidth( servo, 1500 );
pwm.set_PWM_frequency( servo, 0 )
cv2.destroyAllWindows()

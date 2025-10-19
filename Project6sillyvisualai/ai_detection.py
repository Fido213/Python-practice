from deepface import DeepFace
import cv2
import keyboard

# this is gonna be a silly python script that uses deepface to detect faces
# in a live video, a display a meme when its respective emotion is detected
# we'll use open cv for the video feed aswell as displaying the meme
# but as of rn, lets just focus on getting an emotion detection working

cap = cv2.VideoCapture(0)
# 0 is usually the default camera
# we establish a connection to it
# now we have to read frames from it in a loop

while True:
    ret, frame = cap.read()
    # cap.read() returns a boolean and the frame itself
    # the boolean for if its successful or not
    if not ret:
        break
    # now lets use deepface to analyze the frame for emotions
    result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
    # DeepFace.analyze returns a dictionary with the analysis results
    # we specified we only want emotion analysis
    # enforce_detection=False means it won't throw an error if no face is detected
    emotion = result[0]['dominant_emotion']
    # the [0] is because analyze can return results for multiple faces
    # so we want the first one
    # we get the dominant emotion from the result
    cv2.putText(frame, f"You look {emotion}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
    cv2.imshow('Emotion', frame)
    # imshow displays the frame in a window
    # the first value is just the title of the window
    print(f'Detected emotion: {emotion}')
    # now we can display the frame with the detected emotion
    if keyboard.is_pressed('q'):
        cap.release()
        cv2.destroyAllWindows()
        # release the camera so other apps can use it
        break
    cv2.waitKey(1)
    # waitKey is necessary for imshow to work properly
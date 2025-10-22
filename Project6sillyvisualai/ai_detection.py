from deepface import DeepFace
import cv2
import keyboard

# this is gonna be a silly python script that uses deepface to detect faces
# in a live video, a display a meme when its respective emotion is detected
# we'll use open cv for the video feed aswell as displaying the meme
# but as of rn, lets just focus on getting an emotion detection working

# cap = cv2.VideoCapture(0)
# # 0 is usually the default camera
# # we establish a connection to it
# # now we have to read frames from it in a loop

# while True:
#     ret, frame = cap.read()
#     # cap.read() returns a boolean and the frame itself
#     # the boolean for if its successful or not
#     if not ret:
#         break
#     # now lets use deepface to analyze the frame for emotions
#     result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
#     # DeepFace.analyze returns a dictionary with the analysis results
#     # we specified we only want emotion analysis
#     # enforce_detection=False means it won't throw an error if no face is detected
#     emotion = result[0]['dominant_emotion']
#     # the [0] is because analyze can return results for multiple faces
#     # so we want the first one
#     # we get the dominant emotion from the result
#     cv2.putText(frame, f"You look {emotion}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
#     cv2.imshow('Emotion', frame)
#     # imshow displays the frame in a window
#     # the first value is just the title of the window
#     print(f'Detected emotion: {emotion}')
#     # now we can display the frame with the detected emotion
#     if keyboard.is_pressed('q'):
#         cap.release()
#         cv2.destroyAllWindows()
#         # release the camera so other apps can use it
#         break
#     cv2.waitKey(1)
# waitKey is necessary for imshow to work properly
# now my next objective is gonna be to modularize this code into functions
# so we can call them as needed, so this main loop will be a function for
# displaying the video feed and detecting emotions
# then we can make it return the detected emotion
# and then we can have another function that takes an emotion
# and displays the respective meme for it
# ill also split this code into another main function which is to just run
# the video feed, so one function to detect emotions (returns emotion detected)
# a function to display the feed (returns the frame), and a last one to
# display memes (takes emotion as input)
# so the code will run like this:
# function 1: displays video feed, return frames
# function 2: takes frames as input, returns detected emotion
# function 3: takes detected emotion as input, displays respective meme
# outside of function is just: cv2.imshow loop that calls these functions
# this way the code is modular and easier to manage and add other features


def video_capture():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
        # yield frame is like return
        # but instead of terminating the function
        # it allows the function to be resumed later
        # so it returns frame, then waits for next call
        # then continues from here, reads next frame
        # so the flow works like this:
        # yields frame >> function pauses >>
        # router function takes it, processes it >>
        # then when router function calls next frame >>
        # function resumes here, reads next frame >>
        # and so on


def router():
    for frame in video_capture():
        # we do a for loop over the generator function
        # so for each frame yielded by video_capture
        # we assign it to frame variable, then after
        # the inner loop is done, we call it again
        # here we just route our frame to other functions
        emotion = detect_emotion(frame)
        display_feed(frame)
        emotion_analysis(emotion)
        if keyboard.is_pressed("q"):
            cv2.VideoCapture(0).release()
            cv2.destroyAllWindows()
            break


def detect_emotion(frame):
    result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False, detector_backend='yunet')
    emotion = result[0]["dominant_emotion"]
    return emotion


def display_feed(frame):
    cv2.imshow("Emotion", frame)
    cv2.waitKey(1)
    # waitKey is necessary for imshow to work properly


def emotion_analysis(emotion):
    print(f"Detected emotion: {emotion}")


router()
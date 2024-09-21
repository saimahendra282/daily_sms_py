# ok now time to run the push notification

from pushbullet import Pushbullet 
api= "o.vDwDr43vEFSBbpOkCOfRLwgymxRFGslh"
file = "text.txt"
with open(file, mode="r") as f:
  text = f.read()
  
pb = Pushbullet(api)
push = pb.push_note("Push Notification", text)

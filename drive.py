from bottle import route, run, template
# Import required libraries
import time
import RPi.GPIO as GPIO

IP_ADDRESS = '192.168.1.10'
PORT = 8080

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Define GPIO signals to use
TRIG = 17
ECHO = 27

INA = 23
INB = 24
INC = 25
IND = 8

channel = 21

GPIO.setup(TRIG , GPIO.OUT)
GPIO.setup(ECHO , GPIO.IN)

GPIO.setup(INA , GPIO.OUT)
GPIO.setup(INB , GPIO.OUT)
GPIO.setup(INC , GPIO.OUT)
GPIO.setup(IND , GPIO.OUT)

GPIO.setup(channel, GPIO.IN)

@route('/')
def hello():
    return '<b>Hi from RoboCar!</b>'

@route('/remote')
def remote():
    return '''

<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.css">
<script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
<script src="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.js"></script>
<script>
$(document).ready(function() {
  $("#moveleft").click(function() {
    $.ajax({
            url:  '/remote/left',
            type: 'GET',
            data: { command:'left' }
    });
  });
  
  $("#moveright").click(function() {
    $.ajax({
            url:  '/remote/right',
            type: 'GET',
            data: { command:'right' }
    });
  });

  $("#moveback").click(function() {
    var isRunning = $("#start").is(":checked") ? 1:0;
    $.ajax({
            url:  '/remote/back',
            type: 'GET',
            data: { command:'right' }
    });
  });

  $("#play").click(function() {
    var cmd ='start';
    $.ajax({
            url:  '/remote/play',
            type: 'GET',
            data: { command:cmd }
    });
  });
  
  $("#pause").click(function() {
    var cmd ='stop'; 
    $.ajax({
            url:  '/remote/pause',
            type: 'GET',
            data: { command:cmd }
    });
  });
});
</script>

<style>
#moveback {
  -webkit-transform: rotate(90deg);     /* Chrome and other webkit browsers */
  -moz-transform: rotate(90deg);        /* FF */
  -o-transform: rotate(90deg);          /* Opera */
  -ms-transform: rotate(90deg);         /* IE9 */
  transform: rotate(90deg);             /* W3C compliant browsers */

  /* IE8 and below */
  filter: progid:DXImageTransform.Microsoft.Matrix(M11=-1, M12=0, M21=0, M22=-1, DX=0, DY=0, SizingMethod='auto expand');
}

#moveleft {
  -webkit-transform: rotate(180deg);     /* Chrome and other webkit browsers */
  -moz-transform: rotate(180deg);        /* FF */
  -o-transform: rotate(180deg);          /* Opera */
  -ms-transform: rotate(180deg);         /* IE9 */
  transform: rotate(180deg);             /* W3C compliant browsers */

  /* IE8 and below */
  filter: progid:DXImageTransform.Microsoft.Matrix(M11=-1, M12=0, M21=0, M22=-1, DX=0, DY=0, SizingMethod='auto expand');
} 
</style>
</head>
<body>
<div data-role="page">
  <div data-role="main" class="ui-content">
    <form>
        <label for="switch">Start RoboCar</label>
        <img id="play" height="42" width="42" src='http://icons.iconarchive.com/icons/icons-land/vista-multimedia/256/Play-1-Hot-icon.png' />
        <img id="pause" height="42" width="42" src='https://www.chezyangco.fr/images/pause.png' />

        <br/>
        <img id="moveleft" height="42" width="42" src='http://s1.iconbird.com/ico/2014/1/598/w256h2561390846449right256.png' />
        <img id="moveright" height="42" width="42"  src='http://s1.iconbird.com/ico/2014/1/598/w256h2561390846449right256.png' />
        <img id="moveback" height="42" width="42"  src='http://s1.iconbird.com/ico/2014/1/598/w256h2561390846449right256.png' />
        
    </form>
 </div>
</div>
</body>
</html>
        '''

time.sleep(5)

def callback(channel):
    print("flame detected")
    
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
while True:
        time.sleep(1)

@route('/remote/play')
def play():
    GPIO.output(INA, 1)
    GPIO.output(INB, 0)
    GPIO.output(INC, 1)
    GPIO.output(IND, 0)
    return 'Starting'

@route('/remote/back')
def back():
    GPIO.output(INA, 0)
    GPIO.output(INB, 1)
    GPIO.output(INC, 0)
    GPIO.output(IND, 1)
    return 'back'


 @route('/remote/left')   
 def left():
    GPIO.output(INA, 1)
    GPIO.output(INB, 0)
    GPIO.output(INC, 0)
    GPIO.output(IND, 1)
#     time.sleep(1)
#     GPIO.output(INA, 1)
#     GPIO.output(INB, 0)
    return 'moving left..'

 @route('/remote/right')    
 def right():
    GPIO.output(INA, 0)
    GPIO.output(INB, 1)
    GPIO.output(INC, 1)
    GPIO.output(IND, 0)
#     time.sleep(1)
#     GPIO.output(INA, 0)
#     GPIO.output(INB, 1)
    
 @route('/remote/pause')
 def pause():
    GPIO.output(INA, 0)
    GPIO.output(INB, 0)
    GPIO.output(INC, 0)
    GPIO.output(IND, 0)
    return 'reverse'
    time.sleep(1)
    left()
        
    
stop()
while True:
    GPIO.output(TRIG, 0)
    time.sleep(0.1)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    
    while GPIO.input(ECHO)==0:
        pulse_start =time.time()
    
    while GPIO.input(ECHO)==1:
        pulse_end =time.time()
    
    pulse_duration =pulse_end - pulse_start
    distance = pulse_duration*17150
    distance = round(distance ,2)
    if distance < 15:
        stop()
        time.sleep(1)
#     else:
#         x = input()
#     if x == 'w':
#         forward()
#     elif x == 's':
#         backward()
#     elif x == 'd':
#         right()
#     elif x == 'a':
#         left()
#     elif x == ' ':
#         stop()

try:
    run(host = IP_ADDRESS, port= PORT)
except(KeyboardInterrupt):
    # If a keyboard interrupt is detected then it exits cleanly!
    print('Finishing up!')
    GPIO.output(17, False)
    GPIO.output(18, False)
    GPIO.output(22, False)
    GPIO.output(23, False)
    quit()
    

# here is the code for the raspberry synth, created as a team effort by the developers
# the code is relatively and mostly works around an indefinite while loop that activates as
# soon as the synth is powered on
# these import functions are necessary for the synth to work fully
import explorerhat as ex
import time
from math import *
import mido


# initialising variables that play an important role in the synth's performance
button_on = 0
voice_active = 1
py_pan = 1
midi_output = mido.open_output()
midi_message = mido.Message('note_on', note=0, velocity=0)


while True:
    time.sleep(0.2)
    # turns all lights off by default and only turns them on if they're necesary to display what is currently being used in the synth
    joystick_click = not ex.input.one.read()
    ex.light.blue.off()
    ex.light.red.off()
    ex.light.green.off()
    ex.light.yellow.off()

    # these 4 if statements alter the value of voice_active to correspond to what ever button is pressed
    if ex.touch.five.is_pressed():
        voice_active = 1
    if ex.touch.six.is_pressed():
        voice_active = 2
    if ex.touch.seven.is_pressed():
        voice_active = 3
    if ex.touch.eight.is_pressed():
        voice_active = 4
        
    # this while loop is used for our preset waveforms, when the user presses down the joystick and selects a button from 1 to 4 and preset waveform is input
    # to whatever voice is currently active at the time
    while(joystick_click == True):
        rasp_preset = open("rasp_preset.txt","w")
        # button one corresponds to a sine wave
        if(ex.touch.one.is_pressed()):
            ex.light.blue.on()
            # each waveform is written into a .txt file to be read by pure data and the joystick_click value is reset to false to exit this while loop
            rasp_preset.write("; \n")
            rasp_preset.write("sin" + str(voice_active) + " 1;")
            rasp_preset.close()
            # earlier builds of the program didn't include this lane and had a bug in which the program got stuck within this while loop and the program no longer
            # functioned properly
            joystick_click = False
        # button two corresponds to a sawtooth wave
        if(ex.touch.two.is_pressed()):
            ex.light.yellow.on()
            rasp_preset.write("; \n")
            rasp_preset.write("saw" + str(voice_active) + " 1;")
            rasp_preset.close()
            joystick_click = False
        # button 3 is a square wave
        if(ex.touch.three.is_pressed()):
            ex.light.red.on()
            rasp_preset.write("; \n")
            rasp_preset.write("square" + str(voice_active) + " 1;")
            rasp_preset.close()
            joystick_click = False
        # button 4 is a triangle wave
        if(ex.touch.four.is_pressed()):
            ex.light.green.on()
            rasp_preset.write("; \n")
            rasp_preset.write("tri" + str(voice_active) + " 1;")
            rasp_preset.close()
            joystick_click = False
        # the actual messages to send to the oscillators for the synthesiser are stored in the pure data patch, this makes for a cleaner program as it removes unecesary code because
        # the preset waveforms do not rely on the output of the joystick to function


    # this short if statement carries out the pitch changing function
    if button_on == 0:
        x_val = ex.analog.one.read()
        y_val = ex.analog.two.read()
        # the y and x position of the note are used for velocity and pitch
        note_vel = int(y_val * 20)
        pitch_freq = (x_val - 0.8) * 1000
        print(pitch_freq)
        # the conversion from frequency to midi was calculated using the formula
        pitch_midi = int((12/log(2)) * log(pitch_freq/27.5) + 21)
        # here we set up the MIDI message to be sent through to pure data
        midi_message = mido.Message('note_on', channel=0, note=0, velocity=0)
        midi_message.note =pitch_midi
        midi_message.velocity = note_vel
        midi_message.channel = voice_active-1
        midi_output.send(midi_message)
        # here the message is sent using the aconnectgui utility to an ALSA port in pure data itself
        midi_message = mido.Message('note_on', channel=voice_active, note = pitch_midi, velocity = note_vel)
        
    # this while block is for the pan and hi pass filter
    while(ex.touch.one.is_pressed()):
        rasp_pan = open("rasp_pan.txt","w")
        # blue light turns on to indicate the synth is in edit mode
        ex.light.blue.on()
        x_val = ex.analog.one.read()
        py_pan = x_val / 5
        rasp_HI = y_val * 4000
        # the voice_active variable must be added as a str value to the output this is so that the synth in pure data will send the value of the cutoff frequency
        # for the high pass filter to the correct, indicated by the value of voice_active
        rasp_pan.write("; \n")
        rasp_pan.write("pan " + str(py_pan) + "; HI" + str(voice_active) + " " + str(rasp_HI) + ";")
        rasp_pan.close()
        
    while(ex.touch.two.is_pressed()):
        rasp_LFO = open("rasp_LFO.txt","w")
        ex.light.yellow.on()
        x_val = ex.analog.one.read()
        y_val = ex.analog.two.read()
        LFO_rate = x_val
        LFO_depth = y_val * 3
        # the LFO rate and depth is the same for all voices so there is no need for voice_active to be used
        rasp_LFO.write("; \n")
        rasp_LFO.write("LFO_rate " + str(LFO_rate) + "; LFO_depth " + str(LFO_depth) + ";")
        rasp_LFO.close()

    # these two while loops function the same as the previous two, the voice_active string is included so it knows which voice to send the value to
    while(ex.touch.three.is_pressed()):
        rasp_AR = open("rasp_AR.txt","w")
        ex.light.red.on()
        x_val = ex.analog.one.read()
        y_val = ex.analog.two.read()
        rasp_ATK = x_val * 60
        rasp_REL = y_val * 200
        rasp_AR.write("; \n")
        rasp_AR.write("ATK" + str(voice_active) + " " + str(rasp_ATK) + "; REL" + str(voice_active) + " " + str(rasp_REL) + ";")
        rasp_AR.close()

    while(ex.touch.four.is_pressed()):
        rasp_filter = open("rasp_filter.txt","w")
        ex.light.green.on()
        x_val = ex.analog.one.read()
        y_val = ex.analog.two.read()
        rasp_low = x_val * 4000
        rasp_del = y_val * 200
        rasp_filter.write("; \n")
        rasp_filter.write("LOW" + str(voice_active) + " " + str(rasp_low) + "; DEL" + str(voice_active) + " " + str(rasp_del) + ";")
        rasp_filter.close()
        
# the values of each variable (LFO depth, high pass cutoff, etc...) only update once the button is released, which is an important thing for the user to mention.  
    


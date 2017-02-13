#waveform is the name of the variable whilst it is saved as waveform.txt
#could probably do more sensible variables but its not important right now
#the for loop could be replaced by a function so it lasts as long as a button is
#pressed for
#I have no idead what "w" does maybe experiment with it?
waveform = open("wave.txt","w")
waveform.write("; \n")
waveform.write("osc1 sinesum 131 ")
for i in range(10):
    waveform.write(input("Enter a number: "))
    waveform.write(" ")
    
#this writes a normalize function after the draw waveform part
#normalize causes all values to be between 1 and -1 i think so by using it
#it doesn't matter what values we input from the accelerometer it should work    
waveform.write("\n; \n")
waveform.write("osc1 normalize ")
waveform.close()

# About the project:
Hey Visitors

It was somewhere between spring and summer 2023 when i decided to build the radio from the game [Portal](https://store.steampowered.com/app/400/Portal/)!
I did this to improve my understanding of IOT devices, do something with my RPI and learn a bit about electronics. 

## The journey:
First of all, I had a hard time deciding where to start, but as I am primarily a software developer, i started with the python script for the project. You can look up the code in this repository =)

Then, i 3D printed the case using [this](https://www.myminifactory.com/object/3d-print-portal-radio-50006) model by [Alex I](https://www.myminifactory.com/users/Aibot). 

The tricky part was the assembly, as i decided to use a button and a standard potentiometer paired with a MCP3008 ADC to read user input (Nowadays, i would just use a KY-040 and have a way better product in the end). 
Also, i wanted the radio to:
- Play the default upbeat still alive from the game
- Be usable as a bluetooth speaker
- be able to run without a power cable
- be able to run the game portal itself (at least for a few minutes because of the heat thats produced)

As you can see, this thing is not your average Portal Radio Prop, and it took about 3 months of work to finish. So let's get to where it is now and talk about what you should keep in mind if you want to replicate my version of this thing:

1. Use something like a KY-040 instead of the button+potentiometer+adc combination i used!
2. Finish the electronics before printing the case
3. Find a fitting method to power the prop (i soldered a fitting accumulator to do the job)

...

### Setting up ###

The script uses xdotool to control volume, mpd and mpc to play a stream and python Flask to display the web interface. Install them all.

    sudo apt install mpd mpc xdotool python3-pip
    pip3 install flask


The next step is to configure the configuration file: 
    
    /etc/mpd.conf.

In the first section: Files and directories, change all paths to a folder in your home location like: 

    /home/<user>/.mpd/

Change user from mpd to your user name.

In the Audio Output section, to find the correct setting I had to run: 

    aplay -l

and got response:

    card 0: Generic [HD-Audio Generic], device 3: HDMI 0 [HDMI 0]
        Subdevices: 1/1
        subdevice #0: subdevice #0
    card 1: Generic_1 [HD-Audio Generic], device 0: ALC256 Analog [ALC256 Analog]
        Subdevices: 1/1
        Subdevice #0: subdevice #0

So my setting is:

    audio_output {
        type		"alsa"
        name		"Generic_1" 

Now restart your computer or try just the mpd service:

    sudo systemctl restart mpd.service

Try the mpd settings using:

    mpd --stdout --no-daemon --verbose

If any errors are displayed, you need to solve them and restart the mpd service. For your conveniance, there is an mpd.conf example file in this folder.

Test MPC:

    mpc help
    mpc add https://stream.vanillaradio.com:8028/live
    mpc play
    mpc stop



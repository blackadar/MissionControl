# Progress Updates


## Week One (October 29 - November 5)

Our team put a large amount of effort into the project this week, and therefore we are very significantly ahead of schedule.
Due to recently discovered foreseeable time restraints at the end of the semester, we felt it better to use time now and get a head-start on
the project. If more time is available at the end of the semester than had been allocated in the proposal, the modular nature of the project
will allow us to further expand the tasks our devices can perform.


### Last Week
* Set Up Repository (Team)
    * GitHub set up with package structure
* Identify Deliverable Items (Team)
    * See README.md
* Made Plan (Team)
    * See README.md
* Implemented Telnet servers for Devices and Hypervisor (Jordan)
    * Implemented hub.reception, hub.vector, and spoke.junction


### This Week
* Expand Command-Sets (Team)
    * Added sys, update, status, save, discover
* Test for Edge Cases (Ryan)
    * Found and fixed many bugs in saving and restoring state
* Add Device Tasks (Ryan)
    * Morse Code and Printer for debug and testing, only CLI output for now.


### Blocking Issues
* None identified

### Comments
1. For the stuff last week and this week, you might want to add the person who is responsible for the item. E.g., Set up Repo (Jordan), Indentify Deliverables (team) (COMPLETE)
2. Describe a more about the work item, not just the title (COMPLETE)


## Week Two (November 4 - November 10)

The team completed a large amount of testing of the telnet servers, encountering many issues with multi-threading and exception handling.
Both servers are now updated to handle many users and long-running tasks without interrupting any one user's experience.
The two Raspberry Pi computers were configured and set up to use the VPN for the demo. We are using a VPN due to the school network's client isolation.
An LED 'Mood Light' kit was purchased and GPIO headers were soldered onto the Pi Zero and the HAT. 

### This Week
* Test for and Handle Multiple Users (Team)
    * Multi-threading from the threading module was implemented in junction and reception
    * Calls to long-running device tasks are threaded separately from the server
* Configure Raspberry Pi Computers (Jordan)
    * Flash SD cards and install necessary tools
    * Configure VPN
    * Install project
* Solder GPIO Headers (Ryan)
    * Raspberry Pi Zero
    * Unicorn pHAT

### Blocking Issues
* None identified

### Comments


## Week Three (November 11 - 17)
This week's focus was on the actual implementation of the physical devices in the code, the spoke.devices module.
All interactions with the Lamp device (The 'Mood Light' kit device) were written at an LED by LED level.
A decent amount of time was invested into transitions and effects for this device which will really show the diversity of possibilities for this software.
It was discovered that the Alexa API does not support direct telnet or SSH control from Alexa enabled devices.
Implementing Alexa control into this project is most definitely possible, however it would require a call to a web service running another service to handle passing through telnet interaction.
It was decided that this introduces a large amount of complication, and would waste time for a feature we can already demonstrate with Siri, which supports SSH directly.

### This Week
* Physical Device Implementation (Team)
    * spoke.devices now contains functions to control physical devices attached to Raspberry Pi computers
    * Improvements to existing 'test' code were made as it was apparent that it would need to be more modular
* Testing with Physical Devices (Team)
    * Morse Code LED function was tested and verified to be working
    * Lamp functions were improved and added
    * Simultaneous, grouped devices were tested
    
### Blocking Issues
* None identified

### Comments

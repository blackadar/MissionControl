# Mission Control

## Network Device Control Framework
Mission Control provides a single access point Telnet server to control arrays of network devices.
Devices may have any number of services available to control, and any number of arguments to these services.
This tool will allow developers to easily abstract and control single devices, and large groups of devices in other applications
without the complications of complex network interactions and lower-level programming.

### Functionality: (What?)
Connect physical devices into a telnet environment for easy scripting and control.
### Purpose: (Why?)
There is no simple control method for maker projects over a network, and simple programs are frequently
complicated by repetitive and often suboptimal networking procedures.
### Implementation: (How?)
A Python-based telnet hypervisor and client infrastructure allows makers to only write for their devices
and clients, rather than create a standard for their entire network.

## Deliverable Items
- Hub Package
    * Hypervisor Telnet Server 'Reception'
    * Runs on a separate computer, to control devices on spokes
    * Can be run with redundancy, separated from spoke clients
- Spoke Package
    * Client Telnet Server 'Junction'
    * Runs on the controller for a physical device
    * Accepts direct commands and commands from the hub
    * Exposes available 'tasks' to clients for control and status
- Demonstration of Functionality with a physical device
    * Control from digital assistant (Siri)
    * Control from Telnet commands
    * Control from an abstract GUI

## Plan
- Week One: Hub and Spoke Telnet (COMPLETE)
- Week Two: Command and Functionality Addition (COMPLETE)
- Week Three: Physical Device (Task) Creation (COMPLETE)
- Week Four: Application Demonstrations (Smart Assistant, GUI)
- Week Five: Presentation


## Team
`Jordan Blackadar` jordan.blackadar@outlook.com

`Ryan Lawton` lawtonr2@wit.edu

# Comments
1. I would like to see the breakdown of the description by breaking it down to What? Why? and How? (COMPLETE)
2. Need to be more specific on the deliverables. E.g., What does Hub Package do? What are the Hub Package features? (COMPLETE)
3. Adjust the plan to fit in 5 weeks schedule including presentation and wrap-up (COMPLETE)

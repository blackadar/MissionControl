# Mission Control

## Network Device Control Framework
Mission Control provides a single access point Telnet server to control arrays of network devices.
Devices may have any number of services available to control, and any number of arguments to these services.
This tool will allow developers to easily abstract and control single devices, and large groups of devices in other applications
without the complications of complex network interactions and lower-level programming.

## Getting Started
### Installation
- Environment
    * This project depends on Python 3.6.5+ and the miniboa package
    * Install Python 3.6.5+ from `https://www.python.org/downloads/`
    * Install miniboa using `python3 -m pip install miniboa`
- Network
    * Devices must be accessible on a network level. Junction servers must have network access to Reception.
    * For Internet access of your devices, port forward to Reception.
- Configuration and Development
    * Newly written device handlers should be placed in spoke.devices, and their physical connection mapped in spoke.devices.pinout
    * Newly written routines and tasks for devices should be placed spoke.tasks
    * Junction accessible tasks should be referenced in spoke.junction so that clients may enable them
    
### Execution
- Reception (Hypervisor)
    * Run hub.reception with `python3 -m hub.reception &` from the project top-level directory
    * To redirect console output to a logfile, use `python3 -m hub.reception &> log.txt &`
- Junction (Device)
    * Run spoke.junction with `(sudo) python3 -m spoke.junction &` from the project top-level directory
    * To redirect console output to a logfile, use `(sudo) python3 -m spoke.junction &> log.txt &`
    
### Features and Operations

'help': List all commands and help text

'tell': Issue a command to a vector or group. tell <name/group> <arguments>

'sys': Issue a raw Junction system command. sys <name/group> <arguments>

'list': Without arguments, lists all entities. With arguments, lists services. list <*name/group>

'add': Add a new vector or group. add <'vector'/'group'> <name> <*IP Address> <*Port> <*Vector Names>

'remove': Remove a vector or group. remove <name>

'assign': Add a vector to a group. assign <vector> <group>

'update': Update services available for all vectors and groups.

'status': Return a formatted list of the status of a service on vector or group of vectors. status <'vector'/'group'> <service>

'save': Save vectors and groups to local server files for recovery after restart.

'discover': Formatted list of commands.

'end': Terminates Telnet session.

'exit': Terminates Telnet session.

'stop': Stops the reception service, closing all connections.

## Project Plan and Information
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

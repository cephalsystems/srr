Sample Return Challenge
=======================

This repository contains source code and documentation for the NASA Sample Return Challenge.  
It is organized as a stack of ROS Hydro packages.

Hardware configuration
----------------------
| USB device   | Symlink             | Position | Connection                   |
| ------------ | ------------------- | -------- | ---------------------------- |
| Roboclaw 30A | /dev/roboclaw_drive | TOP      | pci-0000:00:14.0-usb-0:4:1.0 |
| Roboclaw 15A | /dev/roboclaw_rake  | MIDDLE   | pci-0000:04:00.0-usb-0:1:1.0 |
| Roboclaw 15A | /dev/roboclaw_bag   | BOTTOM   | pci-0000:04:00.0-usb-0:2:1.0 |

| Eth Device | IP Address | Subnet      |
| ---------- | ---------- | ----------- |
| em1        | 10.0.1.1   | 255.255.0.0 |

Contents
--------
  * src - Source code for ROS packages.
  * puppet - System configuration files for puppet.

Copyright Notice
----------------
Copyright (C) 2013. All rights reserved.
  * Prasanna Velagapudi \<psigen@gmail.com>
  * Pyry Matikainen \<pkmatikainen@gmail.com>
  * Michael Dawson-Haggerty \<mik3dh@gmail.com>

This repository is *not* open source.

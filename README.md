# lostarm
An ARM CortexM3 environment

This started years ago on SourceForge, this is an major update to that package

The primary thing it demonstrates is how to create a proper HAL and KAL layer that seperates the OS and HARDWARE so that the app runs in multiple places.

One thing that HAL writers don't get well is what I call "complex devices" - for example - often a timer module can be used to create a PWM motor control system.

They then try to create a timer HAL with features that support a motor, when instead they should be writing a motor control HAL.

Likewise, a socket interface - everybody says they have a BSD Socket implimentation - yea, right - they don't it is BSD in concept but there are enough things different in header files that you end up with a million or two #ifdef crazyness fixes in your code

The aim here is to demonstrate how to "do it right"... Ha ha..

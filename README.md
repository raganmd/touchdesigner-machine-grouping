# TouchDesigner Machine Grouping
*A first look at possible mechanisms for handling mirrored networks*

## Overview
Here you'll find an example network that lets you see some of these ideas in action.

To configure locally, start the `machine-grouping.toe` twice so that you have two processes running simultaneously. On `base_project` set one project's role to be `Controller` and the other to be `Draw`. 

On the `Controller` machine, in `\base_project\base_scenes\base_scene_01` you can now change any parameter on any operator tagged with `syncPars` and you should see the changes reflected on the machine with the `Draw` role. 

There are some limitations on this approach - most importantly that it only really syncs parameters and not operator locations or connections. There is a mechanism for handling re-loading changed toxes locally, but to make that work across the network correctly would take a little more fussing. 

Depending on your configuration you may be able to use this to a limited degree for a show, but I wouldn't recommend this kind of approach.
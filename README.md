# Eggbot
Basic text pusher with embed message functionality

## Discord
[![Server Invite](tutorial/invite.png)](https://discord.gg/rTfkdvX)

## Commands
e!help: help

e!about {OPTIONAL: @user or user id}: about the speaking/tagged user

e!test_args {arguments}: list of args

e!kiri: displays an image of Eijiro Kirishima from My Hero Academia [request from Franky Morrison#6669]

e!song: The screams of the damned (WIP)

e!github: Links to this Github Repo

e!invite: Links to an invite link for Eggbot.

e!server: DMs you an invite to the official Discord Server

e!timer {number} {time unit}: Creates a timer that pings the requesting user after a specified time.

e!rateFood: Rates food. [beware foul language]

e!get_icon: Links to a copy of the current server's icon.

e!admins: Lists the admins for the current copy of Eggbot.

e!settings: Displays the logging configuration for the current instance of Eggbot.

egg: egg

e!eggCount: counts the day's eggs

simp: SIMP

moyai: 🗿

### Economy Commands

e!fridge: Shows the number of global and server eggs you own.

e!shop: Displays the selection of items on sale.

e!buy: Buys an item from the shop.

e!inv: Shows your inventory.

e!bank: Shows the current number of server eggs donated to the server.

e!goals: Displays the server goals. One can contribute to the funding of the goals by using e!donate.

e!donate {number}: Donates the specified number of eggs to the server.

e!notifs {on/off}: Toggles notifications for eggs earned.

### Server Admin-only Commands

e!vacuum {number}: Mass deletes {number} messages. 

e!joinRole {@role}: Sets a role for automatic assignment when a member joins the server. (requires bot to be online)

e!setGoal {cost} {name}: Sets a server goal.

e!deleteGoal {name}: Deletes a server goal.

e!addEggs {number}: Adds eggs to the server bank.

e!removeEggs {number}: Removes eggs from the server bank.

e!confirmGoal {name}: Confirms goal completion. (Deducts eggs from the server bank, deletes goal) 

### Eggbot Admin-Only Commands

e!say: says whatever you tell it to say

e!shutdown: shuts the bot down without needing to manually stop the script

e!print_emoji {emoji}: prints the emoji code in terminal

e!bee: Prints the bee movie script 

e!roleGiver {@role/role id} {emoji} {color name}: Creates an automatic role giver with the specified parameters.

e!addRole {@role/role id} {emoji}: Adds a role to a recently made role giver (in the same channel).

e!reloadRoles: Reloads the role database from a backup.

e!backupRoles: Backs up the roles to a "roles.json.bak" file.

e!spam: Toggles spam mode for "egg" command

e!botSpam: Toggles processing of bot commands for "egg" and "simp" commands (recommended ON when with multiple instances of Eggbot) 

e!log: Toggles message logging

e!auditLog: Toggles logging of admin commands



## Official Host (Only on when TheEgghead27 is online)
https://discord.com/api/oauth2/authorize?client_id=681295724188794890&permissions=272104513&scope=bot

## Self-Host
For self hosting instructions, check https://github.com/TheEgghead27/Eggbot/blob/master/INSTALL.md

# [Forge of Empires](https://en0.forgeofempires.com/page/) Bot


A simple bot to do automate the main functions of [Forge of Empires](https://en0.forgeofempires.com/page/)

*Purely educational and to fuel curiosity*


## Features

- Collects and starts production buildings (supplies)
- Collects and starts good buildings (goods)
- Collects residential buildings (coins)
- Collects the silver from your tavern
- Sits in your friends tavern
- Polishes your friends / guild members / neighbours buildings

## TODO

- [ ] Auto-login
- [ ] Treasure Hunt
- [ ] Auto-build and complete troops
- [ ] Auto-scout provinces
- [ ] Auto-balance goods
- [ ] Auto-fight undefended cities + plunder
- [ ] More


## Install

- git clone https://github.com/WallyCZ/foe-bot.git
- cd foe-bot
- pip install -r requirements.txt
- Read the comments inside of *foe/config/foe.yml* and update the values
- python main.py or

- main.py takes --userKEy, --sid, --configFile to start bot dynamically
- 
```bash
  main.py --userKey USER_KEY --sid SID
```
- python monitor.py (in another process if you want to see some live updating)


:star: Star the repo if you use this, would be nice to know if people are :) :star:

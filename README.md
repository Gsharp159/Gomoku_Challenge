# Gomoku Challenge
I'm working on a personal project to make a gomoku game! The end goal is to make a (decent) computer player, although I've gotten sidetracked by a number of things and it currently has too many different unfinished ends to do anything.

### What exactly are you looking at?
Initially, I wanted to just make a quick game in pygame that had a good enough AI to prove a point, but I am not one to leave it at an _okay_ attempt, so it kind of devolved as I went in over my head. Because my strongest language is python and it started out as purely python, the main files were/are all python. I moved some of it into other files to simplify things and it quickly turned spaghetti, so I'm reimplementing it in c++ (slowly). I'm hoping my first attempt will help me delay the inevitable spaghettification.

Inside ```/Gomoku``` is ```/algorithms``` where the meat resides, and ```'GUI.py'``` is my main driver. I will ask for forgiveness on some of my naming schemes, I tried to organize to late and a lot ended up in the ```__init__```s that probably should not be in an ```__init__```.

In short: it is a hot mess but it is _my__ hot mess 🥺

### Future Goals and Ideas
- [ ] Create a number of different algorithms, and give a user the choice of which they want to play against! This would allow for tournaments and interesting gameplay
- [ ] Move the main code from python to c++, I'm learning c++ and the speed improvement will be greatly appreciated. Don't judge my c++ code however
- [ ] Create a simple debugging GUI
- [ ] Create a visual game with game style elements that build on gomoku, such as levels or opponents who increase in difficulty
- [ ] Finish eradicating goblins from my sad attempt at deep q learning, making custom tensorflow training loops is harder than I thought :skull:
- [ ] Make it compatible with piskvork and submit my strongest algorithm to [Gomocup](https://gomocup.org/)

### Aspirations, would be nice to achieve but are out of the scope of this project or deserve their own repos
- [ ] Implement online multiplayer
- [ ] Create an iOS version of the game

### If you have any ideas or critiques:
I am doing this primarily for my ownn fulfillment, but I also honestly have no clue about some things because I leanred by doing so I don't understand some of the formal 'best' practices. That said, I would appreciate if anybody smarter than me randomly stumbled across this and decided to give me any tips. (In particular, anything related to github folder structure conventions and releases)


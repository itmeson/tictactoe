# tictactoe
An exploration of tic-tac-toe bots and learning agents for a high school computational thinking class.

After two trimesters with this project, one where the code was written in jupyter notebooks and one where it was ported to a repl.it project template, I've got some more ideas on where to go with it.

 * the programming assignment for students is to write a hard-coded bot that can complete a legal game of tic-tac-toe, regardless of the moves made by the opponent.  It doesn't have to play "well".
 * their bot needs to be playable against a human, random, menace, and other yet-to-be-written player-agents
 * it's really hard for students to visualize the move-space, even for a "simple" game like tic-tac-toe
 * it would be a lot more fun for students if it was simple to setup matches between their bots, but it's simpler for them if they are only writing for 'X'
 * the AI portion of the assignment is about how their bot fares against different learning approaches, and then how well the learner that trained against their bot does against others
 * the experiment interface is confusing
 
Here's some potential things to do to address some of these:
 - [x] Raise an exception when an illegal move is made.  Currently an error message is printed and control returns to the Game class, which then returns to the Agent.  If the bot is deterministic, this means that the bot will keep making the same bad move, and there isn't an easy way for the student to figure out where the faulty logic happened.  Raising an exception allows the possibility of reporting the board state and the move that was made to facilitate debugging.
 - [ ] Catch the invalid move errors in the Experiment class (?), allow inspection and visualization of bad move if in interactive mode (like in a notebook or in repl.it)
 - [ ] Change the menace approach to use weights for each potential move.  This will make the playbook easier to inspect, decrease the memory requirement dramatically for long training runs, and will make move selection faster after long training runs. It may also make it easier to change or experiment with the update rules so different reinforcement approaches can be tried.
 - [ ] Make visualization tools for the playbook and move history.  These will be interesting at the least, and potentially help students understand the differences in results for different approaches and training regiments.  Visualization of the move history will aid in debugging.
 - [ ] Make submission be of a single module file, through ______ (?), to make automated testing and head-to-head runs easier.  This will mean changing the way the module works, with a main.py, import of the classes and of the student bot
 

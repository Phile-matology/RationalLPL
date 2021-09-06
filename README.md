# Rational LPL

This is a simple attempt to verify the rationality of LPL's competition system.

## Explanations

- 'Print' is used for the display of single simulation results, including each small game of each bo5, which allows you to start your own version of the playoff journey, but their victory and defeat can not be controlled.
- Mass simulation is based on extreme changes to observe the impact of team level gap in the playoffs on the probability of winning the championship in the regular season.

- In particular, comparative mass simulation is used to compare the rationality of the old and new LPL competition system.

## How to use
- Update the rank list to use the latest regular season rankings.

- Modify some comments in the init function to enable the custom team name mode. (note that this function requires input once for each simulation. If the change is used for large-scale simulation, please modify the rank list)

- Since it's developed for LPL, competition systems are named by Chinese, and example are given in the program.
- 0.5 is the basic level of Playoff teams, and flawless team are defined as 1, so the variable used to describe the extreme difference should be between 0 and 0.5.

## Result

![验证结果](https://cdn.jsdelivr.net/gh/Phile-matology/Picture@master/img/%E9%AA%8C%E8%AF%81%E7%BB%93%E6%9E%9C.png)

The x-axis is used to indicate the poor strength of the team, and the y-axis indicates the probability of winning the championship in the regular season. It's obvious that double elimination performs better when the difference is insignificant.
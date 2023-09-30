# retirement-plans

Tool to fascilitate investment decisions between Roth and traditional retirement accounts.

You can now run this project on [Google Colab](https://colab.research.google.com/drive/1fQHGKQeZxlU-GnJP_kfV_JBNT7Nr-kEf)!

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fQHGKQeZxlU-GnJP_kfV_JBNT7Nr-kEf)

## Description

This tool takes various inputs (such as projected salaries, retirement age, and life expectancy) in order to determine your funds in retirement. The program determines your funds in the case that you contribute to a Roth account for the first *x* years that you work, and then switch to traditional for the remaining years (or vice versa). Funds shown are post-tax. Thus, you can see whether it is best to start by contributing to either Roth or traditional, when it is best to switch, and how big a difference this makes to your retirement funds.

## Usage

To launch the program on Google Colab, click the button below.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fQHGKQeZxlU-GnJP_kfV_JBNT7Nr-kEf)

To run the program locally on a terminal, follow the steps below.

Download all files, then run `python3 main.py`. Follow the prompts in terminal to input the required values. If no value is provided, program will use default values (or last used values).

To automatically fill in default values without being prompted, run `python3 main.py d`.

To automatically fill in the last used values from a previous execution, run `python3 main.py p`.

To automatically fill in values from another file, run `python3 main.py use [filename]`. Values should be in JSON format. If you don't know how to properly format the file, simply run the code with any other values, then copy the "history.txt" file and substitute in the desired values.

## Screenshots

The following figure is a sample output of the program.

![](https://github.com/ekestelman/retirement-plans/blob/main/Retirement%20Images/main_plot.png)

<!--
Using specified inputs, the axes display two curves. The blue represents first contributing to a Roth account, then switching to traditional after _x_ years. The orange represents first contributing to a traditional account, then switching to Roth after _x_ years. Using the Roth first strategy gives the best results if this user switches to traditional in 17 years. The traditional first strategy is best if this user switches immediately (that is, they would only ever contribute to Roth). In this case, we can likely conclude that it is best for this user to contribute to a Roth account for now, and should consider switching at some time in the future (possibly in 17 years).

The pie charts show this user's retirement income breakdown for the maximum of each curve. That is, the Roth first pie chart is for the Roth first strategy and switching in 17 years. the trad first pie chart is for the trad first strategy and switching immediately.
-->

## Disclaimers and Explanations

For more information on how the code works and what factors are and are not considered, please see the [Explanations](https://colab.research.google.com/drive/1fQHGKQeZxlU-GnJP_kfV_JBNT7Nr-kEf#scrollTo=Explanations) on the project's Colab.

I am not a financial expert. This program was made for fun, and I hope you enjoy! If something looks fishy, or if you like what you see, I would love to hear your thoughts.

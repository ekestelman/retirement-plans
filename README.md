# retirement-plans
Tool to fascilitate investment decisions between Roth and traditional retirement accounts.

## Description

This tool takes various inputs (such as current and projected salaries, years in work force, anticipated years in retirement, and expected yearly returns on investments) in order to determine your funds in retirement. The program determines your funds in the case that you contribute to a Roth account for the first x years that you work, and then switch to taditional for the remaining years (or vice versa). Funds shown are post-tax. Thus, you can see whether it is best to start by contributing to either Roth or traditional, when it is best to switch, and how big a difference this makes to your retirement funds.

## Usage

Download all files, then run `python3 main.py`. Follow the prompts in terminal to input the required values. If no value is provided, program will use default values (or last used values).

To automatically fill in default values without being prompted, run `python3 main.py d`.

To automatically fill in the last used values from a previous execution, run `python3 main.py p`.

To automatically fill in values from another file, run `python3 main.py use [filename]`. Values should be in JSON format. If you don't know how to properly format the file, simply run the code with any other values, then copy the "history.txt" file and substitute in the desired values.

## Disclaimers and Explanations

This program does not currently take into account other sources of income such as social security or pensions, only funds that were invested into retirement accounts such as a 401k or IRA. It assumes a contribution limit of $22,500. The program works with the assumption that whatever amount you are willing to contribute to a Roth account, you should be comfortable contributing some amount more to a traditional account. This additional amount is computed in the program, and is based on the tax rate for your income. While Roth contributions are capped at the contribution limit, for the years that one contributes to a traditional account, the program assumes that you may still invest the aforementioned additional amount into a private account, still for retirement. However, some adjustments still have to me made with regards to how this amount is calculated, as it is not tax deferred. Capital gains taxes are assumed to be 15%. Taxes are computed based on the 2023 brackets for a single filer in New York City (that is, it considers NYC, NY state, and federal income tax). Taxes are calculated using my best understanding of tax rules. While I have done my research on the matter, I am not an expert and my understanding should be treated with a healthy dose of skepticism. The program also does not account for continued growth during retirement: ROI is set to 0 beginning at the retirement age. The program only takes in starting and ending salaries, then fills in each year linearly from start to end.

A note about inflation: The code does not account for inflation. However, tax brackets and contribution limits in reality scale with inflation. Therefore, as a simple estimate, we should inflate past salaries and deflate future salaries in order for the tax and contribution rules to work best. Wouldn't the final value be skewed to overly weigh past income if we ignore inflation? No, simply lower the expected APY. This is equivalent to depreciation.

I am not a financial expert. This program was made for fun, and I hope you enjoy! If something looks fishy, or if you like what you see, I would love to hear your thoughts.

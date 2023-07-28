import tax_calculator as tx

contribution_lim = 22500
catchup_bonus = 7500

def brackets(thousands=True):
  cutoffs = [10, 50, 100, 150, 1000]
  rates   = [ 0, .1,  .2,  .3, .4]
  if thousands:
    return {i: j for i, j in zip(cutoffs, rates)}
  else:
    return {i*1000: j for i, j in zip(cutoffs, rates)}
    #return {10e3:0, 50e3:.1, 100e3:.2, 150e3:.3}

def income_tax(income):
  cutoffs = brackets()
  for x in cutoffs:
    if income < x:
      return income * cutoffs[x]

def invest(principle):
  rate = 1.05
  return principle * rate

#----------------------------------------------------

def tax_rate(income):
  return tx.tax_rate(income)
  if income == 0:
    return 0
  rates = brackets()
  effective = 0
  prev_brack = 0
  for x in rates:
    if income > x:
      effective += rates[x] * (x - prev_brack)
      prev_brack = x
    else:
      effective += rates[x] * (income - prev_brack)
      return effective / income
  #for x in rates:
  #  if income < x:
  #    return rates[x]          # Returns None of income>highest bracket

def contribution(income, keep, roth=True):
  #roth_cont = income * (1 - tax_rate(income)) - keep
  roth_cont = keep    # Misnamed to avoid edits, keep=cont
  if roth:
    #return income * (1 - tax_rate(income)) - keep
    return min(roth_cont, contribution_lim)
  else:
    #return (income * (1 - tax_rate(income)) - keep) / (1 - tax_rate(income))
    #return roth_cont / (1 - tax_rate(income - roth_cont))
    return min(roth_cont / (1 - tax_rate(income)), contribution_lim)

#def account_bal(P, apy, years):
  #return P * apy**years
def discrepancy(income, keep):
  roth_keep = income - contribution(income, keep) - tx.tax_calc(income)
  trad_cont = contribution(income, keep, roth=False)
  trad_keep = income - trad_cont - tx.tax_calc(income-trad_cont)
  return roth_keep - trad_keep

def account_bal(salary_arr, keep_arr, years, apy=1.05, roth=True):
  # Is years necessary? Doesn't years have to be len(arr)?
  tot = 0
  for i in range(years):
    tot += contribution(salary_arr[i], keep_arr[i], roth) * apy**(years-i)
  return tot

def summation(func, start, stop):
  tot = 0
  for i in range(start, stop + 1):
    tot += func(i)


  

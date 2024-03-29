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

def contribution(income, keep, roth=True, clim=contribution_lim):
  #roth_cont = income * (1 - tax_rate(income)) - keep
  roth_cont = keep    # Misnamed to avoid edits, keep=cont
  if roth:
    #return income * (1 - tax_rate(income)) - keep
    return min(roth_cont, clim)
  else:
    #return (income * (1 - tax_rate(income)) - keep) / (1 - tax_rate(income))
    #return roth_cont / (1 - tax_rate(income - roth_cont))
    return min(roth_cont / (1 - tax_rate(income)), clim)

#def account_bal(P, apy, years):
  #return P * apy**years
def discrepancy(income, keep):
  old_method = False
  if old_method:
    roth_keep = income - contribution(income, keep) - tx.tax_calc(income)
    trad_cont = contribution(income, keep, roth=False)
    trad_keep = income - trad_cont - tx.tax_calc(income-trad_cont)
    return roth_keep - trad_keep
  rcont = keep # roth contribution
  tcont = rcont / (1-tx.tax_rate(income))
  mehcont = rcont / (1-tx.tax_rate(income-rcont))
  #mehcont = rcont * (1+tx.tax_rate(income))
  badcont = rcont * (1+tx.tax_rate(income-rcont))
  roth_keep = income - rcont - tx.tax_calc(income)
  trad_keep = income - tcont - tx.tax_calc(income-tcont) # Is -rcont of interest?
  bad_keep = income - badcont - tx.tax_calc(income-badcont)
  meh_keep = income - mehcont - tx.tax_calc(income-mehcont)
  #return trad_keep-roth_keep
  #return roth_keep, trad_keep, bad_keep, meh_keep
  return tcont / rcont, 1/(badcont-rcont)*(tcont-rcont), trad_keep / roth_keep

def account_bal(salary_arr, keep_arr, years, apy=1.05, roth=True, age=18, clim=[]):
  # Is years necessary? Doesn't years have to be len(arr)?
  #clim = contribution_lim
  if clim==[]:
    clim = [30000 for i in range(years)]  # Beyond hacky
  tot = 0
  for i in range(years):
    #if i + age == 50:   # This is not correct
    #  clim += catchup_bonus
    tot += contribution(salary_arr[i], keep_arr[i], roth, clim=clim[i]) * \
           apy**(years-i)
    # Separate if clause for roth to avoid calling function needlessly?
  return tot

def soc_sec(salaries):
  salaries = [min(x, 160200) for x in salaries] # Max soc sec contribution
  salaries.sort(reverse=True)                   # Sort high to low
  years = min(35, len(salaries))                # We want the 35 highest
  salaries = salaries[:35]
  aime = sum(salaries) / 35 / 12 # Average Indexed Monthly Earnings
  benefit = .9 * min(aime, 1115)
  if aime > 1115:
    benefit += .32 * min(aime-1115, 6721-1115)
    if aime > 6721:
      benefit += .15 * (aime-6721)
  return benefit

def summation(func, start, stop, *args):
  tot = 0
  for i in range(start, stop + 1):
    tot += func(*args, i)
  return tot

def exponentiate(base, exponent):
  return base ** exponent

  

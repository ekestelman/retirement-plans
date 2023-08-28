import tax_calculator as tx
import functions as fun
import numpy as np
import matplotlib.pyplot as plt
import json
import sys

def check_discrepancy():
  print("Salary|RCont|TCont|RKeep|TKeep|DKeep|Tax Saved|DCont")
  for i in range(20, 320, 20):
    i *= 1000
    #print(fun.discrepancy(i, (0.85-fun.tax_rate(i))*i))
    # Can we compute contribution using marginal tax rates instead of effective?
    keep = .85 * (i - tx.tax_calc(i))
    roth_cont = fun.contribution(i, keep)
    trad_cont = fun.contribution(i, keep, roth=False)
    print(i, str(round(tx.tax_rate(i)*100, 2))+"%", \
          int(roth_cont), int(trad_cont), \
          int(i - roth_cont - tx.tax_calc(i)), \
          int(i - trad_cont - tx.tax_calc(i-trad_cont)), \
          int(fun.discrepancy(i, keep)),
          int(tx.tax_calc(i) - tx.tax_calc(i-roth_cont)),
          int(trad_cont - roth_cont)
          #fun.discrepancy(i, .85*(1-fun.tax_rate(i))*i), \
          #fun.contribution(i, .85*(1-fun.tax_rate(i))) * \
          #fun.tax_rate(i-fun.contribution(i, .85*(1-fun.tax_rate(i)))),
          #fun.contribution(i, .85*(1-fun.tax_rate(i)) * (1-1))
          )

def get_vals(dic=False, loadfile=None):
  if loadfile:
    with open(loadfile) as f:
      vals = json.load(f)
      return vals
  vals = {"work years" : 40,    # Default values
          "ret years" : 30,
          "start sal" : 70*1000,
          "end sal" : 148*1000,
          "apy" : 1.05,
          "normalize" : False,
          "cont" : .1,
          "ret apy" : 1.03,
          "age" : 25,
          "ret age" : 65,
          "life" : 95,
          "bal" : 0,
          "pension" : 0,
          "match" : 0
          }
  if sys.argv[-1] == 'd':
    #return [vals[x] for x in vals] # Not here because still want to save hist
    pass    # Pointless if: pass? Not pointless if 'd' because else clause
  # ERROR IF NO ARGS
  elif len(sys.argv)!=1 and sys.argv[1] == 'use':     # Instead of "use" simply try?
    with open(sys.argv[2]) as f:
      vals = json.load(f)
  else:   # else not necessary after previous return, YES necessary if 'd'
    try:
      with open("history.txt") as f:  # history is overwriting defaults here
        vals = json.load(f)
    except FileNotFoundError:
      pass
  if sys.argv[-1] == 'p':
    #return [vals[x] for x in vals] # No need to re-save hist
    pass
  elif len(sys.argv)==1:
                                            # Check if thousands=True in fun
    print("Yearly salary will be computed as increasing linearly from \n" \
          "starting salary to ending salary over the course of number \n" \
          "of years working.")
    #vals["work years"] = int(input("Years working: ") or vals["work years"])
    #vals["ret years"] = int(input("Years in retirement: ") or vals["ret years"])
    vals["start sal"] = int(input("Starting salary (thousands of dollars): ") or \
                        vals["start sal"]*.001)*1000
    vals["end sal"] = int(input("Ending salary (thousands of dollars): ") or \
                      vals["end sal"]*.001)*1000
    vals["cont"] = int(input("% of gross income to be invested: ") or \
                   vals["cont"]*100) * .01
    vals["apy"] = float(input("APY on investments (%): ") or \
                  (vals["apy"]-1)*100) * .01 + 1
    vals["ret apy"] = float(input("APY during retirement (%): ") or \
                  (vals["ret apy"]-1)*100) * .01 + 1
    # "or" goes inside float() because if input=0 then (float('0') or x)=x but
    # float('0' or x)=0 as desired.
    #normalize = bool(input("Normalize curves? 1=Yes, 0=No: ") or \
    #            vals["normalize"])   # Doesn't work as intended
    vals["age"] = int(input("Current age: ") or vals["age"])
    vals["ret age"] = int(input("Retirement age: ") or vals["ret age"])
    if vals["ret age"] < 59:
      print("WARNING: retirement distributions may be subject to a penalty." + \
            " Results may be less accurate.")
    vals["life"] = int(input("Life expectancy (90 is recommended): ") or \
                       vals["life"])
    vals["bal"] = int(input("Current pre-tax balance (thousands of dollars): ") \
                      or vals["bal"]*.001)*1000
    vals["pension"] = int(input("Pension (thousands of dollars): ") or \
                      vals["pension"]*.001)*1000
    vals["match"] = float(input("Employer match (%): ") or \
                    vals["match"]*100) * .01
    vals["normalize"] = input("Normalize curves? (y/n): ") or \
                        vals["normalize"]
    vals["work years"] = vals["ret age"] - vals["age"]
    vals["ret years"] = vals["life"] - vals["ret age"]
    if vals["normalize"] == 'y':
      vals["normalize"] = True
    elif vals["normalize"] == 'n':
      vals["normalize"] = False
  with open("history.txt", 'w') as f:    # Not necessary if argv[-1]=='p'
    json.dump(vals, f, indent=2)
  #return work_years, ret_years, start_sal, end_sal, apy, normalize
  if dic:
    return vals
  return [vals[x] for x in vals]

def ret_plan(vals, rothorder):  # roth takes value 1 or 2 to indicate 1st or 2nd
  # TODO give rothorder default value?
  if not vals.get("normalize"):   # Allow widget.py to not show normalize
    vals["normalize"] = False     # These hacks aren't necessary with new method
  rothorder = vals.get("rothorder", rothorder) # Allow iplot.py to show rothorder
  # rothorder arg pointless?
  vals['work years'] = vals['ret age'] - vals['age']  # Assign calculated vars
  vals["ret years"] = vals["life"] - vals["ret age"]
  salaries = np.linspace(vals["start sal"], vals["end sal"], vals["work years"])
                # Better to do this in get_vals()?
  clim = fun.contribution_lim
  clim = [fun.contribution_lim for i in range(vals['age'], 50)]
  clim += [fun.contribution_lim + fun.catchup_bonus for i in \
           range(50, vals['ret age'])]
  # TODO clim also being used in fun.contribution?
  # TODO may be easier to get the right match if cont list is established for
  # each plan (i.e., a cont list for switching from roth to trad at 0, at 1, 
  # etc.)
  cont = [min(vals["cont"] * x, y) for x,y in zip(salaries, clim)]
  # Allow user to set clim? Maybe all the policies should be in a config file.
  # Config file can include tax brackets, limits, default args...
  excess = [max(x * (1 + tx.tax_rate(y)) - z, 0) for x,y,z in \
            zip(cont, salaries, clim)]
            # Really only have to compute this for trad yrs
            # Should this be a bit higher? This works if cont=clim. What about
            # cont<clim<cont+excess? or < cont(1-taxrate)? Maybe this is close
            # enough as a floor.
  vals["match"] = vals.get("match", 0)
  match = [min(vals.get("match", 0) * s, c) for s,c in zip(salaries, cont)]
  # TODO: potential for greater match if you contribute (more) to trad rather
  # than roth.
  ret_tot = []
  acct = [None, None, None]
  all_accts = {"roth" : [], "trad" : [], "priv" : [], "pension" : []}
  withdraw = {"trad" : [], "priv" : []}
  def plan_calc(i):
    acct[1] = fun.account_bal(salaries[:i], cont[:i], i, \
                              vals["apy"], rothorder==1, age=vals["age"], \
                              clim=clim[:i])
                              #first=="roth")
                              # roth==1 true for roth, false for trad first
    acct[2] = fun.account_bal(salaries[i:], cont[i:], vals["work years"]-i, \
                              vals["apy"], rothorder==2, age=vals["age"], \
                              clim=clim[i:])
                              #first=="trad")
                              # roth==2 false for trad, true for roth second
    acct[1] *= vals["apy"]**(vals["work years"]-i)
                              # Continued growth from first account
    if rothorder==1:
      roth = acct[1]      # Consider better var names
      trad = acct[2]
      # acct[0] is private brokerage acct
      acct[0] = fun.account_bal(salaries[i:], excess[i:], vals["work years"]-i, \
                                vals["apy"], roth=True)
      acct[0] -= (acct[0] - sum(excess[i:])) * .15
      # Assumes no growth on priv in retirement
      #acct[2] *= 1 - fun.tax_rate(acct[2] / vals["ret years"])
      #match[i:] = [min(vals["match"] * s, m / (1-tx.tax_rate(s))) for m,s in \
      #             zip(match[i:], salaries[i:])]
      # use a tstart and tstop variable to cut out some lines?
    else:
      trad = acct[1]
      roth = acct[2]
      acct[0] = fun.account_bal(salaries[:i], excess[:i], i, \
                                vals["apy"], roth=True)
      acct[0] *= vals["apy"]**(vals["work years"]-i)
      acct[0] -= (acct[0] - sum(excess[:i])) * .15
      #acct[1] *= 1 - fun.tax_rate(acct[1] / vals["ret years"])
      #match[:i] = [min(vals["match"] * s, m / (1-tx.tax_rate(s))) for m,s in \
      #             zip(match[:i], salaries[:i])]
      # FIXME does 172 and 183 correct for greater match with trad? But fails
      # sanity check in edge cases where cont < match. Commenting out resolves
      # sanity check and non-edge cases are unaffected.
      # Hypothesis: if match < cont, 172 and 183 do nothing. If cont < match,
      # 172 and 183 will produce higher value in first min arg, so second min
      # arg may be returned (or higher first arg). Doesn't explain sanity fail
      # though? Only explains why non-edge cases are unaffected.
      # I think sanity check fails due to off by 1 error.
    #match = [min(vals.get("match", 0) * s, c) for s,c in zip(salaries, cont)]
    # Add employer match to trad
    trad += fun.account_bal(salaries[:], match[:], vals['work years'], \
                            vals['apy'], roth=False, age=vals['age'])
    trad += vals['bal'] * vals['apy'] ** vals['work years']
    ret_growth_factor = vals["ret apy"] ** vals["ret years"] / \
                        fun.summation(fun.exponentiate, 0, \
                        vals["ret years"]-1, vals["ret apy"])
                        # Growth factor already determines yearly distribution
                        # TODO clarify what growth_factor is/does
    #ret_growth_factor = 1
    #if i == 11:
    #  print(roth, trad, acct[0])
    roth *= ret_growth_factor
    trad *= ret_growth_factor
    #acct[0] *= ret_growth_factor  # Questionable because selling and reinvesting
                                  # would incur tax
    #if i == 11:
    #  print(roth, trad, acct[0])
    old_method = False
    #if ret_growth_factor == 1:   # Bug when ret apy = 1
    if old_method:
      trad *= 1 - fun.tax_rate(trad / vals["ret years"])
      #acct[0] -= (acct[0] - sum(excess)) * .15
    else:
      withdraw["trad"].append(trad)   # For withdrawal instructions
      #trad += vals.get("pension", 0)  # Assume pension is fully taxable (not
                                      # accurate for soc sec). Should not be
                                      # subject to FICA either.
                                      # Not compatible with old method.
                                      # Use .get for other optional args?
      pension = vals.get("pension", 0)
      taxable = trad + pension
      # FIXME true pension is probably fully taxable but not soc sec (only up
      # to 85%). Not subject to FICA, but should have been paid earlier.
      # Separate out other pension from soc sec? Other solution: only input
      # taxable pension (other pension + 85% of soc sec).
      trad *= 1 - fun.tax_rate(taxable)
      pension *= 1 - fun.tax_rate(taxable)
      #acct[0] *= .9   # VERY rough approx for now
      # Challenge to calculate because profit keeps going up over time
    # Assume no growth on priv in retirement?
    acct[0] /= vals["ret years"]
    #if ret_growth_factor != 1:      # This didn't make a difference?
    #  acct[0] /= vals["ret years"]
      # If priv isn't treated with growth factor, it must be divided
    #if i == 11:
    #  print(roth, trad, acct[0])
    #ret_tot.append(sum(acct))
    ret_tot.append(roth + trad + acct[0] + pension)
    #all_accts.append({"roth" : roth, "trad" : trad, "priv" : acct[0]})
    all_accts["roth"].append(roth)
    all_accts["trad"].append(trad)
    all_accts["priv"].append(acct[0])
    all_accts["pension"].append(pension)
  #print_results(ret_tot, vals["ret years"], vals["normalize"])
  for i in range(0, vals["work years"]+1):
    plan_calc(i)
  old_method=False
  if vals["normalize"]:
    return [x / max(ret_tot) for x in ret_tot]
    # ret_tot may be obsolete once we account for growth in retirement, since
    # growth affects yearly ret which affects tax rate which affects ret_tot.
    # It doesn't make so much sense to think of "total" funds after tax if tax
    # is paid based on yearly, not total, funds.
  #if ret_growth_factor != 1:
  if not old_method:
    #return all_accts
    return ret_tot, all_accts, withdraw
  yearly_ret = [x / vals["ret years"] for x in ret_tot]
  return yearly_ret

def print_results(ret_tot, ret_years, normalize):
  print(ret_tot.index(max(ret_tot)), ret_tot.index(min(ret_tot)))
  #print(max(ret_tot), min(ret_tot))
  print(max(ret_tot)/ret_years, min(ret_tot)/ret_years)
  #print(ret_tot[0], ret_tot[-1])  # Sanity check

def plot_plan(plans):
  color_num = 0
  for y in plans:
    plt.plot(np.arange(0, len(y), 1), y, label = "")
    color = 'C' + str(color_num)
    plt.hlines(max(y)*.99, 0, len(y), color, ls='--')
    color_num += 1
    plt.xlabel("Year at which we switch type")
    plt.ylabel("Yearly income in retirement")
    plt.title("Contribute to Roth or Trad for x years, then switch")
  plt.show()

def plot_tax_rates(*points, ax, lbound=0, ubound=200):
  salaries = np.linspace(min(lbound,min(points)/1000), \
                         max(ubound,max(points)/1000),1000)
  rates = [tx.tax_rate(x*1000) for x in salaries]
  ax.plot(salaries, rates)
  #salaries = np.linspace(20, 800, 1000)
  salaries = np.linspace(lbound, ubound, 1000)   # Set bounds based on income?
  rates = [tx.tax_rate(x*1000) for x in salaries]
  #plt.plot(salaries, rates)
  ax.plot(salaries, rates)
  for p in points:
    #plt.plot(p/1000, tx.tax_rate(p), 'o')
    ax.plot(p/1000, tx.tax_rate(p), 'o')
    # This amount is actually after tax! This graph doesn't show what I want.
  #plt.show()
  return ax

def plot_pies(*strats, ubound=200, lbound=0, rates=True):   # Choice in * rather than list?
  fig, axs = plt.subplots(1, 3)
  # best_yr bad variable
  # TODO messy plot with 0% categories, get rid of these
  for i in range(len(strats)):
    axs[i].pie(strats[i].values(), labels=["Roth", "Trad", "Private", "Pension"], \
               autopct='%1.1f%%')
  #axs[0].pie([rcomp["roth"][best_yrs[0]], \
  #         rcomp["trad"][best_yrs[0]], \
  #         rcomp["priv"][best_yrs[0]]], \
  #         labels=["Roth", "Trad", "Private"], autopct='%1.1f%%')
  axs[0].set_title("Roth first")
  #axs[1].pie([tcomp["roth"][best_yrs[1]], \
  #         tcomp["trad"][best_yrs[1]], \
  #         tcomp["priv"][best_yrs[1]]], \
  #         labels=["Roth", "Trad", "Private"], autopct='%1.1f%%')
  axs[1].set_title("Trad first")
  if rates:
    plot_tax_rates(strats[0]["trad"], strats[1]["trad"], ax=axs[2], \
                   ubound=ubound, lbound=lbound)
                 # FIXME wrong tax rate based on post-tax trad (and no pension)
  plt.show()
  #plot_tax_rates(rcomp["trad"][best_yrs[0]], tcomp["trad"][best_yrs[1]])
  #plot_tax_rates(strats[0]["trad"], strats[1]["trad"])
              # best_yrs global var?
              # maybe better choice in args, don't need whole rcomp dic + lists

#def get_results(ret_tot, all_accts, withdraw):
def summary(plans):
  # Want plan func to call results/summary func
  # Plans is a list of 2 retirement plans to be compared.
  tots = [x[0] for x in plans]   # Total yearly retirement funds
  rfirst, tfirst = tots
  rcomp, tcomp = [x[1] for x in plans]  # Components of tots (trad/roth/priv/pens)
  rwithdraw, twithdraw = [x[2] for x in plans]  # Trad withdrawal
  best_yrs = []
  for x in tots:
    best = max(x)
    best_yr = x.index(best)
    best_yrs.append(best_yr)
    worst = min(x)
    print("Best:" + str(best_yr).rjust(3) + str(int(best)).rjust(9) + "  ", \
          "Worst:" + str(int(worst)).rjust(9) + "  ", \
          "Diff:" + str(int(best-worst)).rjust(9))
  print("Optimal diff:", int(max(tots[0])-max(tots[1])))
  print("Yearly trad withdrawal (pretax):", \
        int(rwithdraw["trad"][best_yrs[0]]), "or", \
        int(twithdraw["trad"][best_yrs[1]]))
  if not (rfirst[0]==tfirst[-1] and rfirst[-1]==tfirst[0]): # Sanity check
    print("Something's wrong! Please contact the author :)")
  rbest = {"roth" : rcomp["roth"][best_yrs[0]],
           "trad" : rcomp["trad"][best_yrs[0]],
           "priv" : rcomp["priv"][best_yrs[0]],
           "pension" : rcomp["pension"][best_yrs[0]]}
  tbest = {"roth" : tcomp["roth"][best_yrs[1]],
           "trad" : tcomp["trad"][best_yrs[1]],
           "priv" : tcomp["priv"][best_yrs[1]],
           "pension" : tcomp["pension"][best_yrs[1]]}
           # Better way than copy paste...
  return rbest, tbest

def compare_comp():
  tax = np.linspace(0, 50, 1000)

def main(args):
  plans = [ret_plan(args, 1), ret_plan(args, 2)]
  pie_data = summary(plans)
  tots = [x[0] for x in plans]
  plot_plan(tots)
  plot_pies(*pie_data, lbound=args["start sal"]/1000, \
            ubound=args["end sal"]/1000)

if __name__=="__main__":
  args = get_vals(True)
  main(args)
  #plt.stackplot(np.arange(0, len(rfirst), 1), rcomp.values())
  #plt.show()
  #plt.stackplot(np.arange(0, len(tfirst), 1), tcomp.values())
  #plt.show()
  #check_discrepancy()
  #plot_tax_rates()

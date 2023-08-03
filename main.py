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

def trial_2():
  contribution = 6e3
  salaries = [(70e3, 40)]
  retirement = 0

  for x in salaries:
    for i in range(x[1]):
      retirement = functions.invest(retirement) + contribution
  
  print(retirement)

def get_vals(dic=False):
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
          "bal" : 0
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
      with open("history.txt") as f:
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

def trial_3(work_years, ret_years, start_sal, end_sal, apy, normalize=False, \
            cont=.1):
  #print("Years", "Roth/Yr", "Trad/Yr", "Tot/Yr", "Tax")
  salaries = np.linspace(start_sal, end_sal, work_years)
  #keeps = [(0.85-fun.tax_rate(x))*x for x in salaries] # Check math
  clim = fun.contribution_lim
  keeps = [min(cont * x, clim) for x in salaries]
  excess = [max(x * (1 + tx.tax_rate(y)) - clim, 0) for x,y in \
            zip(keeps, salaries)]  # Can this be more efficient?
                                   # Necessary if roth<clim<trad?
  ret_tot = []
  
  for i in range(0, work_years+1):
    roth = fun.account_bal(salaries[:i], keeps[:i], i, apy=apy)
    roth *= apy**(work_years-i)    # -1?
    priv = fun.account_bal(salaries[i:], excess[i:], work_years-i, apy=apy, \
           roth=True)
    priv -= (priv - sum(excess)) * .15    # Assume 15% capital gains tax
    trad = fun.account_bal(salaries[i:], keeps[i:], work_years-i, apy=apy, \
           roth=False)
    #temp_trad = trad
    #trad -= trad * fun.tax_rate(trad / ret_years) #* ret_years math mistake
    trad *= 1 - fun.tax_rate(trad / ret_years) #* ret_years math mistake
    ret_tot.append(roth+trad+priv)

  print_results(ret_tot, ret_years, normalize)  # Check ret_tot[0] and ret_tot[-1]

  if normalize:
    return [x / max(ret_tot) for x in ret_tot]
  yearly_ret = [x / ret_years for x in ret_tot]
  return yearly_ret

def trial_4(work_years, ret_years, start_sal, end_sal, apy, normalize=False, \
            cont=.1):  # Can set default args here instead of get_vals()
  # Check if thousands=True in fun
  salaries = np.linspace(start_sal, end_sal, work_years)
  #keeps = [(0.85-fun.tax_rate(x))*x for x in salaries]
  #keeps = [cont * x for x in salaries]
  clim = fun.contribution_lim
  keeps = [min(cont * x, clim) for x in salaries]
  excess = [max(x * (1 + tx.tax_rate(y)) - clim, 0) for x,y in \
            zip(keeps, salaries)]
  ret_tot = []
  
  for i in range(0, work_years+1):
    roth = fun.account_bal(salaries[i:], keeps[i:], work_years-i, apy=apy)
    #roth += roth * apy**(work_years-i)
    priv = fun.account_bal(salaries[:i], excess[:i], i, apy=apy, roth=True)
    trad = fun.account_bal(salaries[:i], keeps[:i], i, apy=apy, roth=False)
    priv *= apy**(work_years-i)  # -1 ?
    priv -= (priv - sum(excess)) * .15    # Assume 15% capital gains tax
    trad *= apy**(work_years-i)  # -1 ?
    #temp_trad = trad
    #trad -= trad * fun.tax_rate(trad / ret_years) #* ret_years math mistake
    trad *= 1 - fun.tax_rate(trad / ret_years) #* ret_years math mistake
    ret_tot.append(roth+trad+priv)

  print_results(ret_tot, ret_years, normalize)

  if normalize:
    return [x / max(ret_tot) for x in ret_tot]
  yearly_ret = [x / ret_years for x in ret_tot]
  return yearly_ret

def ret_plan(vals, rothorder):  # roth takes value 1 or 2 to indicate 1st or 2nd
  salaries = np.linspace(vals["start sal"], vals["end sal"], vals["work years"])
                # Better to do this in get_vals()?
  clim = fun.contribution_lim
  clim = [fun.contribution_lim for i in range(vals['age'], 50)]
  clim += [fun.contribution_lim + fun.catchup_bonus for i in \
           range(50, vals['ret age'])]
  cont = [min(vals["cont"] * x, y) for x,y in zip(salaries, clim)] # Need to fix clim issue
  excess = [max(x * (1 + tx.tax_rate(y)) - z, 0) for x,y,z in \
            zip(cont, salaries, clim)]  # Really only have to compute this for trad yrs
  ret_tot = []
  acct = [None, None, None]
  all_accts = {"roth" : [], "trad" : [], "priv" : []}
  withdraw = {"trad" : [], "priv" : []}
  for i in range(0, vals["work years"]+1):
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
    #distr1 = acct[1] * vals["ret apy"] ** vals["ret years"] / \
    #         fun.summation(fun.exponentiate, 0, vals["ret years"]-1, \
    #                       vals["ret apy"])
    #distr2 = acct[2] * vals["ret apy"] ** vals["ret years"] / \
    #         fun.summation(fun.exponentiate, 0, vals["ret years"]-1, \
    #                       vals["ret apy"])
    #distr0 = acct[0] * vals["ret apy"] ** vals["ret years"] / \
    #         fun.summation(fun.exponentiate, 0, vals["ret years"]-1, \
    #                       vals["ret apy"])
    # Better to rename accts with roth/trad naming?
    if rothorder==1:
      roth = acct[1]      # Consider better var names
      trad = acct[2]
      # acct[0] is private brokerage acct
      acct[0] = fun.account_bal(salaries[i:], excess[i:], vals["work years"]-i, \
                                vals["apy"], roth=True)
      acct[0] -= (acct[0] - sum(excess[i:])) * .15
      # Assumes no growth on priv in retirement
      #acct[2] *= 1 - fun.tax_rate(acct[2] / vals["ret years"])
    else:
      trad = acct[1]
      roth = acct[2]
      acct[0] = fun.account_bal(salaries[:i], excess[:i], i, \
                                vals["apy"], roth=True)
      acct[0] *= vals["apy"]**(vals["work years"]-i)
      acct[0] -= (acct[0] - sum(excess[:i])) * .15
      #acct[1] *= 1 - fun.tax_rate(acct[1] / vals["ret years"])
    trad += vals['bal'] * vals['apy'] ** vals['work years']
    ret_growth_factor = vals["ret apy"] ** vals["ret years"] / \
                        fun.summation(fun.exponentiate, 0, \
                        vals["ret years"]-1, vals["ret apy"])
                        # Growth factor already determines yearly distribution
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
      trad *= 1 - fun.tax_rate(trad)
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
    ret_tot.append(roth + trad + acct[0])
    #all_accts.append({"roth" : roth, "trad" : trad, "priv" : acct[0]})
    all_accts["roth"].append(roth)
    all_accts["trad"].append(trad)
    all_accts["priv"].append(acct[0])
  #print_results(ret_tot, vals["ret years"], vals["normalize"])
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

def plot_pies(*strats, ubound=200, lbound=0):   # Choice in * rather than list?
  fig, axs = plt.subplots(1, 3)
  # best_yr bad variable
  for i in range(len(strats)):
    axs[i].pie(strats[i].values(), labels=["Roth", "Trad", "Private"], \
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
  plot_tax_rates(strats[0]["trad"], strats[1]["trad"], ax=axs[2], \
                 ubound=ubound, lbound=lbound)
  plt.show()
  #plot_tax_rates(rcomp["trad"][best_yrs[0]], tcomp["trad"][best_yrs[1]])
  #plot_tax_rates(strats[0]["trad"], strats[1]["trad"])
              # best_yrs global var?
              # maybe better choice in args, don't need whole rcomp dic + lists

def compare_comp():
  tax = np.linspace(0, 50, 1000)

if __name__=="__main__":
      
  #normalize = False
  plans = []
  if 1:
    args = get_vals(True)
    #plans = [ret_plan(args, 1)[0], ret_plan(args, 2)[0]]
    rfirst, rcomp, rwithdraw = ret_plan(args, 1)
    tfirst, tcomp, twithdraw = ret_plan(args, 2)
    #rcomp = rfirst[1]  # Roth first components
    #tcomp = tfirst[1]  # Trad first components
    #rfirst = rfirst[0]
    #tfirst = tfirst[0]
    #rtots = [sum(x.values()) for x in rfirst]
    #ttots = [sum(x.values()) for x in tfirst]
    #rtots = [sum(x[i]) for x in rfirst for i in range(len(x))]
    #ttots = [sum(x[i]) for x in tfirst for i in range(len(x))]
    #plans = [rfirst[0], tfirst[0]]
    #plans.append(rfirst)
    #plans.append(tfirst)
    plans.append(rfirst)
    plans.append(tfirst)
    best_yrs = []
    for x in plans:
      best = max(x)
      best_yr = x.index(best)
      best_yrs.append(best_yr)
      worst = min(x)
      print("Best:" + str(best_yr).rjust(3) + str(int(best)).rjust(9) + "  ", \
            "Worst:" + str(int(worst)).rjust(9) + "  ", \
            "Diff:" + str(int(best-worst)).rjust(9))
    print("Optimal diff:", int(max(plans[0])-max(plans[1])))
    print("Yearly trad withdrawal (pretax):", \
          int(rwithdraw["trad"][best_yrs[0]]), "or", \
          int(twithdraw["trad"][best_yrs[1]]))
    if not (rfirst[0]==tfirst[-1] and rfirst[-1]==tfirst[0]): # Sanity check
      print("Something's wrong! Please contact the author :)")
  if 0:
    args = get_vals()
    #plans = [trial_3(*args), trial_4(*args)]#, trial_3(*args[:4], 1.07)]
    plans.append(trial_3(*args))
    plans.append(trial_4(*args))
  if 0:
    plans = [trial_3(*args), trial_4(*args), trial_3(*args[:4], 1.07, args[5]), \
             trial_4(*args[:4], 1.07, args[5]), \
             trial_3(*args[:4], 1.1, args[5]), trial_4(*args[:4], 1.1, args[5])]
  plot_plan(plans)
  rbest = {"roth" : rcomp["roth"][best_yrs[0]],
           "trad" : rcomp["trad"][best_yrs[0]],
           "priv" : rcomp["priv"][best_yrs[0]]}
  tbest = {"roth" : tcomp["roth"][best_yrs[1]],
           "trad" : tcomp["trad"][best_yrs[1]],
           "priv" : tcomp["priv"][best_yrs[1]]}
           # Better way than copy paste...
  plot_pies(rbest, tbest, lbound=args["start sal"]/1000, \
            ubound=args["end sal"]/1000)
                # 0 is best roth yr, 1 is best trad yr
  #plt.stackplot(np.arange(0, len(rfirst), 1), rcomp.values())
  #plt.show()
  #plt.stackplot(np.arange(0, len(tfirst), 1), tcomp.values())
  #plt.show()
  #trial_3(*args)
  #trial_4(*args)
  #check_discrepancy()
  #plot_tax_rates()

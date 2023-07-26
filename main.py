import functions as fun
import numpy as np
import matplotlib.pyplot as plt
import tax_calculator as tx
import json
import sys

# Consider change if accounts are maxed out
# Allow for fixing one value and determining others (e.g., fix
# retirement balance and determine contributions.
# Consider making a table or 3d plot to compare multiple variables
# at a time, such as different APYs. Can also plot multiple graphs
# for some sampling of APYs.
# Show multiple axes for different salaries, multiple graphs on each
# for diff APYs.

#contribution_lim = 22500
#catchup_bonus = 7500      # Switch from asking time working to ages working, then
#                          # determine limit

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

def get_vals():
  if sys.argv[-1] == 'd':
    work_years = 40
    ret_years = 20
    start_sal = 70*1000
    end_sal = 148*1000
    apy = 5 / 100 + 1
    normalize = False
  else:
    try:
      with open("history.txt") as f: # Error if program has not been run before?
        vals = json.load(f)
    except FileNotFoundError:
      vals = {"work years" : 40,
              "ret years" : 20,
              "start sal" : 70*1000,
              "end sal" : 148*1000,
              "apy" : 5 / 100 + 1,
              "normalize" : False
              }
  if sys.argv[-1] == 'p':
    work_years = vals["work years"]
    ret_years = vals["ret years"]
    start_sal = vals["start sal"]
    end_sal = vals["end sal"]
    apy = vals["apy"]
    normalize = vals["normalize"]
  elif len(sys.argv)==1:
                                            # Check if thousands=True in fun
    print("Yearly salary will be computed as increasing linearly from \n" \
          "starting salary to ending salary over the course of number \n" \
          "of years working.")
    work_years = int(input("Years working: ") or vals["work years"])
    ret_years = int(input("Years in retirement: ") or vals["ret years"])
    start_sal = int(input("Starting salary (thousands of dollars): ") or \
                vals["start sal"]/1000)*1000
    end_sal = int(input("Ending salary (thousands of dollars): ") or \
              vals["end sal"]/1000)*1000
    apy = float(input("APY on investments (%): ") or \
          (vals["apy"]-1)*100) / 100 + 1
    #normalize = bool(input("Normalize curves? 1=Yes, 0=No: ") or \
    #            vals["normalize"])   # Doesn't work as intended
    normalize = input("Normalize curves? (y/n): ") or \
                vals["normalize"]
    if normalize == 'y':
      normalize = True
    elif normalize == 'n':
      normalize = False
  vals = {"work years" : work_years,
          "ret years" : ret_years,
          "start sal" : start_sal,
          "end sal" : end_sal,
          "apy" : apy,
          "normalize" : normalize
          }
  with open("history.txt", 'w') as f:    # Not necessary if argv[-1]=='p'
    json.dump(vals, f)
  return work_years, ret_years, start_sal, end_sal, apy, normalize

def trial_3(work_years, ret_years, start_sal, end_sal, apy, normalize=False):
  #print("Years", "Roth/Yr", "Trad/Yr", "Tot/Yr", "Tax")
  salaries = np.linspace(start_sal, end_sal, work_years)
  keeps = [(0.85-fun.tax_rate(x))*x for x in salaries] # Check math
  ret_tot = []
  #normalize = False       # Normalize resutls to compare different APYs
  
  for i in range(0, work_years+1):
    roth = fun.account_bal(salaries[:i], keeps[:i], i, apy=apy)
    roth *= apy**(work_years-i)    # -1?
    trad = fun.account_bal(salaries[i:], keeps[i:], work_years-i, apy=apy, \
           roth=False)
    #temp_trad = trad
    #trad -= trad * fun.tax_rate(trad / ret_years) #* ret_years math mistake
    trad *= 1 - fun.tax_rate(trad / ret_years) #* ret_years math mistake

    ret_tot.append(roth+trad)
    #print(repr(i).rjust(3), repr(round(roth/ret_years, 1)).rjust(6), \
    #      repr(round(trad/ret_years, 1)).rjust(6), \
    #      repr(round((roth+trad)/ret_years, 1)).rjust(6), \
    #      repr(round(fun.tax_rate(trad/ret_years), 3)).rjust(5) \
    #      )

  #for i in range(work_years):
  #  print(repr(i).rjust(3), repr(round(salaries[i], 1)).rjust(6), \
  #        repr(round(keeps[i], 1)).rjust(6), \
  #        repr(round(fun.contribution(salaries[i], keeps[i]), 1)).rjust(6), \
  #        repr(round(fun.contribution(salaries[i], keeps[i], roth=False), \
  #        1)).rjust(6) \
  #        )
  yearly_ret = [x / ret_years for x in ret_tot]
  print(ret_tot.index(max(ret_tot)), ret_tot.index(min(ret_tot)))
  print(max(ret_tot), min(ret_tot))
  print(max(ret_tot)/ret_years, min(ret_tot)/ret_years)
  if normalize:
    return [x / max(ret_tot) for x in ret_tot]
  return yearly_ret
  #plt.plot(np.arange(0,work_years+1,1), ret_tot)
  plt.plot(np.arange(0,work_years+1,1), yearly_ret)
  plt.title("Roth for x Years Followed by Trad")
  plt.xlabel("Years into Roth")
  plt.show()
  # Check for discrepancies between kept amounts.

def trial_4(work_years, ret_years, start_sal, end_sal, apy, normalize=False):
  
  # Check if thousands=True in fun
  salaries = np.linspace(start_sal, end_sal, work_years)
  keeps = [(0.85-fun.tax_rate(x))*x for x in salaries]
  ret_tot = []
  
  for i in range(0, work_years+1):
    roth = fun.account_bal(salaries[i:], keeps[i:], work_years-i, apy=apy)
    #roth += roth * apy**(work_years-i)
    trad = fun.account_bal(salaries[:i], keeps[:i], i, apy=apy, roth=False)
    trad *= apy**(work_years-i)  # -1 ?
    #temp_trad = trad
    #trad -= trad * fun.tax_rate(trad / ret_years) #* ret_years math mistake
    trad *= 1 - fun.tax_rate(trad / ret_years) #* ret_years math mistake
    ret_tot.append(roth+trad)

    #print(repr(i).rjust(3), repr(round(roth/ret_years, 1)).rjust(6), \
    #      repr(round(trad/ret_years, 1)).rjust(6), \
    #      repr(round((roth+trad)/ret_years, 1)).rjust(6), \
    #      repr(round(fun.tax_rate(trad/ret_years), 3)).rjust(5))
     
  print(ret_tot.index(max(ret_tot)), ret_tot.index(min(ret_tot)))
  print(max(ret_tot), min(ret_tot))
  print(max(ret_tot)/ret_years, min(ret_tot)/ret_years)
  yearly_ret = [x/ret_years for x in ret_tot]
  if normalize:
    return [x / max(ret_tot) for x in ret_tot]
  return yearly_ret
  plt.plot(np.arange(0,work_years+1,1), yearly_ret)
  #plt.plot(np.arange(0,work_years+1,1), ret_tot)
  plt.title("Trad for x Years Followed by Roth")
  plt.xlabel("Years into Trad")
  plt.show()
  #trial_4()

def plot_plan(plans):
  for y in plans:
    plt.plot(np.arange(0, len(y), 1), y, label = "")
    plt.xlabel("Year at which we switch type")
    plt.ylabel("Yearly income in retirement")
    plt.title("Contribute to Roth or Trad for x years, then switch")
  plt.show()

def plot_tax_rates():
  salaries = np.linspace(20, 800, 1000)
  rates = [tx.tax_rate(x*1000) for x in salaries]
  plt.plot(salaries, rates)
  plt.show()

def compare_comp():
  tax = np.linspace(0, 50, 1000)

if __name__=="__main__":
      
  #normalize = False
  args = get_vals()
  plans = [trial_3(*args), trial_4(*args)]#, trial_3(*args[:4], 1.07)]
  if 0:
    plans = [trial_3(*args), trial_4(*args), trial_3(*args[:4], 1.07, args[5]), \
             trial_4(*args[:4], 1.07, args[5]), \
             trial_3(*args[:4], 1.1, args[5]), trial_4(*args[:4], 1.1, args[5])]
  plot_plan(plans)
  #trial_3(*args)
  #trial_4(*args)
  #check_discrepancy()
  #plot_tax_rates()

import functions as fun
import numpy as np
import matplotlib.pyplot as plt

def trial_1():
  salary = 70e3
  tax = functions.income_tax(salary)
  print(salary, "\n", tax, "\n", salary - tax, "\n")

def trial_2():
  contribution = 6e3
  salaries = [(70e3, 40)]
  retirement = 0

  for x in salaries:
    for i in range(x[1]):
      retirement = functions.invest(retirement) + contribution
  
  print(retirement)

def trial_3():
  
  work_years = 40                     # Check if thousands=True in fun
  ret_years = 20
  salaries = [70 + 2*i for i in range(work_years)]
  #salaries = [70 for i in range(work_years)]
  keeps = [(0.85-fun.tax_rate(x))*x for x in salaries]
  apy = 1.05

  #print("Years", "Roth/Yr", "Trad/Yr", "Tot/Yr", "Tax")
  ret_tot = []
  
  for i in range(0, work_years+1):
    roth = fun.account_bal(salaries[:i], keeps[:i], i)
    roth *= apy**(work_years-i)    # -1?
    trad = fun.account_bal(salaries[i:], keeps[i:], work_years-i, \
           roth=False)
    temp_trad = trad
    #trad -= trad * fun.tax_rate(trad / ret_years) #* ret_years math mistake
    trad *= 1 - fun.tax_rate(trad / ret_years) #* ret_years math mistake

    ret_tot.append(roth+trad)
    print(repr(i).rjust(3), repr(round(roth/ret_years, 1)).rjust(6), \
          repr(round(trad/ret_years, 1)).rjust(6), \
          repr(round((roth+trad)/ret_years, 1)).rjust(6), \
          repr(round(fun.tax_rate(trad/ret_years), 3)).rjust(5) \
          )

  #for i in range(work_years):
  #  print(repr(i).rjust(3), repr(round(salaries[i], 1)).rjust(6), \
  #        repr(round(keeps[i], 1)).rjust(6), \
  #        repr(round(fun.contribution(salaries[i], keeps[i]), 1)).rjust(6), \
  #        repr(round(fun.contribution(salaries[i], keeps[i], roth=False), \
  #        1)).rjust(6) \
  #        )

  print(ret_tot.index(max(ret_tot)), ret_tot.index(min(ret_tot)))
  print(max(ret_tot), min(ret_tot))
  print(max(ret_tot)/ret_years, min(ret_tot)/ret_years)
  plt.plot(np.arange(0,41,1), ret_tot)
  plt.title("Roth for x Years Followed by Trad")
  plt.xlabel("Years into Roth")
  plt.show()

def trial_4():
  
  work_years = 40                     # Check if thousands=True in fun
  ret_years = 20
  salaries = [70 + 2*i for i in range(work_years)]
  #salaries = [70 for i in range(work_years)]
  keeps = [(0.85-fun.tax_rate(x))*x for x in salaries]
  apy = 1.05
  ret_tot = []
  
  for i in range(0, work_years+1):
    roth = fun.account_bal(salaries[i:], keeps[i:], work_years-i)
    #roth += roth * apy**(work_years-i)
    trad = fun.account_bal(salaries[:i], keeps[:i], i, \
           roth=False)
    trad *= apy**(work_years-i)  # -1 ?
    temp_trad = trad
    #trad -= trad * fun.tax_rate(trad / ret_years) #* ret_years math mistake
    trad *= 1 - fun.tax_rate(trad / ret_years) #* ret_years math mistake
    ret_tot.append(roth+trad)

    print(repr(i).rjust(3), repr(round(roth/ret_years, 1)).rjust(6), \
          repr(round(trad/ret_years, 1)).rjust(6), \
          repr(round((roth+trad)/ret_years, 1)).rjust(6), \
          repr(round(fun.tax_rate(trad/ret_years), 3)).rjust(5))
     
  print(ret_tot.index(max(ret_tot)), ret_tot.index(min(ret_tot)))
  print(max(ret_tot), min(ret_tot))
  print(max(ret_tot)/ret_years, min(ret_tot)/ret_years)
  plt.plot(np.arange(0,41,1), ret_tot)
  plt.title("Trad for x Years Followed by Roth")
  plt.xlabel("Years into Trad")
  plt.show()
  #trial_4()
if __name__=="__main__":
      
  trial_3()
  trial_4()

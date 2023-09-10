import textwrap
import json

# Use with caution: tax rules are not fully understood and may be misrepresented.
# Income upward of 150000/yr will produce inaccurate FICA results.

class Tax_Code:
  pass

def assign_brackets(vals):

  dic = {}
  i = 0

  while i < len(vals):
    try:
      dic[int(vals[i+1])] = float(vals[i])
      i += 2
    except ValueError:
      i += 1
    except IndexError:
      break

  return dic

citystate = {'nyc' : 'ny'}

def get_brackets(loc='nyc'):
  
  with open("tax_brackets.json") as f:
    #tax_juris = json.load(f)
    all_juris = json.load(f)
  #return tax_juris
  
  tax_juris = {"fed":{}}

  # TODO error handling for invalid loc
  if loc:
    state = citystate.get(loc, loc)   # Get state if city, else state=loc
    tax_juris[state] = {}

  if loc in citystate:
    tax_juris[loc] = {}

  for x in tax_juris:
    tax_juris[x] = {eval(cutoff): all_juris[x][cutoff] \
                    for cutoff in all_juris[x]}

  return tax_juris

    # This shouldn't be necessary every time the calculator is called.
  #  with open("tax_brackets_" + x + ".csv") as f:
  #    vals = f.read().split()

  #  tax_juris[x] = assign_brackets(vals)

  #return tax_juris

# New strat: read in all tax juris into single dict, then assign the desired one.

#print(textwrap.fill("Choose one of the following locations for determining "
#                    "taxes (must be typed exactly, omit for no state or city "
#                    "tax):"))
#print("Choose one of the following locations for determining taxes \n"
#      "(must be typed exactly, omit for no state or local tax):")
#print(*["nyc", "ny", "ca"], sep='\n')
#location = input('> ')
location = 'nyc'   # Default location if no user input option.
tax_juris = get_brackets(location)  # Make this an argument in tax_calc for scalability
std_ded = {'fed' : 12950, 'ny' : 8000, 'ca' : 5202, 'nyc': 8000}
#cities = ['nyc']
#states = ['ny', 'ca']
#locs = {'ny' : ['nyc'], 'ca' : []}
#states = ('ny', 'ca')    # Better lookup time complexity than list?

def tax_calc(salary, partner=None, loc='nyc'):

  # Tests:
  # salary=partner (should be same as single filer unless exceeding fica limits.
  # swap salary and partner (should get same results).
  # TODO this block is not yet in use
  if partner is not None:  # partner salary can be 0 and still file jointly
    sal1 = salary
    sal2 = partner
    salary = sal1 + sal2
    # We will need a retirement plan for both partners in one iteration of 
    # the program.
  
  #deduction = {'fed': std_ded['fed']}
  #if loc:
  #  state = citystate.get(loc, loc)   # Get state if city, else state=loc
    #deduction[state] = std_ded[state]
  #  if loc in citystate:
  #  city = loc
    #deduction[city] = std_ded[city]
  #deduction = {x:y for x, y in zip(tax_juris, \
  #             [std_ded['fed'], std_ded[state], std_ded[city]])}
  deduction = {x: std_ded[x] for x in tax_juris}
  # get tax_juris as argument. std deduction should be dictated by juris
  taxes = {x:0 for x in tax_juris}

  for x in tax_juris:
    brackets = [y for y in tax_juris[x]]
    i = 0
    taxable = max(salary - deduction[x], 0)
    #taxable = salary - deduction[x]   # This mistake was responsible for
                                      # steep dropoff if not trad contributions
                                      # are ever made
    #while 0 < brackets[i] < salary-deduction[x]:
    while 0 < brackets[i] < taxable:
      taxes[x] += (brackets[i]-brackets[i-1]) * tax_juris[x][brackets[i]] * .01
      i += 1
    #taxes[x] += (salary-deduction[x] - brackets[i-1]) * \
    taxes[x] += (taxable - brackets[i-1]) * \
                 tax_juris[x][brackets[i]] * .01

  soc_sec = .062 * min(salary, 160200)
  medi = .0145 * salary + .009 * max(salary-200000, 0)
  fica = soc_sec + medi
  taxes["fica"] = fica

  #return taxes
  return sum([taxes[x] for x in taxes])
  #for x in tax_juris:
  #  print(tax_juris[x])

def tax_rate(salary):
  if salary == 0:
    return 0
  return tax_calc(salary) / salary

def cap_gains(cg, sal):
  cutoffs = [41675, 459750]
  rates = [0, .15, .2]
  tot_income = cg + sal
  tax = 0
  if tot_income > cutoffs[1]:
    tax += (tot_income - max(sal, cutoffs[1])) * rates[2]
  if tot_income > cutoffs[0]:
    tax += max(0, (min(tot_income, cutoffs[1]) - max(sal, cutoffs[0])) * rates[1])
  return tax

if __name__ == "__main__":

  for i in range(2, 11, 2):
    print(str(i*10) + "k", tax_calc(i*10000), tax_rate(i*10000))
  #print(sum([taxes[x] for x in taxes]))
  #with open("tax_brackets.json", 'w') as f:
  #  json.dump(tax_juris, f)   # Maybe should use two list method instead of dic








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

def tax_calc(salary):

  tax_juris = {"fed":{}, "nys":{}, "nyc":{}}
  
  for x in tax_juris:

    # This shouldn't be necessary every time the calculator is called.
    with open("tax_brackets_" + x + ".csv") as f:
      vals = f.read().split()

    tax_juris[x] = assign_brackets(vals)
  
  deduction = {x:y for x, y in zip(tax_juris, [12950, 8000, 8000])}
  taxes = {x:0 for x in tax_juris}

  for x in tax_juris:
    brackets = [y for y in tax_juris[x]]
    i = 0
    while 0 < brackets[i] < salary-deduction[x]:
      taxes[x] += (brackets[i]-brackets[i-1]) * tax_juris[x][brackets[i]] * .01
      i += 1
    taxes[x] += (salary-deduction[x] - brackets[i-1]) * \
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

if __name__ == "__main__":

  for i in range(2, 11, 2):
    print(str(i*10) + "k", tax_calc(i*10000), tax_rate(i*10000))
  #print(sum([taxes[x] for x in taxes]))








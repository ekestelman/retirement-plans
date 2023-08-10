# Testing module
# Instructions: replace elements in "files" list with filenames containing \
# the desired inputs for the main program. To save test case results, set \
# new_save = True. To test the program against previously saved answers, set \
# new_save = False.
# What needs to be tested? Salaries/contributions above and below limit. Non
# zero starting balance, pension. Increased limit over 50.

import json
import main
import sys

# Clean up main so that we can also just test the summary results?
# Check which part of each test case failed? (roth, trad, or priv dict)

def ret_plan_test(args, rothorder, result, trial):
  try:
    new_result = list(main.ret_plan(args, rothorder))
    assert new_result == result, \
           "ret_plan_test case "+trial+" FAILED"
           #"ret_plan_test "+str(args)+' '+str(rothorder)+" FAILED"
           # Show filename instead of args?
    #print("OK")    # Comment out to minimize print statements
    return 1   # For adding to success count
    # Consider just giving a final count of passed/failed cases?
    # Maybe a better way: add to a results list, then summarize results
  except AssertionError as ae:
    print("AssertionError:", ae)
    if False:  # Toggle for breakdown of failed cases
      for old,new,category in zip(result, new_result, ["tot", "sep", "draw"]):
        if old != new:
          print("Failed", category)
          if type(old)==type(new)==dict:
            for key in old:
              if old[key] == new[key]:
                print("P", key)
              else:
                print("F", key)
          else:
            allg = True
            for x,y in zip(old,new):
              if round(x,9)==round(y,9):
                continue
                print("Something worked", x, old.index(x))
              else:
                allg=False
                print("F", x, y, old.index(x))
            if allg: print("...but only by roundoff error")
        else:
          print("Passed", category)
      #if type(x) == dict:
      #  for key in x
      #    if result[key] != new_result[key]:
      #  print("Failed", key)  # Just do each as individual case?
      #else:
      #  print("Passed", key)
    #for key in new_results:
    #  if key not in results:
    #    print(key, "not tested")
    return 0   # For adding to success count

def save_output(results, fname):   # Pointless funcification?
  with open(fname, 'w') as f:
    json.dump(results, f, indent=2)

def overwrite():
  if sys.argv[-1] == "new":
    print("Are you sure you want to overwrite previous test cases? (y/n)")
    answer = input()
    if answer == "y":
      return True
    else:
      print("Aborting overwrite. Testing existing cases.")
  return False
    #  raise KeyboardInterrupt  # just an idea

def add_case():
  try:
    if sys.argv[1] == "add":
      with open(sys.argv[2]) as f:
        new_case = json.load(f)
      return new_case
  except IndexError:
    pass         # Return None if sys.argv != "add" or DNE

if __name__ == "__main__":
  new_save = overwrite()     # False by default
  add_case = add_case()
  with open("test_cases.json") as f:
    cases = json.load(f)
  if add_case:
    if add_case not in cases["ins"].values():
      # FIXME will overwrite other test case if any numbers are missing!
      cases["ins"][str(len(cases["ins"]))] = add_case
      save_output(cases, "test_cases.json")
      print("Added new test case")
    else:
      print("Duplicate test case")
  ins = cases["ins"]      # Inputs
  if new_save:
    outs = {}
    for key in ins:
      try:
        for i in range(1,3):
          results = main.ret_plan(ins[key], i)
          outs[key+'.'+str(i)] = results
        print("...Saving new test cases for "+key)
      except KeyError as ke:
        #print("KeyError:", ke, "on file", fname)
        print("KeyError:", ke, "on case", key)
    cases["outs"] = outs
    save_output(cases, "test_cases.json")
  else:
    outs = cases["outs"]  # Outputs
    score = 0
    for key in ins:
      results = [None, None]
      try:
        args = ins[key]
        for i in range(1,3):
          results[i-1] = outs[key+'.'+str(i)]
          score += ret_plan_test(args, i, results[i-1], key+'.'+str(i))
          # Not necessary to ever return 0 because exception will be raised
      except KeyError as ke:
        print("KeyError", ke, "on case", key)
    print("Passed", score, '/', len(outs), "test cases")
    # len(outs) won't include unsaved cases from ins?






# Testing module
# Instructions: `python test.py add [filename]` to add new test case.
# `python test.py new` to save new results for all test cases (necessary when
# adding new test case). `python test.py detail` for details on failed cases.
# Old Instructions: replace elements in "files" list with filenames containing \
# the desired inputs for the main program. To save test case results, set \
# new_save = True. To test the program against previously saved answers, set \
# new_save = False.
# What needs to be tested? Salaries/contributions above and below limit. Non
# zero starting balance, pension. Increased limit over 50. Cont > match.

import json
import main
import sys

# Clean up main so that we can also just test the summary results?
# Check which part of each test case failed? (roth, trad, or priv dict)
# Allow clargs to choose a test case file or what file to write new cases to.

for x in sys.argv[1:]:
  if x[0] == '-':
    continue
    # '-' indicates flags that are not filenames
  else:
    casefile = x
    break
    # Assign clarg filename to casefile. This is the file with all test cases.
    # Not to be confused with the file to load a new test case from.
    # Consider reorganizing: currently first filename is casefile, filenames
    # after are ignored and can be used for new cases. Consider different order?

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
    #if False:  # Toggle for breakdown of failed cases
    #if sys.argv[-1] == "detail":
    if "-detail" in sys.argv or "-d" in sys.argv:
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

# TODO option create new save without needing to overwrite old saves?
def overwrite():
  #if sys.argv[-1] == "new":
  if "-new" in sys.argv or "-n" in sys.argv:
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
    #if sys.argv[1] == "add":
    # Can get rid of try-except?
    if "-add" in sys.argv or "-a" in sys.argv:
      #with open(sys.argv[2]) as f:
      #with open(casefile) as f: # casefile is not the new case file
      with open(sys.argv[-1]) as f: # Assumes last arg is new case file
        new_case = json.load(f)
      return new_case
  except IndexError:
    pass         # Return None if sys.argv != "add" or DNE

if __name__ == "__main__":
  new_save = overwrite()     # False by default
  add_case = add_case()
  #with open("test_cases.json") as f:
  with open(casefile) as f:
    cases = json.load(f)
  new_cases = []  # If no add_case then we iterate over empty list.
  if add_case:
    for x in add_case:
      if type(x) is not dict:
        #single = True
        new_cases = [add_case]
        break
        # We can now iterate over the single test case being added.
      else:  # type(x) is dict, we can proceed
        new_cases = add_case  # new_cases is list of all new cases to be added.
        break
  # not the best variable naming...
  if type(new_cases) is not list:
    # Probably not necessary
    quit("Trying to add new cases not in list format. Aborting.")
  for add_case in new_cases:
    if add_case not in cases["ins"].values():
      # FIXME will overwrite other test case if any numbers are missing!
      # Add a check to see if test case file is properly enumerated.
      cases["ins"][str(len(cases["ins"]))] = add_case
      #save_output(cases, "test_cases.json")
      save_output(cases, casefile)
      print("Added new test case")
    else:
      print("Duplicate test case")
      # FIXME bug where you can add duplicate test cases if work years and/or
      # ret years are different but will become the same after running the
      # program (deprecated attributes that are now computed using age / ret
      # age / life
  ins = cases["ins"]      # Inputs
  if new_save:
    outs = {}
    # TODO way to only write new case without overwriting old
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
    #save_output(cases, "test_cases.json")
    save_output(cases, casefile)
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






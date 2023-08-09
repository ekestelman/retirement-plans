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

# Test arrays output by ret_plan?
# Clean up main so that we can also just test the summary results?
# Way of adding test case from file?

def ret_plan_test(args, rothorder, result):
  try:
    assert list(main.ret_plan(args, rothorder)) == result, \
           "ret_plan_test "+str(args)+' '+str(rothorder)+" FAILED"
           # Show filename instead of args?
    print("OK")
  except AssertionError as ae:
    print("AssertionError", ae)

def save_output(results, fname):   # Pointless funcification?
  with open(fname, 'w') as f:
    json.dump(results, f, indent=2)

def overwrite():
  try:
    if sys.argv[1] == "new":
      print("Are you sure you want to overwrite previous test cases? (y/n)")
      answer = input()
      if answer == "y":
        return True
      else:
        return False
      #  raise KeyboardInterrupt  # just an idea
    else:
      return False
  except IndexError:
    return False

if __name__ == "__main__":
  new_save = False    # Use cmd args to change?
  new_save = overwrite()
  with open("test_cases.txt") as f:
    cases = json.load(f)
  ins = cases["ins"]      # Inputs
  if new_save:
    outs = {}
    for key in ins:
      try:
        for i in range(1,3):
          results = main.ret_plan(ins[key], i)
          outs[key+str(i)] = results
        print("...Saving new test cases for "+key)
      except KeyError as ke:
        #print("KeyError:", ke, "on file", fname)
        print("KeyError:", ke, "on case", key)
    cases["outs"] = outs
    save_output(cases, "test_cases.txt")
  else:
    outs = cases["outs"]  # Outputs
    for key in ins:
      results = [None, None]
      try:
        args = ins[key]
        for i in range(1,3):
          results[i-1] = outs[key+str(i)]
          ret_plan_test(args, i, results[i-1])
      except KeyError as ke:
        print("KeyError", ke, "on case", key)






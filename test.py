# Testing module
# Instructions: replace elements in "files" list with filenames containing \
# the desired inputs for the main program. To save test case results, set \
# new_save = True. To test the program against previously saved answers, set \
# new_save = False.

import json
import main

# Test arrays output by ret_plan?
# Clean up main so that we can also just test the summary results?

def ret_plan_test(args, rothorder, result):
  assert list(main.ret_plan(args, rothorder)) == result, \
         "ret_plan_test "+str(args)+' '+str(rothorder)+" FAILED"
         # Show filename instead of args?
  print("OK")

def save_output(results, fname):
  with open(fname, 'w') as f:
    json.dump(results, f)

if __name__ == "__main__":
  new_save = False    # Use cmd args to change?
  if new_save:
    cases = {}
  else:
    with open("test_cases.txt") as f:
      cases = json.load(f)
  files = ["bimodal_trad.txt", "config.txt", "constant.txt", "even_peaks.txt", "high_cont_low_roi.txt"]
  for fname in files:
    with open(fname) as f:
      args = json.load(f)
    if new_save:
      try:
        for i in range(1,3):
          results = main.ret_plan(args, i)
          #save_output(results, 'test'+str(i)+fname)
          cases[fname+str(i)] = results
        print("...Saved new test cases for "+fname)
      except KeyError as ke:
        print("KeyError:", ke, "on file", fname)
    else:
      results = [None, None]
      try:
        for i in range(1,3):
          #with open("test"+str(i)+fname) as f:
          #  results[i-1] = json.load(f)
          results[i-1] = cases[fname+str(i)]
          ret_plan_test(args, i, results[i-1])
      except FileNotFoundError as fnfe:
        print(fnfe)
      except KeyError as ke:
        print("KeyError", ke, "on file", fname)
  if new_save:
    save_output(cases, "test_cases.txt")  # Consider pretty print






import numpy as np
import json
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import main

try:
  if sys.argv[1][-4:] == ".txt" or sys.argv[-1][-5:] == ".json":
    with open(sys.argv[1]) as f:
      vals = json.load(f)
    print("loading cmd arg file")
except:
  loadfile = 'history.txt'              # Handle exception if no history.txt?
  vals = main.get_vals(dic=True, loadfile=loadfile)
  print("loading", loadfile)

rothorder = 1
vals['rothorder'] = rothorder   # But would we prefer simultaneous plots?

#fig, ax = plt.subplots()
fig = plt.figure()
ax = plt.subplot(211)
ax1 = plt.subplot(223)
ax2 = plt.subplot(224)
under = False     # Place textboxes under graph (or to the right)
if under:
  fig.subplots_adjust(bottom=.4)  # Make this a function of len(vals?)
else:
  fig.subplots_adjust(right=.75)
#year = np.arange(vals["age"], vals["ret age"])  # To display age instead of
                                                 # years from today, but not
                                                 # yet operational.
#year = np.arange(0, vals["work years"]+1, 1)
# TODO rothorder arg in ret_plan does nothing
plans = [None, None]
plans[0] = main.ret_plan(vals, 1)
vals["rothorder"] = 2
plans[1] = main.ret_plan(vals, 2)
vals["rothorder"] = 1    # Necessary for tbox to show 1 initially.
#for x in plans:
#  print("Plan\n")
#  for y in x:
#    print(y,'\n')
#line, = ax.plot(main.ret_plan(vals, rothorder)[0])
line, = ax.plot(plans[0][0])
#vals["rothorder"] = 2
#line2, = ax.plot(main.ret_plan(vals, rothorder)[0])
line2, = ax.plot(plans[1][0])
#comps = [x[1] for x in plans]  # Components
piedata = main.summary(plans)
pies = [ax1, ax2]
plabels = ["Roth", "Traditional", "Private", "Pension"]
for i in range(2):
  use_labels = [label if val>0 else '' for label,val in \
                zip(plabels,piedata[i].values())]
  #pies[i].pie(piedata[i].values(), autopct='%1.1f%%', labels=['r','t','pr','pe'])
  pies[i].pie(piedata[i].values(), autopct=lambda p: '{:.1f}%'.format(p) \
              if p>0 else '', labels=use_labels)
#pies[0].legend()  # set labeldistance=1 in pie()?
#pie1 = ax1.pie(comps[0].values)
# Could be plt.plot if only one axis object, else ax needs to be specified.

del vals['normalize'], vals['work years'], vals['ret years']
# This breaks something: KeyError: 'work years' line 38

def update(arg):     # Alternative: 0 args in update() and remove next line
                     # ^may be better if I want to only allow certain args
                     # to be cahnged.
  newvals = {v : eval(boxes[v].text) for v in vals}
  budget = main.ret_plan(newvals, rothorder) # newvals -> vals
                                                # if alt method
  newvals["rothorder"] = newvals["rothorder"] % 2 + 1
  budget2 = main.ret_plan(newvals, rothorder)
  newvals['work years'] = newvals['ret age'] - newvals['age']
  years = np.arange(0, newvals['work years']+1, 1)
  #line.set_ydata(budget)   # Insufficient of we change age/ret age/work years
  line.set_data(years, budget[0]) # 0:yearly total, 1:components, 2:withdrawal
  line2.set_data(years, budget2[0])
  high = max(np.max(budget[0]), np.max(budget2[0]))
  low = min(np.min(budget[0]), np.min(budget2[0]))
  diff = high-low
  ax.set_ylim(low-diff*.05, high+diff*.05)
  ax.set_xlim(-.05*newvals['work years'], 1.05*newvals['work years'])
  piedata = main.summary([budget, budget2])
  plabels = ["Roth", "Traditional", "Private", "Pension"]
  for i in range(2):
    use_labels = [label if val>0 else '' for label,val in \
                  zip(plabels,piedata[i].values())]
    pies[i].clear()   # Prevents rotating through colors
    #pies[i].pie(piedata[i].values(), autopct='%1.1f%%')
    pies[i].pie(piedata[i].values(), autopct=lambda p: '{:.1f}%'.format(p) \
                if p>0 else '', labels=use_labels)
    # TODO show percentages in pie chart. Show legend instead of labels?
  plt.draw()
def new_apy(arg):
  #vals["apy"] = 1 + float(arg) / 100  # Maybe better? But need to edit textbox
  vals["apy"] = float(arg)
  update()
def new_life(arg):
  vals["life"] = int(arg)  # Not recomputing ret_years in main
  update()

i = 0
boxes = {}
for v in vals:
  #if v=="ret years" or v=='work years' or v=='normalize':
  #  continue
  if under:
    axbox = plt.axes([.1+i%2*.5, .05+i//2*.05, .2, .045])  # 2 columns under graph
  else:
    axbox = plt.axes([.825, .825-i*.05, .15, .045])
  boxes[v] = TextBox(axbox, v+": ", vals[v])  # Try another dic of printable var names
                                         # printable["life"] = "Life expectancy"
  boxes[v].on_submit(update)
  i += 1
#axbox = plt.axes([.1, .05, .2, .075])
#apy_box = TextBox(axbox, "APY: ", vals["apy"])
#apy_box.on_submit(new_apy)
##text_box.on_text_change(new_apy)
#axbox = plt.axes([.6, .05, .2, .075])
#life_box = TextBox(axbox, "Life Expectancy: ", 90)
#life_box.on_submit(new_life)


plt.show()

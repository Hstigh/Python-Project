import pandas as pd 

all_transactions = pd.read_csv('data2.csv', error_bad_lines=False, index_col=None, header=0, engine='python').to_dict()
all_shares = pd.read_csv('data3.csv', error_bad_lines=False, index_col=None, header=0, engine='python').to_dict()

print("reset")
print("back")
print("record")

for i in range(1, len(all_transactions['id'])):
  names = []
  shares = []
  for j in range(1, len(all_shares['id'])):
    if all_transactions['id'][i] == all_shares['id'][j]:
      names.append(all_shares['name'][j])
      shares.append(str(all_shares['sahm'][j]))
  
  print(str(all_transactions['date'][i]) + " " + all_transactions['daste'][i] + " " + all_transactions['zirdaste'][i] + " " + str(all_transactions['mablagh'][i])
  + " [" + ",".join(names) + "] " + "id1 [" + ",".join(shares) + "] description")

print("back")
print("report")
print("analys")
print("Ghabz")
print("inv")
print("1399-01-01")
print("1399-10-20")
print("plot")
print("1397-01-01")
print("1399-10-20")
print("Water")
print("back")
print("exit")

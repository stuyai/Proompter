import json

def setBalance(id: str, name:str,  amount: str):
    with open("userData.json", "r") as f:
        data = json.load(f)
        
    if str(id) not in data:
        data[str(id)] = {}
        data[str(id)]["name"] = name
        data[str(id)]["balance"] = 100
        
    data[str(id)]["balance"] = amount
    
    with open("userData.json", "w") as f:
        json.dump(data, f, indent=4)
    
    
def getBalance(id: str, name: str) -> int:
    with open("userData.json", "r") as f:
        data = json.load(f)
    
    if str(id) not in data:
        data[str(id)] = {}
        data[str(id)]["name"] = name
        data[str(id)]["balance"] = 100
    
    with open("userData.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return int(data[str(id)]["balance"])

def restoreAllBalances(value: int):
    with open("userData.json", "r") as f:
        data = json.load(f)
        
    for key in data:
        data[key]["balance"] = value
        
    with open("userData.json", "w") as f:
        json.dump(data, f, indent=4)

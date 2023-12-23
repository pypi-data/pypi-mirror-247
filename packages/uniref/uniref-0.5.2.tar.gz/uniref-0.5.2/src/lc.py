from uniref import WinUniRef

ref = WinUniRef("Lethal Company.exe")

manager = ref.find_class_in_image("Assembly-CSharp", "GameNetworkManager")
manager.instance = manager.find_field("<Instance>k__BackingField").value

manager.find_field("maxAllowedPlayers").value = 10

terminal = ref.find_class_in_image("Assembly-CSharp", "Terminal")
money = terminal.find_field("groupCredits")

for address in terminal.guess_instance_address():
    money.instance = address
    if money.value == 60:
        money.value = 999999999

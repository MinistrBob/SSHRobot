"""
If all the servers have the same login, and the IP list is a simple sequence,
then the server list can be generated automatically
"""
net = "10.128.241."
# range must be specified with last + 1, for example, I need 101-232, so the range should be range(101, 233)
seq = range(101, 233)
login = "root"
password = "RootPassword123"

print("server_list = {")
for ip in seq:
    print(f"    '{net}{ip}': ('{login}', '{password}'),")
print("}")

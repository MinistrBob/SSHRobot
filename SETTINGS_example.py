import SL
import CL

# Current SL (Server List)
# sl = SL.server_list_full
# sl = SL.cassandra_servers
# sl = SL.test_servers
sl = SL.server_list

# Current CL (Command List)
cl = CL.command_list
########################################################################################################################

default_SSH_port = '22'

# constanta - subnet
net = "10.128.241."
# constanta - range ip addresses in subnet, begin = first IP, end = last IP
begin = 101
end = 232
end += 1
seq = range(begin, end)
# constanta - if there is INCLUDE list then it is used instead of SEQ
include = ()
# constanta - ip addresses to be excluded from processing
exclude = (105, 106, 107, 108, 109, 110, 111, 112, 113, 117, 118, 119, 120, 125,
           126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138,
           139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151,
           152, 153, 154, 155, 156, 157, 185, 186, 187, 188, 189, 190, 191,
           192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204,
           205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217,
           218, 219, 220, 221, 222, 225, 226, 227, 228, 229, 230, 231, 232)
# dictionary - a lot of any parameters
param = {'login': 'root',
         'password': 'root_password',
         'hostname': 'dc1-db-XXX'  # template for hostname, can consist replace pattern
         }

import SL
import CentOS8 as MOD
import FOL

############### MAIN SETTINGS ###############
# SSH port
default_SSH_port = '22'

# DEBUG
debug = False
if debug:
    # Debug SL (Server List)
    sl = SL.debug_server
    # Debug CL (Command List)
    module = MOD.c_dnf_proxy
    # Debug FOL (File Operation List)
    fl = FOL.file_operations_list
    # Show after and before (execute show command and print result execution)
    show_after = True
    show_before = True
else:
    # Current SL (Server List)
    sl = SL.full_server_list_current
    # sl = SL.server_list2
    # Current CL (Command List)
    module = MOD.c_dnf_proxy_check
    # FOL (File Operation List)
    fl = FOL.file_operations_list
    show_after = False
    show_before = False

# Empty output strings replece with replace_empty_out_str_template
# (sometimes it may be needed for debugging)
replace_empty_out_str_with_null = False
replace_empty_out_str_template = "<NULL>"
# Success sign is added to the list of successful executions (may be True)
success_sign = 'ОК'



############### REPORT SETTINGS ###############
# Need report (list success and failure servers)
report = True
succes_list_report = True

############### GENERATOR SETTINGS ###############
# constanta - subnet
net = "10.128.241."
# constanta - range ip addresses in subnet, begin = first IP, end = last IP
begin = 135
end = 147
end += 1
seq = range(begin, end)
# constanta - if there is INCLUDE list then it is used instead of SEQ
include = ()
# constanta - ip addresses to be excluded from processing (only for generation SL)
exclude = (105, 106, 107, 108, 109, 110, 111, 112, 113, 117, 118, 119, 120, 125,
           126, 127, 128, 129, 130, 131, 132, 133, 134, 155, 156, 157, 185, 186, 187, 188, 189, 190, 191,
           192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204,
           205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217,
           218, 219, 220, 221, 222, 225, 226, 227, 228, 229, 230, 231, 232)
# dictionary - a lot of any parameters
param = {'login': 'root',
         'password': 'P@ssw0rds77',
         'hostname': 'ca-isarch-XXX.dc1.local'  # template for hostname, can consist replace pattern
         }

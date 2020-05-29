"""
If all the servers have the same login, and the IP list is a simple sequence,
then the server list can be generated automatically
"""
from SETTINGS import net, seq, include, exclude, param


def get_exclude_list(begin, end):
    list_ = []
    for i in range(begin, end + 1):
        list_.append(str(i))
    return ', '.join(list_)


def get_inner_dict():
    list_ = []
    for key, value in param.items():
        list_.append(f"'{key}': '{value}'")
    list_ = ', '.join(list_)
    return f"{{{list_}}}"


def generate_servers_list():
    inner_dict = get_inner_dict()
    list_ = []
    if len(include) == 0:
        seq_ = seq
    else:
        seq_ = include
    for ip in seq_:
        if ip not in exclude:
            list_.append(f"    '{net}{ip}': {inner_dict}")
    list_ = ',\n'.join(list_)
    return f"server_list = {{\n{list_}\n}}"


if __name__ == '__main__':
    # Generate list excludes
    # list_ = get_exclude_list(225, 230)
    # print(list_)

    # Generate servers list
    list_ = generate_servers_list()
    print(list_)

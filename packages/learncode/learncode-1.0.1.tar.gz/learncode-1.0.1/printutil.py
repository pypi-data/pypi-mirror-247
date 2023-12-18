def print_lol(data_list,indent=False,level=0):
    for eachItem in data_list:
        if isinstance(eachItem,list):
            print_lol(eachItem,level+1)
        else:
            if indent:
                for e in range(level):
                    print('\t',end='')
            print(eachItem)
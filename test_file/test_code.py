lst = ['0', '1', '2', '0']
date = ['03/12', '04/15', '08/13', '14/22']
if x:= [i for i, x in enumerate(lst) if lst.count(x) > 1]:
    # w = []
    for indx in x:
        q = lst[indx]+f'_{date[indx]}'
        # w.append(q)
    # print(w)
        lst[indx] = q
    print(lst)
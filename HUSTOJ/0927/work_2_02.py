def is_tree(num_list):
    if len(num_list) <= 2:
        return True
    pos = 0
    for i in range(0,len(num_list) - 1):
        pos += 1 if num_list[i] < num_list[-1] else 0
            
    for i in num_list[pos:len(num_list)-1]:
        if i < num_list[-1]:
            return False

    return True if len(num_list) == 3 else is_tree(num_list[0:pos]) & is_tree(num_list[pos:len(num_list)-1])

print('true' if is_tree(list(map(int,input().split()))) else 'false')
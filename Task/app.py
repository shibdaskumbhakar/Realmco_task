# Python3 code to demonstrate
# to delete dictionary in list
# using del + loop

# initializing list of dictionaries
test_list = [{"id": 1, "data": "HappY"},
             {"id": 2, "data": "BirthDaY"},
             {"id": 3, "data": "Rash"}]


# using del + loop
# to delete dictionary in list
for i in range(len(test_list)):
    if test_list[i]['id'] == 3:
        del test_list[i]
        break

# printing result
print("List after deletion of dictionary : " + str(test_list))

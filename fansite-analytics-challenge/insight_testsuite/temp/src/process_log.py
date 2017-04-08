# your Python code to implement the features could be placed here
# note that you may use any language, there is no preference towards Python
import sys
from datetime import datetime, date, timedelta

input_file = open(sys.argv[1])
output_host = open(sys.argv[2],'a')
output_resources = open(sys.argv[4],'a')
output_hours = open(sys.argv[3],'a')
output_blocked = open(sys.argv[5],'a')

# reading the data and storing in lists
address = []
site = []
byte = []
date_time = []
http_code = []
data =[]
for line in input_file:
    new_line = line.split()
    address.append(new_line[0])
    site.append(new_line[6])
    byte.append(new_line[-1])
    x = new_line[3:5]
    time_string = ' '.join(x)
    date_time.append(time_string[1:-1])
    http_code.append(int(new_line[-2]))
    line = line.replace('\n', '')
    data.append(line)

http_fail_code = [304, 305, 306, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 415, 416, 417, 500, 501, 502, 503, 504, 505]

# Feature 1
def most_active_address(address_list, site_list):
    counts = {}
    for item in range(len(address_list)):
        if len(site_list[item]) > 2:
            if address_list[item] not in counts:
                counts[address_list[item]] = 1
            else:
                counts[address_list[item]] += 1

    lst = []
    for key, val in counts.items():
        lst.append( (val, key) )

    lst.sort(reverse = True)


    for key, val in lst[:10] :
        v, k  = val, str(key)
        one_line = v +','+k
        # print (one_line)
        output_host.write('%s\n'%(one_line))
          
most_active_address(address, site)

# Feature 2

def most_bandwidth(site_list, byte_list):
    sums ={}
    for item in range(len(site_list)):
        if len(site_list[item]) >2:
            if byte_list[item] == '-':
                byte_list[item] = 0
            else:
                byte_list[item] = int(byte_list[item])
            if site_list[item] not in sums:
                sums[site_list[item]] = byte_list[item]
            else:
                sums[site_list[item]] += byte_list[item]
    lst = []
    for key, val in sums.items():
        lst.append( (val, key) )

    lst.sort(reverse = True)

    for key, val in lst[:10] :
        # print (val)
        output_resources.write('%s\n'%(val))


most_bandwidth(site, byte)

# Feature 3
start_date = datetime.strptime(date_time[0], "%d/%b/%Y:%H:%M:%S %z")
end_date = datetime.strptime(date_time[-1], "%d/%b/%Y:%H:%M:%S %z")

def new(date_time_list):
    start_time = start_date
    end_time = end_date
    counts = {}
    while (start_time <= end_time):
        for time in range(len(date_time_list)):
            date_and_time = datetime.strptime(date_time_list[time], "%d/%b/%Y:%H:%M:%S %z")
            end_interval = start_time + timedelta(minutes = 59)
            if (date_and_time > start_time):
                break
            else:
                if (date_and_time-start_time).total_seconds() >= float(60):
                    break
                else:
                    time_string = start_time.strftime('%d/%b/%Y:%H:%M:%S %z')
                    if time_string not in counts:
                        counts[time_string] = 1
                    else:
                        counts[time_string] += 1
        start_time += timedelta(seconds = 1)

    lst = []
    for key, val in counts.items():
        lst.append( (val, key) )

    lst.sort(reverse = True)


    for key, val in lst[:10] :
        v, k  = val, str(key)
        one_line = v +','+k
        # print (one_line)
        output_hours.write('%s\n'%(one_line))
    
new(date_time)


# Feature 4
def failed_login(http_list):
    length = len(http_list)
    list_failed_items = []
    for item in range(length):
        if http_list[item] in http_fail_code:
            list_failed_items.append(item)
    return list_failed_items


def triple_failed_indexes(http_list,address_list, date_time_list):
    list_failed_index = failed_login(http_list)
    length = len(list_failed_index)
    triple_failed_index = []
    for items in range(length):
        index = list_failed_index[items]
        look_for = address_list[index]
        look_date = datetime.strptime(date_time_list[index], "%d/%b/%Y:%H:%M:%S %z")
        items1 = items + 1
        for items_1 in range(items1,length):
            index_1 = list_failed_index[items_1]
            look_for1 = address_list[index_1]
            look_date1 = datetime.strptime(date_time_list[index_1], "%d/%b/%Y:%H:%M:%S %z")
            if (look_date1-look_date).total_seconds() > float(20):
                break
            else:
                if (look_for == look_for1):
                    items2 = items_1 + 1
                    for items_2 in range(items2,length):
                        index_2 = list_failed_index[items_2]
                        look_for2 = address_list[index_2]
                        look_date2 = datetime.strptime(date_time_list[index_2], "%d/%b/%Y:%H:%M:%S %z")
                        if (look_date2-look_date).total_seconds() > float(20):
                            break
                        else:
                            if (look_for == look_for2):
                                ban_5_min = look_date2 + timedelta(minutes =5)
                                items3 = items_2 + 1
                                for items_3 in range(items3, length):
                                    index_3 = list_failed_index[items_3]
                                    look_for3 = address_list[index_3]
                                    look_date3 = datetime.strptime(date_time_list[index_3], "%d/%b/%Y:%H:%M:%S %z")
                                    if (look_date3 > ban_5_min):
                                        break
                                    else:
                                        if (look_for == look_for3):
                                            triple_failed_index.append(index_3)
                                

    index_list = (list(set(triple_failed_index)))
    index_list.sort()
    return index_list

def ban_5_min_list(http_list, address_list, date_time_list, data_list):
    triple_fail_list = triple_failed_indexes(http_list,address_list,date_time_list)
    length = len(triple_fail_list)
    for items in range(length):
        index = triple_fail_list[items]
        data_print = data_list[index]
        # print (data_list[index])
        output_blocked.write('%s\n'%(data_print))
    
ban_5_min_list(http_code, address, date_time, data)

input_file.close()
output_host.close()
output_resources.close()
output_hours.close()
output_blocked.close()

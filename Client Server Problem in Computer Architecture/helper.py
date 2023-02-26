def ip_checksum(data):
    pos = len(data)
    if pos & 1:  
        pos -= 1
        sum = data[pos]
    else:
        sum = 0
    while pos > 0:
        pos -= 2
        sum += ((data[pos + 1]) << 8) + (data[pos])

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    result = (~ sum) & 0xffff 
    result = result >> 8 | ((result & 0xff) << 8)
    return chr(result // 256) + chr(result % 256)

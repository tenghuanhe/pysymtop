def dataconvert(data):
    """
    converts 12-bytes of data read from the serial port
    into x,y,z,roll,pitch,yaw (inch,inch,inch,deg,deg,deg)
    for a single bird
    """
    xls, xms = data[0], data[1]
    yls, yms = data[2], data[3]

    #
    xls = ord(xls) - 128  # change leading bit to zero
    xls <<= 1  # shift bits left
    x = ((xls + (ord(xms) * 256)) << 1)
    y = (((ord(yls) << 1) + (ord(yms) * 256)) << 1)

    if x > 32767: x -= 65536
    if y > 32767: y -= 65536

    # convert to inch and deg
    x = x * 144.0 / 32768.0
    y = y * 144.0 / 32768.0

    return x, y

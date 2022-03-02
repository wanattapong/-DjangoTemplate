import base64

# function set format date for insert to table
# date format input --> 01/05/2019
# date format output --> 2019-05-01
def date_format(date):
    if date == '':
        return None
    else:
        date = date.split('/')
        date = date[2]+'-'+date[1]+'-'+date[0]
        return date

def encode_url(number):
    encode = base64.b16encode(base64.b85encode(bytes(str(number), "utf-8"))).decode("utf-8", "ignore")
    return encode

def decode_url(number):
    decode = base64.b85decode(base64.b16decode(number)).decode("utf-8", "ignore")
    return decode
    
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
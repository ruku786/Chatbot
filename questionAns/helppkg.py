import re 
from flashgeotext.geotext import GeoText
geotext = GeoText(use_demo_data=True)

def get_keyword(request, msg):
    global geotext
    try:
        city = None
        city = list(geotext.extract(input_text= msg, span_info= True)["cities"].keys())[0]
        if not city:
            city=""
        else:
            city = " in "+city
        d=msg.split(" ")
        if "sq" in msg:
            word = re.findall(r'[sq]\S*', msg)
            
        if "bhk" in msg:
            word = re.findall(r'[bhk]\S*',msg)
        get_data ="searching "+str(d[d.index(word[0])-1])+" "+str(word[0])+city
        answer_status = True
    except Exception as e:
        print(e)
        get_data = None
        answer_status = True

    return get_data, answer_status

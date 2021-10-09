import json
from temp import Doc_directory
from flask import Flask, render_template, request, jsonify   
from datetime import date, datetime
import pickle

from werkzeug.wrappers import response

def calculator(chance_, percent_):
    ans=percent_
    global input_list
    for i in input_list:
        if i in chance_.keys():
            ans+=chance_[i]
    return ans

a=0
w=0
percent_hyper= 0
percent_arth= 0
percent_alzie= 0
percent_diab= 0
percent_depress= 0
percent_choles=0
percent_cataract=0
percent_cardio=0
chance_arth={'6':15,'5':15,'4':20,'7':5,'1':5,'3':5}
chance_hyper={'30':5,'32':5,'36':5,'33':5,'11':10,'35':10,'34':5,'1':5,'2':5}
chance_alzie={'31':10,'18':10,'17':10,'28':10,'29':10,'30':5,'3':5,'11':5,'4':5,'19':5}
chance_diab={'21':5,'24':10,'13':10,'19':10,'4':6,'20':14,'25':5,'26':5,'27':5}
chance_depress={'23':20,'22':10,'20':10,'11':10,'21':5,'3':8,'2':10,'17':5,'19':5,'18':5}
chance_choles={'1':15,'2':10,'3':10,'9':10,'25':10}
chance_cataract={'13':10,'2':10,'3':10,'14':10,'15':27,'16':33}
chance_cardio={'8':10,'3':10,'9':31,'10':15,'11':5,'12':5}

input_list=[]


Arthiritis=['1. Weight loss<br>','2. Physical exercise<br>','3. Yoga<br>','4. Heating Pad<br>']
HyperTension=[]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("InputOutput.html")        

@app.route("/submitJSON", methods=["POST"])
def processJSON(): 
    global percent_cardio,percent_alzie,percent_arth,percent_cataract, percent_choles
    global percent_depress,percent_diab,percent_hyper
    global a, w, input_list
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr)
    
    a=int(jsonObj['age'])
    w=int(jsonObj['weight'])
    age=a-60
    weight=w-65

    if age<25:
        f_age=0.8*age
    else:
        f_age=20

    if weight<42:
        f_weight=0.6*weight
    else:
        f_weight=25
    percent_hyper= f_age + f_weight
    percent_arth= f_age + f_weight
    percent_alzie= 0
    percent_diab= f_weight
    percent_depress= 0
    percent_choles= f_age + f_weight
    percent_cataract=0
    percent_cardio=f_weight
    input_list=[x for x in list(jsonObj['Input_lis'].split(','))]
    disease=['arth','hyper','alzie','diab','depress','choles','cataract','cardio']
    stat=[]
    for dis in disease:
        stat.append(tuple([dis, calculator(eval('chance_'+dis), eval('percent_'+dis))]))
    dictionary={
        'arth':'Arthritis',
        'hyper':'Hyper-Tension',
        'alzie':'Alzheimer\'s disease',
        'diab':'Diabetes',
        'depress':'Depression',
        'choles':'High Cholesterol',
        'cataract':'Cataract',
        'cardio':'Cardiovascular disease'
    }
    Details="You can try consulting these Doctors in your city:<br><br> "
    City_List=['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Ahmedabad', 'Pune', 'Lucknow', 'Chandigarh']
    f=open('Doctors.txt', 'rb')
    Doc_directory=pickle.load(f)
    f.close()
    stat.sort(key= lambda x:int(x[1]), reverse=True)
    addr=""
    for tup in stat:
        if tup[1]>=50:
            addr=""
            for x in Doc_directory:
                if (x['City']==jsonObj['city'])and(x['Disease']==dictionary[tup[0]]):
                    addr=""
                    lis=x['Address'].split(',')
                    for i in range(len(lis)):
                        addr+=lis[i]+','+(i+1)%2*'<br>'
                    Details+="For "+x['Disease']+'<br>'+x['Name']+'<br>'+x['Phone Number']+'<br>'+addr+"<br><br>"

    response='******************************************************************************<br>Probablity of diseases:<br><br>'
    for tup in stat:
        response+='  '+dictionary[tup[0]]+' : '+str(tup[1])+'%  <br>'
    response+="<br>******************************************************************************<br><br>"
    if jsonObj['city'] in City_List:
        if int(stat[0][1])>=50:
            response+='<br>'+Details
    return response
if __name__ =="__main__":
	app.run(debug=True)
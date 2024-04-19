from datetime import date, datetime,timedelta
from API.api import CoWinAPI
import geocoder
from geopy.geocoders import Nominatim
import pgeocode

import plotly.graph_objs as go

import pandas as pd




from flask import Flask, render_template, request, jsonify





@app.route('/getDistrict_byState_id', methods=['GET'])
def getDistrict_byState_id():
    state_id = request.args.get('state_id', type=int)
    districts = cowin.get_districts(state_id)
    return jsonify(districts['districts'])

@app.route('/getCenterdetails',methods=['GET'])
def getCenterdetails():
    # s_date:s_date,option:option,locationKey:locationKey, minage: minage, feeType:feeType, vaccineType:vaccineType
    s_date = request.args.get('s_date', type=str)
    option = request.args.get('option', type=str)
    state_id = request.args.get('state_id', type=str)
    locationKey = request.args.get('locationKey', type=str)
    minage = request.args.get('minage', type=str)
    feeType = request.args.get('feeType', type=str)
    vaccineType = request.args.get('vaccineType', type=str)

    year,month,day=map(int,s_date.split("-"))
    actualdate=datetime(year,month,day)
    list_format= [actualdate+timedelta(days=i) for i in range(3)]
    actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
    data_dict=[]
    data={}
    for given_date in actual_dates:
        if option =="DISTRICT":
            try:
                available_centers = cowin.get_availability_by_district(locationKey, given_date, int(minage))
                states = cowin.get_states()
                state_name=""
                for i in states['states']:
                    # print(i['state_id']==int(state_id))
                    if i['state_id']==int(state_id):
                        state_name=i['state_name']
                if len(available_centers['centers'])>0:
                    for center in available_centers['centers']:
                        if center['fee_type'].upper()==feeType.upper() and int(center['sessions'][0]['min_age_limit'])==int(minage) and center['sessions'][0]['vaccine'].upper()==vaccineType.upper() and int(center['sessions'][0]['available_capacity'])>0:

                            from_t=int(center['from'].split(":")[0])
                            to_t=int(center['to'].split(":")[0])
                            from_time=""
                            to_time=""
                            if from_t<12:
                                from_time=str(from_t)+":"+str(center['from'].split(":")[1])+" AM"
                            else:
                                from_time=str(from_t-12)+":"+str(center['from'].split(":")[1])+" PM"
                            if to_t<12:
                                to_time=str(to_t)+":"+str(center['to'].split(":")[1])+" AM"
                            else:
                                to_time=str(to_t-12)+":"+str(center['to'].split(":")[1])+" PM"
                            temp={}
                            # temp['Center name']=center['name']
                            temp['Center name']=center['name']+","+center['block_name']+","+center['address']+","+center['district_name']+"- "+str(center['pincode'])+","+center['state_name']
                            temp['Available capacity']=center['sessions'][0]['available_capacity']
                            temp['Dose 1 capacity']=center['sessions'][0]['available_capacity_dose1']
                            temp['Dose 2 capacity']=center['sessions'][0]['available_capacity_dose2']
                            temp['Date']=center['sessions'][0]['date']
                            temp['Vaccine']=center['sessions'][0]['vaccine']
                            temp['Min Age']=center['sessions'][0]['min_age_limit']
                            temp['Fee Type']=center['fee_type']
                            temp['From']=from_time
                            temp['To']=to_time
                            data_dict.append(temp)


            except:
                return jsonify({"status":"Error","payload":{},"msg":"something went wrong!"})
        else:
            try:
                available_centers = cowin.get_availability_by_pincode(locationKey, given_date, int(minage))
                nomi = pgeocode.Nominatim('in')
                state_name=nomi.query_postal_code(locationKey)['state_name']
                if len(available_centers['centers'])>0:
                        for center in available_centers['centers']:
                            if center['fee_type'].upper()==feeType.upper() and int(center['sessions'][0]['min_age_limit'])==int(minage) and center['sessions'][0]['vaccine'].upper()==vaccineType.upper() and int(center['sessions'][0]['available_capacity'])>0:
                                from_t=int(center['from'].split(":")[0])
                                to_t=int(center['to'].split(":")[0])
                                from_time=""
                                to_time=""
                                if from_t<12:
                                    from_time=str(from_t)+":"+str(center['from'].split(":")[1])+" AM"
                                else:
                                    from_time=str(from_t-12)+":"+str(center['from'].split(":")[1])+" PM"
                                if to_t<12:
                                    to_time=str(to_t)+":"+str(center['to'].split(":")[1])+" AM"
                                else:
                                    to_time=str(to_t-12)+":"+str(center['to'].split(":")[1])+" PM"
                                temp={}
                                # temp['Center name']=center['name']
                                temp['Center name']=center['name']+","+center['block_name']+","+center['address']+","+center['district_name']+"- "+str(center['pincode'])+","+center['state_name']
                                temp['Available capacity']=center['sessions'][0]['available_capacity']
                                temp['Dose 1 capacity']=center['sessions'][0]['available_capacity_dose1']
                                temp['Dose 2 capacity']=center['sessions'][0]['available_capacity_dose2']
                                temp['Date']=center['sessions'][0]['date']
                                temp['Vaccine']=center['sessions'][0]['vaccine']
                                temp['Min Age']=center['sessions'][0]['min_age_limit']
                                temp['Fee Type']=center['fee_type']
                                temp['From']=from_time
                                temp['To']=to_time
                                data_dict.append(temp)


            except:
                return jsonify({"status":"Error","payload":{},"msg":"something went wrong!"})

    ind=0
    u_df={}
    for d_df in data_dict:
        u_df[ind]=d_df
        ind+=1

    df=pd.DataFrame.from_dict(u_df, orient='index')
    if len(df)>0:
        newdf = df[['Date','Dose 1 capacity','Dose 2 capacity']].copy()
        bardf=newdf.groupby(['Date'])[['Dose 1 capacity', 'Dose 2 capacity']].sum().reset_index()
        barchart=bardf['Date']
        keys=[i for i in barchart]
        value1=[i for i in bardf['Dose 1 capacity'] ]
        value2=[i for i in bardf['Dose 2 capacity']]

        l_df=df[["Center name","Available capacity"]].copy()
        linedf=l_df.groupby(['Center name'])[["Available capacity"]].sum().reset_index()
        lkeys=[i.split(",")[0] for i in linedf['Center name']]
        lvalue=[i for i in linedf['Available capacity']]
    else:
        keys=[actualdate.strftime("%d-%m-%Y")]
        value1=[0]
        value2=[0]
        lkeys="NA"
        lvalue=[0]
    gdata=[
            {'name':'Dose 1', 'x':keys, 'y':value1,'type':'bar'},
            {'name':'Dose 2', 'x':keys, 'y':value2,'type':'bar'}
        ]
    ldata=[
            {'name':'Centers', 'x':lkeys, 'y':lvalue,'type':'scatter'},
    ]

    testing_report=cowin.get_testing_history()
    testing_data=[]
    for test_rep in testing_report['data']:
        temp={}
        temp['Date']=test_rep['day']
        year,month,day=map(int,test_rep['day'].split("-"))
        actualtime=10000*year + 100*month + day
        temp['int_date']=actualtime
        temp['totalSamplesTested']=test_rep['totalSamplesTested']
        testing_data.append(temp)
    ind=0
    testing_data_df={}
    for d_df in testing_data:
        testing_data_df[ind]=d_df
        ind+=1

    df_testing_data=pd.DataFrame.from_dict(testing_data_df, orient='index')
    today=datetime.today()
    t_y,t_m,t_d=map(int,str(today.strftime("%Y-%m-%d")).split("-"))
    t_startingpoint=datetime(year,month,day)-timedelta(7)
    t_y,t_m,t_d=map(int,str(t_startingpoint.strftime("%Y-%m-%d")).split("-"))
    t_actualtime=10000*t_y + 100*t_m + t_d
    # print(t_actualtime)
    # print(df_testing_data.head(1))
    test_df=df_testing_data.loc[df_testing_data['int_date']>t_actualtime]
    tg_key=[i for i in test_df['Date']]
    tg_value=[i for i in test_df['totalSamplesTested'] ]
    tgdata=[
            {'name':'Testing Samples Collected', 'x':tg_key, 'y':tg_value,'type':'scatter'},
    ]


    cases=cowin.get_latest_case_counts()
    case_data=[]
    for case_rep in cases['data']['regional']:
        temp={}
        temp['loc']=case_rep['loc']
        temp['totalConfirmed']=case_rep['totalConfirmed']
        temp['discharged']=case_rep['discharged']
        temp['deaths']=case_rep['deaths']
        case_data.append(temp)
    ind=0
    case_data_df={}
    for d_df in case_data:
        case_data_df[ind]=d_df
        ind+=1

    df_case_data=pd.DataFrame.from_dict(case_data_df, orient='index')
    case_df=df_case_data.loc[df_case_data['loc'] == state_name]
    case_state={}
    confirmed=int(case_df['totalConfirmed'])
    active=int((case_df['totalConfirmed']-(case_df['discharged']+case_df['deaths'])))
    recovered=int(case_df['discharged'])
    deaths=int(case_df['deaths'])
    case_state['confirmed']="{:,}".format(confirmed,",")
    case_state['active']="{:,}".format(active,",")
    case_state['recovered']="{:,}".format(recovered,",")
    case_state['deaths']="{:,}".format(deaths,",")

    hospital_beds=cowin.get_hospital_beds()
    hospital_beds_data=[]
    for beds in hospital_beds['data']['regional']:
        temp={}
        temp['state']=beds['state']
        temp['ruralHospitals']=beds['ruralHospitals']
        temp['urbanHospitals']=beds['urbanHospitals']
        temp['ruralBeds']=beds['ruralBeds']
        temp['urbanBeds']=beds['urbanBeds']
        temp['totalHospitals']=beds['totalHospitals']
        temp['totalBeds']=beds['totalBeds']
        hospital_beds_data.append(temp)
    ind=0
    hospital_beds_data_df={}
    for d_df in hospital_beds_data:
        hospital_beds_data_df[ind]=d_df
        ind+=1

    df_beds_data=pd.DataFrame.from_dict(hospital_beds_data_df, orient='index')
    beds_df=df_beds_data.loc[df_beds_data['state'] == state_name]
    hospital_beds={}
    ruralHospitals=int(beds_df['ruralHospitals'])
    ruralBeds=int(beds_df['ruralBeds'])
    urbanHospitals=int(beds_df['urbanHospitals'])
    urbanBeds=int(beds_df['urbanBeds'])
    totalHospitals=int(beds_df['totalHospitals'])
    totalBeds=int(beds_df['totalBeds'])
    hospital_beds['ruralHospitals']="{:,}".format(ruralHospitals,",")
    hospital_beds['ruralBeds']="{:,}".format(ruralBeds,",")
    hospital_beds['urbanHospitals']="{:,}".format(urbanHospitals,",")
    hospital_beds['urbanBeds']="{:,}".format(urbanBeds,",")
    hospital_beds['totalHospitals']="{:,}".format(totalHospitals,",")
    hospital_beds['totalBeds']="{:,}".format(totalBeds,",")



    medical_colleges=cowin.get_medical_colleges()
    medical_colleges_data=[]
    for colleges in medical_colleges['data']['medicalColleges']:
        temp={}
        temp['state']=colleges['state']
        temp['name']=colleges['name']
        temp['city']=colleges['city']
        temp['ownership']=colleges['ownership']
        temp['admissionCapacity']=colleges['admissionCapacity']
        temp['hospitalBeds']=colleges['hospitalBeds']
        medical_colleges_data.append(temp)
    ind=0
    medical_colleges_data_df={}
    for d_df in medical_colleges_data:
        medical_colleges_data_df[ind]=d_df
        ind+=1

    df_medical_colleges_data=pd.DataFrame.from_dict(medical_colleges_data_df, orient='index')
    modified_state_name=""
    if state_name=="Andaman and Nicobar Islands":
        modified_state_name="A & N Islands"
    else:
        modified_state_name=state_name.replace(" and "," & ")
    print(modified_state_name)
    medical_colleges_df=df_medical_colleges_data.loc[df_medical_colleges_data['state'] == modified_state_name]
    medical_colleges_final=[]

    for index,row in medical_colleges_df.iterrows():
        temp={}
        admissionCapacity=row['admissionCapacity']
        hospitalBeds=row['hospitalBeds']
        temp['state']=row['state']
        temp['name']=row['name']
        temp['city']=row['city']
        temp['ownership']=row['ownership']
        temp['admissionCapacity']=admissionCapacity
        temp['hospitalBeds']=hospitalBeds
        medical_colleges_final.append(temp)



    contact_details=cowin.get_contacts()
    contact_data=""
    for contact in contact_details['data']['contacts']['regional']:
        if contact['loc'] ==state_name:
            contact_data=contact['number']



    # graphJSON = json.dumps(gdata, cls=plotly.utils.PlotlyJSONEncoder)
    data['status']="success"
    data['payload']=data_dict
    data['barchart']=gdata
    data['linechart']=ldata
    data['state_name']=state_name
    data['sample_graph']=tgdata
    data['cases']=case_state
    data['beds']=hospital_beds
    data['medical_colleges']=medical_colleges_final
    data['contact']=contact_data
    # data['barchart']=barchartfig.show()
    return jsonify(data)
@app.route('/vaccineavailability')
def vaccineavailability():
    states = cowin.get_states()
    today=datetime.today()
    locator = Nominatim(user_agent="myGeocoder")
    g = geocoder.ip('me')
    # print(g)
    coordinates=",".join([str(x) for x in g.latlng])
    location = locator.reverse(coordinates)
    notifications=cowin.get_notifications()
    # print(notifications['data'])
    cases=cowin.get_latest_case_counts()
    hospital_beds=cowin.get_hospital_beds()
    contact=cowin.get_contacts()

    # print(cases)


    data=dict()
    # print(states)
    data['states']=states['states']
    data['date']=today
    data['geolocation']=location.raw
    data['notifications']=notifications['data']
    data['case_summary']=cases['data']['summary']
    data['hospital_beds_summary']=hospital_beds['data']['summary']
    data['contact']=contact['data']['contacts']['primary']


    return render_template('coviddash.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)

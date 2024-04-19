class Constants:
    base_url = "https://cdn-api.co-vin.in/api/v2"
    covid_rest_url="https://api.rootnet.in/covid19-in"

    states_list_url = f"{base_url}/admin/location/states"
    districts_list_url = f"{base_url}/admin/location/districts"

    availability_by_pin_code_url = f"{base_url}/appointment/sessions/public/calendarByPin"
    availability_by_district_url = f"{base_url}/appointment/sessions/public/calendarByDistrict"

    case_counts_latest = f"{covid_rest_url}/stats/latest"
    case_counts_history = f"{covid_rest_url}/stats/history"
    testing_counts_latest = f"{covid_rest_url}/stats/testing/latest"
    testing_counts_history = f"{covid_rest_url}/stats/testing/history"
    hospitals_beds = f"{covid_rest_url}/hospitals/beds"
    hospitals_medical_colleges = f"{covid_rest_url}/hospitals/medical-colleges"
    helpline_contacts = f"{covid_rest_url}/contacts"
    notifications = f"{covid_rest_url}/notifications"
    DD_MM_YYYY = "%d-%m-%Y"

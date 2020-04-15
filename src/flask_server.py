import pandas as pd

# Get last update 
from flask import Flask
from flask import abort, make_response

app = Flask(__name__)

@app.route('/get_full_dataset', methods=['GET'])
def get_full_dataset():
    """ Returns full dataset
    """    

    url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
    
    df = pd.read_csv(url, error_bad_lines=False)

    return df.to_json()

@app.route('/get_last_update')
def get_last_update():
    """ Returns last update of the dataset
    """    
    url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
    df = pd.read_csv(url, error_bad_lines=False)
    last_date = df.iloc[-1]
    return last_date.to_json()

@app.route('/get_entry/<string:date>', methods=['GET'])
def get_date_entry(date):
    """ Returns entry from a specific date
    """    
    url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
    
    df = pd.read_csv(url, error_bad_lines=False)
    
    entry_of_interest = df.loc[df.data == date]

    if entry_of_interest.shape[0] == 0:
        return make_response('Could not find the desired date', 404)

    return entry_of_interest.to_json()

@app.route('/get_entry/<string:date_1>_until_<string:date_2>', methods=['GET'])
def get_batch_of_updates(date_1, date_2):
    """ Returns entry from an interval of dates
    """  

    url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
    
    df = pd.read_csv(url, error_bad_lines=False)
    
    entry_date_1 = df.loc[df.data == date_1]
    entry_date_2 = df.loc[df.data == date_2]

    print(entry_date_1.shape,  entry_date_2.shape)

    if (entry_date_1.shape[0] == 0) or (entry_date_2.shape[0] == 0):
        return make_response('One of the dates are wrong', 404)

    entry_of_interest = df.iloc[entry_date_1.index[0]: entry_date_2.index[0], :]

    return entry_of_interest.to_json()

@app.route('/get_status/', methods=['GET'])
def get_status():
    """ Returns the status of server
    """  

    status_code = make_response('Server_OK', 200)

    return status_code

if __name__ == '__main__':
    app.run(port=5001, threaded=True, host='0.0.0.0')
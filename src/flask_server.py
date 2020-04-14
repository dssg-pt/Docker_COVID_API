import pandas as pd

# Get last update 
from flask import Flask
from flask import abort

app = Flask(__name__)


@app.route('/get_last_update')
def get_last_update():
    url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
    df = pd.read_csv(url, error_bad_lines=False)
    last_date = df.iloc[-1]
    return last_date.to_json()

@app.route('/get_entry/<string:date>', methods=['GET'])
def get_task(date):
    url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
    
    df = pd.read_csv(url, error_bad_lines=False)
    
    entry_of_interest = df.loc[df.data == date]

    if entry_of_interest.shape[0] == 0:
        abort(404)

    return entry_of_interest.to_json()

if __name__ == '__main__':
    app.run(port=5001, threaded=True, host='0.0.0.0')
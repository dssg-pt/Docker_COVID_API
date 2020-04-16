import pandas as pd

# Get last update 
from flask import Flask
from flask import abort, make_response, request, Response
from flask_restplus import Api, Resource, fields

flask_app = Flask(__name__)
app = Api(app = flask_app,
          version = "1.0", 
		  title = "COVID-19 REST API Portugal", 
		  description = "DSSG Portugal / VOST REST API para fazer Download dos dados da DGS correspondentes ao COVID-19")

name_space = app.namespace('Requests', description='Request disponíveis até à data')

@name_space.route('/get_last_update')
class GetLastUpdate(Resource):

    def get(self):
        """ Returns the last updated entry

            Returns a dict with the following fomat: {index -> {column -> value}}

            PT: Retorna o último update do dataset em formato JSON.

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}
    
        """
        url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
        df = pd.read_csv(url, error_bad_lines=False)
        last_date = df.iloc[-1]

        resp = Response(response=last_date.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)


@name_space.route('/get_full_dataset')
class GetFullDataset(Resource):

    def get(self):
        """ Returns the full dataset in a JSON format.

            Returns a dict with the following fomat: {index -> {column -> value}}

            PT: Retorna o dataset inteiro em formato JSON. 

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}

        """
        
        url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
        df = pd.read_csv(url, error_bad_lines=False)

        resp = Response(response=df.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)

@name_space.route('/get_entry/<string:date>')
class GetSpecificDate(Resource):
    
    @app.doc(responses={ 200: 'OK', 500: 'Requested data was not found.' }, 
			 params={ 'date': 'Specify the date in the format dd-mm-yyyy' })
    def get(self, date):
        """ Returns the update of a specific date

            Should be asked in the following format: dd-mm-yyyy. For example: /get_entry/01-04-2020

            Returns a dict with the following fomat: {index -> {column -> value}}

            PT: Retorna o update para uma data específica

            Deve ser feito no formato dd-mm-yyyy. Por exemplo /get_entry/01-04-2020

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}

        """    

        url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
        
        df = pd.read_csv(url, error_bad_lines=False)
        
        entry_of_interest = df.loc[df.data == date]

        if entry_of_interest.shape[0] == 0:
            name_space.abort(500, status = "Requested data was not found.", statusCode = "500")

        resp = Response(response=entry_of_interest.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)

@name_space.route('/get_entry/<string:date_1>_until_<string:date_2>')
class GetRangeOfDates(Resource):
    
    @app.doc(responses={ 200: 'OK', 500: 'At least one of the dates was not found.' }, 
			 params={ 'date_1': 'Specify the first date in the format dd-mm-yyyy',
                      'date_2': 'Specify the first date in the format dd-mm-yyyy',})
    def get(self, date_1, date_2):
        """ Returns the updates for a specific range of dates

            Should be asked in the following format: dd-mm-yyyy. For example: /get_entry/01-04-2020_until_05-04-2020

            Returns a dict with the following fomat: {index -> {column -> value}}

            PT: Retorna o update para um intervalo de dados específico.

            Deve ser feito no formato dd-mm-yyyy. Por exemplo /get_entry/01-04-2020_until_03_04_2020

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}

        """    

        url = 'https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv'
        
        df = pd.read_csv(url, error_bad_lines=False)
        
        entry_date_1 = df.loc[df.data == date_1]
        entry_date_2 = df.loc[df.data == date_2]

        if (entry_date_1.shape[0] == 0) or (entry_date_2.shape[0] == 0):
            return make_response('At least one of the dates was not found.', 404)

        entry_of_interest = df.iloc[entry_date_1.index[0]: entry_date_2.index[0], :]

        resp = Response(response=entry_of_interest.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)


@name_space.route("/get_status")
class GetStatus(Resource):
    @app.doc(responses={ 200: 'Server is OK'})

    def get(self):
        """ Returns the state of the API

            PT: Retorna o estado da API
        """

        return {
			"status": "Server is OK"
		}

if __name__ == '__main__':
    flask_app.run(port=5001, threaded=True, host='0.0.0.0')

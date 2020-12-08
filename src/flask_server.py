import pandas as pd

# Get last update 
from flask import Flask
from flask import abort, make_response, request, Response
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

flask_app = Flask(__name__)

app = Api(app = flask_app,
          version = "1.0", 
		  title = "COVID-19 REST API Portugal", 
		  description = "DSSG Portugal / VOST REST API for downloading DGS COVID-19 data",
          license='MIT License',
          license_url='https://github.com/dssg-pt/Docker_COVID_API/blob/master/LICENSE')

flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

name_space = app.namespace('Requests', description='Available Requests')

@name_space.route('/get_last_update')
class GetLastUpdate(Resource):

    def get(self):
        """ Returns the last updated entry

            Returns a dict with the following format: {index -> {column -> value}}

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

            Returns a dict with the following format: {index -> {column -> value}}

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

            Returns a dict with the following format: {index -> {column -> value}}

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

            Returns a dict with the following format: {index -> {column -> value}}

            PT: Retorna o update para um intervalo de dados específico.

            Deve ser feito no formato dd-mm-yyyy. Por exemplo /get_entry/01-04-2020_until_03-04-2020

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
        
## COUNTIES 

@name_space.route('/get_last_update_counties')
class GetLastUpdateCounties(Resource):

    def get(self):
        """ Returns the last updated entry for all counties

            Returns a dict with the following format: {index -> {column -> value}}

            PT: Retorna o último update do dataset dos concelhos em formato JSON.

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}
    
        """
        url = 'https://github.com/dssg-pt/covid19pt-data/blob/master/data_concelhos_new.csv'
        df = pd.read_csv(url, error_bad_lines=False)
        last_date = df.iloc[-1]

        resp = Response(response=last_date.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)

@name_space.route('/get_last_update_specific_county/<string:county>')
class GetLastUpdateSpecificCounty(Resource):

    def get(self, county):
        """ Returns the last updated entry for a specific county.

            Returns a dict with the following format: {index -> {column -> value}}

            PT: Retorna o último update do dataset dos concelhos em formato JSON.

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}
    
        """
        url = 'https://github.com/dssg-pt/covid19pt-data/blob/master/data_concelhos_new.csv'
        df = pd.read_csv(url, error_bad_lines=False)
        last_date = df.iloc[-1]
        specific_county = last_date[last_date['concelho'] == county.upper()]
        
        if len(specific_county) == 0:
            name_space.abort(500, status = "Requested county was not found.", statusCode = "500")

        resp = Response(response=specific_county.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)

@name_space.route('/get_entry_counties/<string:date>')
class GetSpecificDateCounties(Resource):
    
    @app.doc(responses={ 200: 'OK', 500: 'Requested data was not found.' }, 
			 params={ 'date': 'Specify the date in the format dd-mm-yyyy' })
    def get(self, date):
        """ Returns the update of a specific date for the counties dataset.

            Should be asked in the following format: dd-mm-yyyy. For example: /get_entry_counties/01-04-2020

            Returns a dict with the following format: {index -> {column -> value}}

            PT: Retorna o update para uma data específica para o dataset dos concelhos

            Deve ser feito no formato dd-mm-yyyy. Por exemplo /get_entry_counties/01-04-2020

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}

        """    
        url = 'https://github.com/dssg-pt/covid19pt-data/blob/master/data_concelhos_new.csv'
        
        df = pd.read_csv(url, error_bad_lines=False)
        
        entry_of_interest = df.loc[df.data == date]

        if entry_of_interest.shape[0] == 0:
            name_space.abort(500, status = "Requested data was not found.", statusCode = "500")

        resp = Response(response=entry_of_interest.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)

@name_space.route('/get_entry_county/<string:date>_<string:county>')
class GetSpecificDateSpecificCounty(Resource):
    
    @app.doc(responses={ 200: 'OK', 500: 'Requested data was not found.', 
                         501: 'Requested county was not found.' }, 
			 params={ 'date': 'Specify the date in the format dd-mm-yyyy',
                      'county': 'Specify the county in UPPERCASE'})
    def get(self, date, county):
        """ Returns the update of a specific date for the desired county.

            Should be asked in the following format: dd-mm-yyyy_UPPERCASECOUNTY. For example: /get_entry_county/01-04-2020_GONDOMAR

            Returns a dict with the following format: {index -> {column -> value}}

            PT: Retorna o update para uma data específica para um concelho específico.

            Deve ser feito no formato dd-mm-yyyy_CONCELHO. Por exemplo /get_entry_county/01-04-2020_GONDOMAR

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}

        """    

        url = 'https://github.com/dssg-pt/covid19pt-data/blob/master/data_concelhos_new.csv'
        
        df = pd.read_csv(url, error_bad_lines=False)
        
        entry_of_interest = df.loc[df.data == date]

        if len(entry_of_interest) == 0:
            name_space.abort(500, status = "Requested county was not found.", statusCode = "500")

        if entry_of_interest.shape[0] == 0:
            name_space.abort(501, status = "Requested data was not found.", statusCode = "500")

        resp = Response(response=entry_of_interest.to_json(),
            status=200,
            mimetype="application/json")
        return(resp)

@name_space.route('/get_entry_counties/<string:date_1>_until_<string:date_2>')
class GetRangeOfDatesCounties(Resource):
    
    @app.doc(responses={ 200: 'OK', 500: 'At least one of the dates was not found.' }, 
			 params={ 'date_1': 'Specify the first date in the format dd-mm-yyyy',
                      'date_2': 'Specify the first date in the format dd-mm-yyyy',})
    def get(self, date_1, date_2):
        """ Returns the updates for a specific range of dates for the counties dataset

            Should be asked in the following format: dd-mm-yyyy. For example: /get_entry/01-04-2020_until_05-04-2020

            Returns a dict with the following format: {index -> {column -> value}}

            PT: Retorna o update para um intervalo de dados específico para o dataset dos concelhos

            Deve ser feito no formato dd-mm-yyyy. Por exemplo /get_entry/01-04-2020_until_03-04-2020

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}

        """    

        url = 'https://github.com/dssg-pt/covid19pt-data/blob/master/data_concelhos_new.csv'
        
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

@name_space.route('/get_entry_county/<string:date_1>_until_<string:date_2>_<string:county>')
class GetRangeOfDatesSpecificCounty(Resource):
    
    @app.doc(responses={ 200: 'OK', 500: 'At least one of the dates was not found.',
                         501: 'Requested county was not found.' }, 
			 params={ 'date_1': 'Specify the first date in the format dd-mm-yyyy',
                      'date_2': 'Specify the first date in the format dd-mm-yyyy',
                      'county': 'Specify the county in UPPERCASE'})
    def get(self, date_1, date_2, county):
        """ Returns the updates for a specific range of dates for the counties dataset

            Should be asked in the following format: dd-mm-yyyy. The county should be in UPPERCASE. For example: /get_entry/01-04-2020_until_05-04-2020_GONDOMAR

            Returns a dict with the following format: {index -> {column -> value}}

            PT: Retorna o update para um intervalo de dados específico para o dataset dos concelhos

            Deve ser feito no formato dd-mm-yyyy. O concelho deve ser pedido em maiúsculas. Por exemplo /get_entry/01-04-2020_until_03-04-2020_GONDOMAR

            Retorna um dicionário em formato JSON do tipo: {index -> {column -> value}}
        """    

        url = 'https://github.com/dssg-pt/covid19pt-data/blob/master/data_concelhos_new.csv'
        
        df = pd.read_csv(url, error_bad_lines=False)
        
        entry_date_1 = df.loc[df.data == date_1]
        entry_date_2 = df.loc[df.data == date_2]

        if (entry_date_1.shape[0] == 0) or (entry_date_2.shape[0] == 0):
            return make_response('At least one of the dates was not found.', 404)

        entry_of_interest = df.iloc[entry_date_1.index[0]: entry_date_2.index[0], :]
        entry_of_interest = entry_of_interest[county]
        
        if len(entry_of_interest) == 0:
            name_space.abort(500, status = "Requested county was not found.", statusCode = "500")

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
    flask_app.run(host='0.0.0.0')

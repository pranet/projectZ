from flask import Flask, request, jsonify, json
from flask_cors import CORS
from data_sources import ChromePluginDataSource
from item_finder import ItemFinder
from models import Query
import configparser
from metadata_providers_factory import MetadataProvidersFactory


app = Flask(__name__)
CORS(app)

def get_metadata_provider():
    config = configparser.ConfigParser()
    config.read('resources/application.properties')
    developer_key = config['DEFAULT']['developer_key']
    sheet_id = config['DEFAULT']['sheet_id']
    return MetadataProvidersFactory.get_google_sheets_metadata_provider(developer_key=developer_key, sheet_id=sheet_id)

@app.route('/processData/', methods=['POST'])
def processData():
    data_source = ChromePluginDataSource(request.json)
    item_finder = ItemFinder(data_source=data_source, queries=metadata_provider.get_all_queries())
    result = item_finder.find_anomalies()
    return jsonify(list(map(lambda x: str(x), result)))

if __name__ == '__main__':
    metadata_provider = get_metadata_provider()
    app.run(debug=True)

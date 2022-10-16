from flask import Flask, request, jsonify

from APIServer import APIServer

from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
_apiServer = APIServer()

CORS(app)


@app.route('/getCompany', methods=['GET'])
def read_one():
    company_key = request.args.get('name')

    data_one = _apiServer.get_company(company_key)
    return data_one


@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        all_companies : Return all documents.
    """
    data = _apiServer.get_companies()
    return data


@app.route('/test', methods=['GET'])
def read_test():
    """
        read() : Fetches documents from Firestore collection as JSON.
        all_todos : Return all documents.
    """
    data = _apiServer.get_companies_test()
    return data


@app.route('/invest', methods=['GET'])
def invest():
    # need json or specific data to update values
    confirmation = request.args.get("confirmation")
    num_shares_bought = request.args.get("sharesBought")
    dollar_amount = request.args.get("dollarAmount")
    hash_investor = request.args.get("investorKey")
    company_key = request.args.get("companyKey")

    # _apiServer = APIServer()

    print(confirmation, num_shares_bought, dollar_amount, hash_investor, company_key)

    update_response = _apiServer.update_company_info(int(confirmation), int(num_shares_bought),
                                                     int(dollar_amount), hash_investor, company_key)
    print(update_response)
    if update_response == 200:
        return {"status": "Success"}
    return {"status": "Failure"}


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=8080)

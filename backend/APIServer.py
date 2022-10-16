import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from Company import Company

cred_path = os.path.join(os.getcwd(), "HackHarvardAuth.json")
cred = credentials.Certificate(cred_path)
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://hackharvard-ba0b8.firebaseio.com/'})
company_ref = db.reference('/companies')
investor_ref = db.reference('/investors')


def put_to_database_company(json_res, key):
    path = '/companies/' + str(key)
    # puttAttempt = app.put('/companies', str(key), jsonRes)
    put_attempt = db.reference(path).set(json_res)
    print("")
    print(put_attempt)
    print("")


def put_to_database_investor(json_res, key):
    put_attempt = app.put('/investors', str(key), json_res)
    print("")
    print(put_attempt)
    print("")


def get_companies():
    # data = app.get('/companies', '')
    data = company_ref.get()
    return data


def get_company(key):
    path = '/companies/' + str(key)
    # data = app.get(path, '')
    data = db.reference(path).get()
    print("")
    print("Company Retrieved: ")
    print("")
    return data


def get_company_test():
    # data = [doc.to_dict() for doc in company_ref.stream()]
    data = company_ref.get()
    print(data)
    return data


def get_investor(key):
    path = '/investors/' + str(key)
    data = app.get(path, '')
    print("")
    print("Investor Retrieved: ")
    print("")
    print(data)
    return data


class APIServer:

    def __init__(self):
        # Just for logging purposes
        self.numCalls = 0

    def get_companies(self):
        data = get_companies()
        return data

    def get_companies_test(self):
        data = get_company_test()
        return data

    def get_company(self, company_key):
        data = get_company(company_key)
        return data

    def get_investor(self, investor_key):
        data = get_investor(investor_key)
        return data

    def update_investor_info(self, confirmation_code, num_shares_bought, dollar_amount, investor_key, company_key):

        if confirmation_code == 1:

            # Step 1: retrieve user from firebase using key
            investor = self.get_investor(investor_key)

            print(investor)

            # Investor portfolio:
            # companies_invested = {'Company A key': 'X shares worth Y', 'Company B key': 'X2 shares worth Y2'}
            # currentDollarPortfolio = investor.dollarPortfolio
            # key = str(companyKey)
            # if key in currentDollarPortfolio:

            # currentDollarPortfolio[str(companyKey)] = (str(numSharesBought) + " shares bought worth " + str(dollarAmount) + " dollars.")

            # Update total number of shares he owns in our platform
            current_number_shares_owned = investor['sharesOwn']
            updated_shares_own = current_number_shares_owned + num_shares_bought

            # Update total dollar amount invested in our platform
            dollars_invested_so_far = investor['dollarsInvested']
            updated_dollars_invested = dollars_invested_so_far + dollar_amount

            # update share holdings of each company
            # companyHoldings: {Company A: X shares, Company B: Y shares}
            company_holdings = investor['companyHoldings']

            key = str(company_key)
            current_company_holdings = 0
            if key in company_holdings:
                current_company_holdings = company_holdings[key]
            company_holdings[key] = num_shares_bought + current_company_holdings

            # Create new investor object
            # investorUpdated = Investor(investorKey, updatedSharesOwn, dollarsInvestedSoFar, companyHoldings)
            # putToDatabaseInvestor(investorUpdated)

        return None

    def update_company_info(self, confirmation_code, num_shares_bought, dollar_amount, hash_investor, company_key):

        # Codes:
        # 1: Successful NFT Purchase
        # 0: Unsuccessful NFT Purchase
        # Anything else: unknown error (HTTP probably)

        # If NFT Purchase successful, do the following:

        if (confirmation_code == 1):

            # Step 1: retrieve company from firebase using hash
            company = get_company(company_key)

            print(company)

            initial_total_shares_outstanding = company['totalSharesInitially']

            # Update shares outstanding
            current_shares_outstanding = company['sharesOutstanding']
            updated_shares_outstanding = current_shares_outstanding - num_shares_bought

            # Update total number of shares bough so far
            current_shares_bought = company['sharesBought']
            updated_shares_bought = current_shares_bought + num_shares_bought

            # update amount raised
            current_amount_raised = company['amountRaised']
            updated_amount_raised = current_amount_raised + dollar_amount

            # Add current investor
            list_current_investors = company['investors'].strip('][').split(', ')  # should return a list
            object_investor = {
                "investorHash": str(hash_investor),
                "numShares": float(num_shares_bought),
                "dollarValue": float(dollar_amount)
            }
            updated_investors = list_current_investors.append(object_investor)

            # Amount remaining to raise
            total_amount_raising = company['totalAmountRaising']
            amount_remaining_to_raise = total_amount_raising - updated_amount_raised

            # Create new object: not as efficient as updating but works better due to pointers and memory concerns
            # Order:

            # Name
            # Valuation
            # Percent of equity available to investors

            # Total shares initially available
            # Shares outstanding (remaining)
            # Shares Bought

            # Total amount to raise
            # Amount reaised
            # Amount remaining to Raise

            # List of investors

            # Link to landing page
            # Progress report
            # Additional info

            # update with put object (using company hash as key)

            company_updated = Company(company['name'], company['valuation'], company['percentEquity'],
                                      company['totalSharesInitially'], updated_shares_outstanding,
                                      updated_shares_bought,
                                      company['totalAmountRaising'], updated_amount_raised, amount_remaining_to_raise,
                                      updated_investors, company['landingPage'], None, None
                                      ).get_JSON()

            put_to_database_company(company_updated, company_key)

            return 200

        # If confirmation code is anything else
        elif confirmation_code == 0:
            # Or return any other error message to client
            print("Unsuccessful NFT purchase. No update made to company data. ")
            return 404


if __name__ == "__main__":
    _apiServer = APIServer()
    _companyMinerva = Company("Minerva", 5000000, 10, 100, 100, 0, 500000, 0, 500000, ["Kyle Berg, Chris Klaus"],
                              "https://minerva-landing-6410d.web.app/", None, None)
    # print("here")
    companyJSONMinerva = _companyMinerva.get_JSON()
    put_to_database_company(companyJSONMinerva, "minervaHash")

    _companyBuble = Company("Bubbl", 5000000, 8, 200, 180, 20, 400000, 40000, 160000, ["Neo"],
                             "https://linktr.ee/usebubbl?utm_source=linktree_profile_share&ltsid=e144875f-4359-45fb"
                             "-b3b5-677b16c82e14",
                            None, None)
    companyJSONBuble = _companyBuble.get_JSON()
    put_to_database_company(companyJSONBuble, "bubleHash")

    _companyCruise = Company("Cruise", 10000000, 5, 500, 50, 450, 500000, 450000, 50000, ["Y Combinator"],
                             "https://getcruise.com/", None, None)
    companyJSONCruise = _companyCruise.get_JSON()
    put_to_database_company(companyJSONCruise, "cruiseHash")

    # retrieve data
    dataMinerva = _apiServer.get_company("minervaHash")
    print("Data Retrieved for Minerva")
    print(dataMinerva)
    print("")

    dataBuble = get_company("bubleHash")
    print("Data Retrieved for Buble")
    print(dataBuble)

    dataCruise = get_company("cruiseHash")
    print("Data Retrieved for Cruise")
    print(dataCruise)

    print("")
    print("Done")
    print("")

    # All companies
    dataCompanies = _apiServer.get_companies()
    print("Data of all companies")
    print(dataCompanies)
    print("")

    print("Investor")
    investor = {
        "key": "Javi",
        "sharesOwn": 0,
        "dollarsInvested": 0,
        "companyHoldings": {
            "no companies so far": 0,
        }
    }

    put_to_database_investor(investor, "Javi")

    dataInvestor = _apiServer.get_investor("Javi")
    print("Data Investor")
    print(dataInvestor)

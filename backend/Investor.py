# Mimics a Real World Investor

class Investor:

    # Investor Level --> can depend on the amountInvestment,income and other factors
    def __init__(self, name, email, amt_investment, wallet_hash, company_list, investor_level):
        self.__init__(self, name, email, amt_investment, wallet_hash, company_list)
        self.investorLevel = investor_level

    # Default constructor to construct an Investor
    def __init__(self, name, email, amt_investment, wallet_hash, company_list):
        self.name = name
        self.email = email
        self.amtInvestment = amt_investment
        self.investorHash = hash(email)
        self.walletHash = wallet_hash
        self.companyList = company_list

    # Differentiating investors basis unique emailId

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.email == other.email

    def __hash__(self):
        return hash(self.email)

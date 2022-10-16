# Assumptions:
# Can only buy entire NFTs/shares at a time. No percentage or fraction of a share/NFT

import json


class Company:

    def __init__(self, name, valuation, percent_equity, total_shares_initially,
                 shares_outstanding, shares_bought, total_amount_raising, amount_raised,
                 amount_remaining_to_raise, investors, landing_page, progress_report,
                 additional_info):
        self.name = name
        self.valuation = valuation
        self.percentEquity = percent_equity
        self.totalSharesInitially = total_shares_initially
        self.sharesOutstanding = shares_outstanding
        self.sharesBought = shares_bought
        self.totalAmountRaising = total_amount_raising
        self.amountRaised = amount_raised
        self.amountRemainingToRaise = amount_remaining_to_raise
        self.investors = investors
        self.landingPage = landing_page
        self.progressReport = progress_report
        self.additionalInfo = additional_info

    def get_JSON(self):
        list_investors = json.dumps(self.investors)
        json_object = {
            "name": str(self.name),
            "valuation": float(self.valuation),
            "percentEquity": float(self.percentEquity),
            "totalSharesInitially": int(self.totalSharesInitially),
            "sharesOutstanding": int(self.sharesOutstanding),
            "sharesBought": int(self.sharesBought),
            "totalAmountRaising": float(self.totalAmountRaising),
            "amountRaised": float(self.amountRaised),
            "amountRemainingToRaise": float(self.amountRemainingToRaise),
            "investors": list_investors,
            "landingPage": str(self.landingPage)
            # Do not include progress report and additional info for now
        }
        return json_object

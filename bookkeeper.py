import pandas as pd

class Bookkeeper:

    def __init__(self, name):
        columns = ["account", "balance", "date", "note", "class", "amount"]
        self.df = pd.DataFrame(columns=columns) #Each row corresponds to a transaction
        self.name = name


    def add_transactions(self, new_df):
        """
        Add transactions from other dataframe

        
        """
        pass

    def month_summary(self, month):
        pass

    def classify_transaction(self):
        pass



    
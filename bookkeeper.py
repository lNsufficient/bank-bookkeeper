import pandas as pd

class Bookkeeper:

    def __init__(self, name):
        self.columns = ["account", "balance", "date", "note", "class", "amount"]
        self.df = pd.DataFrame(columns=self.columns) #Each row corresponds to a transaction
        self.name = name


    def add_transactions(self, new_df):
        """
        Add transactions from other dataframe

        
        """
        self.df = self.df.append(new_df)

    def summary(self, df=None):
        if df is None:
            df = self.df
        print(df.head())
        summary = {}
        neg_amount = df['amount'] < 0
        transfer_rows = df["class"].str.lower().isin(["transfer"])
        summary["transfer_positive"] = df.loc[transfer_rows & ~neg_amount, "amount"].sum()
        summary["transfer_negative"] = df.loc[transfer_rows & neg_amount, "amount"].sum()
        summary["transfer_diff"] = summary["transfer_positive"] + summary["transfer_negative"]
        summary['expenditure'] = df.loc[~transfer_rows & neg_amount, 'amount'].sum()
        summary['income'] = df.loc[~transfer_rows & ~neg_amount, 'amount'].sum()
        summary["ALL_OUT"] = df.loc[neg_amount, "amount"].sum()
        summary["ALL_IN"] = df.loc[~neg_amount, "amount"].sum()
        summary["ALL_SUM"] = df["amount"].sum()
        print(summary)

    def month_summary(self, month):
        pass #call for summary() for dates within range. 

    def classify_transaction(self, x):
        note_lower = x['note'].lower()
        if "överföring" in note_lower:
            return "transfer"
        if "swish" in note_lower:
            return "transfer"
        return "unknown"

    def classify_transactions(self, df=None):
        if df is None:
            df = self.df
        df["class"] = df.apply(self.classify_transaction, axis="columns")

    def filter_out_matching_transfers(self, df=None):
        if df is None:
            df = self.df
        #use columns: target, source, match transfers.

class ImportCSVBank(Bookkeeper):
    import_columns = []
    date_columns = [] #Columns to find datettime.
    column_rename_dict = {
    }

    separator = ","
    thousands = " " #Thousands separator
    decimal = "," #Decimal separator
    quotechar = '"'
    
    encoding = "utf-8"

    def read_csv(self, csv_path):
        return pd.read_csv(
            csv_path, 
            delimiter=self.separator, 
            index_col=False,
            header=1,
            parse_dates=self.date_columns,
            decimal=self.decimal,
            quotechar=self.quotechar,
            encoding=self.encoding,
            )

class Swedbank(ImportCSVBank):
    separator = ','
    import_columns = "Radnummer,Clearingnummer,Kontonummer,Produkt,Valuta,Bokföringsdag,Transaktionsdag,Valutadag,Referens,Beskrivning,Belopp,Bokfört saldo"
    import_columns = import_columns.split(separator)
    date_columns = ["Bokföringsdag","Transaktionsdag","Valutadag"] #Columns to find datettime.
    thousands = "" #Thousands separator
    decimal = "." #Decimal separator
    quotechar = '"'
    column_rename_dict = {
        "Bokfört saldo":"balance", 
        "Bokföringsdag":"date",  
        "Belopp":"amount"
    }
    encoding = "ISO-8859-1"

    def get_account(self, x):
        return str(x["Clearingnummer"]) + ", " + str(x["Kontonummer"])

    def get_note(self, x):
        note = x["Beskrivning"]
        if x["Referens"] not in note:
            note = note + ", ref: " + x["Referens"]
        return note 

    def import_transactions(self, csv_path):
        new_df = self.read_csv(csv_path)
        new_df["account"] = new_df.apply(func=self.get_account, axis = "columns")
        new_df["note"] = new_df.apply(func=self.get_note, axis="columns")
        new_df.rename(columns=self.column_rename_dict, inplace=True)
        new_df_columns = [e for e in self.columns if e in new_df.columns]
        new_df = new_df[new_df_columns]
        self.classify_transactions(new_df)
        self.latest_import_df = new_df
        return self.latest_import_df
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
        pass


    def month_summary(self, month):
        pass

    def classify_transaction(self):
        pass

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
        self.latest_import_df = new_df
        return self.latest_import_df
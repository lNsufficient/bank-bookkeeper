from sys import argv
import bookkeeper as bk

if __name__ == "__main__":
    transaction_account = bk.Swedbank("privatkonto")
    transaction_account.import_transactions(argv[1])
    print(transaction_account.latest_import_df.head())
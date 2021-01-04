from sys import argv
import bookkeeper as bk

if __name__ == "__main__":
    bookkeeper = bk.Bookkeeper("AllAccounts")
    transaction_account = bk.Swedbank("privatkonto")
    privatkonto_df = transaction_account.import_transactions(argv[1])
    bookkeeper.add_transactions(privatkonto_df)

    e_account = bk.Swedbank("e-konto")
    e_df = e_account.import_transactions(argv[2])
    bookkeeper.add_transactions(e_df)

    bookkeeper.summary()
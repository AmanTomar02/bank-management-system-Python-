import streamlit as st
from bank import Bank

bank = Bank()
st.title("🏦 Secure Bank App")

# menu = st.sidebar.radio("Menu", [
#     "Create Account", "Login"
# ])

menu = st.sidebar.radio("Menu", [
    "Create Account", "Login", "Admin"
])



# CREATE ACCOUNT
if menu == "Create Account":
    name = st.text_input("Name")
    age = st.number_input("Age", 18, 100)
    email = st.text_input("Email")
    pin = st.text_input("Set 4-digit PIN", type="password")

    if st.button("Create"):
        res = bank.create_account(name, age, email, int(pin))
        if isinstance(res, dict):
            st.success("Account Created ✅")
            st.write("Account No:", res["Account_Number"])
        else:
            st.error(res)


# LOGIN
elif menu == "Login":
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):
        user = bank.get_details(acc, int(pin))

        if user:
            st.success(f"Welcome {user['name']} 👋")

            option = st.selectbox("Choose Action", [
                "Deposit", "Withdraw", "View Account", "History", "Delete Account"
            ])

            # DEPOSIT
            if option == "Deposit":
                amt = st.number_input("Amount", 1, 10000)
                if st.button("Deposit Now"):
                    st.info(bank.deposit(acc, int(pin), amt))

            # WITHDRAW
            if option == "Withdraw":
                amt = st.number_input("Amount", 1, user["Balance"])
                if st.button("Withdraw Now"):
                    st.info(bank.withdraw(acc, int(pin), amt))

            # VIEW
            if option == "View Account":
                st.json(user)

            # HISTORY
            if option == "History":
                st.table(user["transactions"])

            # DELETE
            if option == "Delete Account":
                if st.button("Confirm Delete"):
                    if bank.delete(acc, int(pin)):
                        st.success("Account deleted")
        else:
            st.error("Invalid login")

# ADMIN PANEL
elif menu == "Admin":
    st.subheader("Admin Login")

    user = st.text_input("Admin Username")
    pwd = st.text_input("Admin Password", type="password")

    if st.button("Login"):
        if Bank.admin_login(user, pwd):

            st.success("Welcome Admin 👑")

            admin_action = st.selectbox("Admin Actions", [
                "View Users", "Delete User",
                "Export Users", "Export Transactions"
            ])

            # VIEW USERS
            if admin_action == "View Users":
                st.table(Bank.get_all_users())

           # DELETE USER (ADMIN)
            if admin_action == "Delete User":
                acc = st.text_input("Enter Account Number to Delete")

                confirm = st.checkbox("I confirm to permanently delete this account")

                if st.button("Delete Account"):
                    if not confirm:
                        st.warning("Please confirm deletion first ⚠️")

                    elif Bank.admin_delete_user(acc):
                        st.success("User Account Deleted Successfully ✅")

                    else:
                        st.error("Account not found ❌")



            # EXPORT USERS
            if admin_action == "Export Users":
                st.success(Bank.export_users())

            # EXPORT TRANSACTIONS
            if admin_action == "Export Transactions":
                st.success(Bank.export_transactions())

        else:
            st.error("Wrong Admin Credentials")

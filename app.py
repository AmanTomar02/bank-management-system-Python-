import streamlit as st
from bank import Bank

# SESSION STATE FOR ADMIN LOGIN
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

bank = Bank()
st.title("🏦 Secure Bank App")

menu = st.sidebar.radio("Menu", [
    "Create Account", "Login", "Admin"
])


# -----------------------------------------
# CREATE ACCOUNT
# -----------------------------------------
if menu == "Create Account":
    name = st.text_input("Name")
    age = st.number_input("Age", 18, 100)
    email = st.text_input("Email")
    pin = st.text_input("Set 4-digit PIN", type="password")

    if st.button("Create Account"):
        res = bank.create_account(name, age, email, int(pin))        
        if isinstance(res, dict):
            st.success("Account Created Successfully 🎉")
            st.write("Your Account Number:", res["Account_Number"])
        else:
            st.error(res)



# -----------------------------------------
# USER LOGIN
# -----------------------------------------
elif menu == "Login":

    # INITIALIZE SESSION KEYS
    if "user_logged_in" not in st.session_state:
        st.session_state["user_logged_in"] = False

    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None

    # ---------------- USER NOT LOGGED IN ----------------
    if not st.session_state["user_logged_in"]:
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")

        if st.button("Login"):
            user = bank.get_details(acc, int(pin))

            if user:
                st.session_state["user_logged_in"] = True
                st.session_state["current_user"] = user
                st.session_state["user_acc"] = acc
                st.session_state["user_pin"] = pin

                st.success(f"Welcome {user['name']} 👋")
            else:
                st.error("Invalid login ❌")

    # ---------------- USER LOGGED IN ----------------
    else:
        user = st.session_state["current_user"]
        acc = st.session_state["user_acc"]
        pin = st.session_state["user_pin"]

        st.success(f"Welcome {user['name']} 👋")

        option = st.selectbox("Choose Action", [
            "Deposit", "Withdraw", "View Account", "History", "Delete Account"
        ])

        # DEPOSIT
        if option == "Deposit":
            amt = st.number_input("Amount", 1, 10000)
            if st.button("Deposit Now"):
                st.info(bank.deposit(acc, int(pin), amt))
                st.session_state["current_user"] = bank.get_details(acc, int(pin))

        # WITHDRAW
        if option == "Withdraw":
            amt = st.number_input("Amount", 1, user["Balance"])
            if st.button("Withdraw Now"):
                st.info(bank.withdraw(acc, int(pin), amt))
                st.session_state["current_user"] = bank.get_details(acc, int(pin))

        # VIEW ACCOUNT
        if option == "View Account":
            st.json(st.session_state["current_user"])

        # HISTORY
        if option == "History":
            st.table(user["transactions"])

        # DELETE ACCOUNT
        if option == "Delete Account":
            if st.button("Confirm Delete"):
                if bank.delete(acc, int(pin)):
                    st.success("Account deleted successfully")
                    st.session_state["user_logged_in"] = False
                    st.session_state["current_user"] = None

# -----------------------------------------
# ADMIN PANEL
# -----------------------------------------
elif menu == "Admin":
    st.subheader("Admin Login")

    # IF ADMIN NOT LOGGED IN
    if not st.session_state["admin_logged_in"]:

        user = st.text_input("Admin Username")
        pwd = st.text_input("Admin Password", type="password")

        if st.button("Login"):
            if Bank.admin_login(user, pwd):
                st.session_state["admin_logged_in"] = True
                st.success("Welcome Admin 👑")
            else:
                st.error("Wrong Admin Credentials")

    # IF ADMIN ALREADY LOGGED IN
    else:
        st.success("Welcome Admin 👑")

        if st.button("Logout"):
            st.session_state["admin_logged_in"] = False
            st.experimental_rerun()

        admin_action = st.selectbox("Admin Actions", [
            "View Users", "Delete User", 
            "Export Users", "Export Transactions"
        ])

        # VIEW USERS
        if admin_action == "View Users":
            st.table(Bank.get_all_users())

        # DELETE USER
        if admin_action == "Delete User":
            acc = st.text_input("Enter Account Number")
            confirm = st.checkbox("Confirm delete")

            if st.button("Delete User"):
                if confirm and Bank.admin_delete_user(acc):
                    st.success("User Deleted Successfully")
                else:
                    st.error("User Not Found ❌")

        # EXPORT USERS
        if admin_action == "Export Users":
            st.success(Bank.export_users())

        # EXPORT TRANSACTIONS
        if admin_action == "Export Transactions":
            st.success(Bank.export_transactions())

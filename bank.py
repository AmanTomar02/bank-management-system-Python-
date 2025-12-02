import json, random, string, hashlib, pandas as pd
from pathlib import Path
from datetime import datetime


class Bank:
    dataBase = 'data.json'
    data = []

    ADMIN_USER = "admin"
    ADMIN_PASS = "1234"

    # ---------------- LOAD DATA ----------------
    if Path(dataBase).exists():
        with open(dataBase, 'r') as fs:
            data = json.load(fs)


    # ---------------- SAVE DATA ----------------
    @classmethod
    def __update(cls):
        with open(cls.dataBase, 'w') as fs:
            json.dump(cls.data, fs, indent=4)


    # ---------------- ACCOUNT NO ----------------
    @classmethod
    def generate_account_number(cls):
        return ''.join(random.sample(string.ascii_uppercase + string.digits, 8))


    # ---------------- HASH PIN ----------------
    @staticmethod
    def hash_pin(pin):
        return hashlib.sha256(str(pin).encode()).hexdigest()


    # ---------------- ADD TRANSACTION ----------------
    @classmethod
    def add_transaction(cls, user, ttype, amount):
        # Ensure backward compatibility
        if "transactions" not in user:
            user["transactions"] = []

        user["transactions"].append({
            "type": ttype,
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


    # ---------------- FIND USER ----------------
    @classmethod
    def find_user(cls, acc, pin):
        enc = cls.hash_pin(pin)
        return next((u for u in cls.data if u["Account_Number"] == acc and u["Pin"] == enc), None)


    # ---------------- CREATE ACCOUNT ----------------
    def create_account(self, name, age, email, pin):
        if age < 18:
            return "Must be above 18"
        if len(str(pin)) != 4:
            return "PIN must be 4 digit"

        user = {
            "name": name,
            "Age": age,
            "email": email,
            "Pin": Bank.hash_pin(pin),
            "Account_Number": Bank.generate_account_number(),
            "Balance": 0,
            "transactions": []
        }

        Bank.data.append(user)
        Bank.__update()
        return user


    # ---------------- DEPOSIT ----------------
    def deposit(self, acc, pin, amount):
        user = Bank.find_user(acc, pin)

        if not user:
            return "Invalid credentials"
        if amount <= 0 or amount > 10000:
            return "Invalid amount"

        user["Balance"] += amount
        Bank.add_transaction(user, "Deposit", amount)
        Bank.__update()
        return "Deposit successful ✅"


    # ---------------- WITHDRAW ----------------
    def withdraw(self, acc, pin, amount):
        user = Bank.find_user(acc, pin)

        if not user:
            return "Invalid credentials"
        if amount > user["Balance"]:
            return "Insufficient balance"

        user["Balance"] -= amount
        Bank.add_transaction(user, "Withdraw", amount)
        Bank.__update()
        return "Withdraw successful ✅"


    # ---------------- DETAILS ----------------
    def get_details(self, acc, pin):
        user = Bank.find_user(acc, pin)

        # back-fill missing transactions if old user
        if user and "transactions" not in user:
            user["transactions"] = []
            Bank.__update()

        return user


    # ---------------- DELETE ----------------
    def delete(self, acc, pin):
        user = Bank.find_user(acc, pin)
        if not user:
            return False

        Bank.data.remove(user)
        Bank.__update()
        return True


    # ================= ADMIN METHODS =================

    @classmethod
    def admin_login(cls, user, pwd):
        return user == cls.ADMIN_USER and pwd == cls.ADMIN_PASS


    @classmethod
    def get_all_users(cls):
        return cls.data


    @classmethod
    def admin_delete_user(cls, account_number):
        for user in cls.data:
            if user["Account_Number"] == account_number:
                cls.data.remove(user)
                cls.__update()
                return True
        return False


    @classmethod
    def export_users(cls):
        df = pd.DataFrame(cls.data)

        if "Pin" in df.columns:
            df.drop(columns=["Pin"], inplace=True)

        df.to_excel("users.xlsx", index=False)
        return "User data exported as users.xlsx ✅"


    @classmethod
    def export_transactions(cls):
        rows = []

        for user in cls.data:
            # SAFE ACCESS
            transactions = user.get("transactions", [])

            for tr in transactions:
                rows.append({
                    "Name": user["name"],
                    "Account": user["Account_Number"],
                    "Type": tr["type"],
                    "Amount": tr["amount"],
                    "Time": tr["time"]
                })

        if not rows:
            return "No transactions available ❌"

        df = pd.DataFrame(rows)
        df.to_excel("transactions.xlsx", index=False)
        return "Transaction data exported ✅"




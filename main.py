# Dhurba Bhusal, Student number: 32100445
# Version update - GUI added

import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt


class HealthcareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dhurba Bhusal - 32100445 (V1.2026)")
        self.root.geometry("900x550")

        self.df = None
        self.summary = {}

        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Healthcare Worker Engagement System",
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Button(frame, text="Load Data", command=self.load_data).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Process Data", command=self.process_data).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Pie Chart", command=self.plot_pie).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Bar Chart", command=self.plot_bar).grid(row=0, column=3, padx=5)
        ttk.Button(frame, text="Dashboard", command=self.open_dashboard).grid(row=0, column=4, padx=5)
        ttk.Button(frame, text="Generate Report", command=self.generate_report).grid(row=0, column=5, padx=5)

        self.text = tk.Text(self.root, height=20)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, msg):
        self.text.insert("end", msg + "\n")
        self.text.see("end")

    # ---------------- Load Data ----------------
    def load_data(self):
        try:
            self.df = pd.read_csv("nurse_attrition.csv")
            self.log(f"Loaded {len(self.df)} records successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_data(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load data first!")
            return False
        return True

    # ---------------- Process Data ----------------
    def process_data(self):
        if not self.check_data():
            return

        df = self.df

        def stats(series):
            return {
                "min": float(series.min()),
                "max": float(series.max()),
                "avg": float(round(series.mean(), 2)),
            }

        summary = {}

        summary["Total Employees"] = len(df)
        summary["Departments"] = df["Department"].unique().tolist()
        summary["Education Levels"] = df["Education"].value_counts().to_dict()

        summary["Single Count"] = int((df["MaritalStatus"] == "Single").sum())
        summary["Divorced Count"] = int((df["MaritalStatus"] == "Divorced").sum())

        summary["Years At Company"] = stats(df["YearsAtCompany"])
        summary["Distance From Home"] = stats(df["DistanceFromHome"])
        summary["Hourly Rate"] = stats(df["HourlyRate"])

        marital_percent = df["MaritalStatus"].value_counts(normalize=True) * 100
        summary["Marital %"] = {k: round(v, 2) for k, v in marital_percent.items()}

        summary["Avg WorkLife Balance"] = round(df["WorkLifeBalance"].mean(), 2)
        summary["Total Attrition"] = int((df["Attrition"] == "Yes").sum())

        self.summary = summary

        self.log("=== SUMMARY ===")
        for k, v in summary.items():
            self.log(f"{k}: {v}")

    # ---------------- Charts ----------------
    def plot_pie(self):
        if not self.check_data():
            return

        counts = self.df["Department"].value_counts()
        plt.figure()
        plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%")
        plt.title("Employees per Department")
        plt.show()

    def plot_bar(self):
        if not self.check_data():
            return

        counts = self.df["Gender"].value_counts()
        plt.figure()
        plt.bar(counts.index, counts.values)
        plt.title("Gender Distribution")
        plt.xlabel("Gender")
        plt.ylabel("Count")
        plt.show()

    # ---------------- Dashboard ----------------
    def open_dashboard(self):
        if not self.summary:
            self.process_data()
            if not self.summary:
                return

        win = tk.Toplevel(self.root)
        win.title("Dashboard")

        text = tk.Text(win, width=60, height=20)
        text.pack(padx=10, pady=10)

        for k, v in self.summary.items():
            text.insert("end", f"{k}: {v}\n")

    # ---------------- Report ----------------
    def generate_report(self):
        if not self.summary:
            messagebox.showwarning("Warning", "Process data first!")
            return

        try:
            with open("report.txt", "w") as f:
                for k, v in self.summary.items():
                    f.write(f"{k}: {v}\n")

            self.log("Report generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ---------------- Run App ----------------
root = tk.Tk()
app = HealthcareApp(root)
root.mainloop()
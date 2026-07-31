import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    add_employee,
    get_employees,
    update_employee,
    delete_employee,
    search_employees
)

class EmployeeManagementSystem:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Employee Management System")
        self.root.geometry("1200x720")
        self.root.resizable(False, False)

        self.selected_id = None

        self.create_widgets()
        self.load_employees()

    # -------------------------
    # Create Widgets
    # -------------------------
    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Employee Management System",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=10)

        # -------------------------
        # Form
        # -------------------------

        form = tk.LabelFrame(
            self.root,
            text="Employee Details",
            padx=15,
            pady=10
        )

        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Name").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(form, width=30)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form, text="Employee ID").grid(row=0, column=2, padx=10)
        self.employee_id_entry = tk.Entry(form, width=30)
        self.employee_id_entry.grid(row=0, column=3)

        tk.Label(form, text="Department").grid(row=1, column=0, padx=10)
        self.department_entry = tk.Entry(form, width=30)
        self.department_entry.grid(row=1, column=1)

        tk.Label(form, text="Designation").grid(row=1, column=2, padx=10)
        self.designation_entry = tk.Entry(form, width=30)
        self.designation_entry.grid(row=1, column=3)

        tk.Label(form, text="Salary").grid(row=2, column=0, padx=10)
        self.salary_entry = tk.Entry(form, width=30)
        self.salary_entry.grid(row=2, column=1)

        tk.Label(form, text="Email").grid(row=2, column=2, padx=10)
        self.email_entry = tk.Entry(form, width=30)
        self.email_entry.grid(row=2, column=3)

        tk.Label(form, text="Phone").grid(row=3, column=0, padx=10)
        self.phone_entry = tk.Entry(form, width=30)
        self.phone_entry.grid(row=3, column=1)

        # -------------------------
        # Buttons
        # -------------------------

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Employee",
            width=15,
            command=self.add_employee_gui
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update",
            width=15,
            command=self.update_employee_gui
        ).grid(row=0, column=1, padx=5)
        
        tk.Button(
            button_frame,
            text="Delete",
            width=15,
            command=self.delete_employee_gui
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Generate Report",
            width=15,
            bg="#9C27B0",
            fg="white",
            command=self.generate_report
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            command=self.clear_fields
        ).grid(row=0, column=4, padx=5)
        
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(side=tk.LEFT)

        self.search_entry = tk.Entry(
            search_frame,
            width=35
        )
        self.search_entry.pack(
            side=tk.LEFT,
            padx=10
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_employee_gui
        ).pack(side=tk.LEFT)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_employees
        ).pack(side=tk.LEFT, padx=5)
        # -------------------------
        # Table
        # -------------------------

        columns = (
            "ID",
            "Name",
            "Employee ID",
            "Department",
            "Designation",
            "Salary",
            "Email",
            "Phone"
        )

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        self.employee_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(command=self.employee_table.yview)

        scrollbar.pack(side="right", fill="y")
        self.employee_table.pack(side="left", fill="both", expand=True)
        self.employee_table.bind(
            "<<TreeviewSelect>>",
            self.select_employee
        )

        for col in columns:
            self.employee_table.heading(col, text=col)
        self.employee_table.column("ID", width=50, anchor="center")
        self.employee_table.column("Name", width=170)
        self.employee_table.column("Employee ID", width=100, anchor="center")
        self.employee_table.column("Department", width=150)
        self.employee_table.column("Designation", width=160)
        self.employee_table.column("Salary", width=100, anchor="center")
        self.employee_table.column("Email", width=220)
        self.employee_table.column("Phone", width=120, anchor="center")
        self.status = tk.Label(
            self.root,
            text="Employees : 0",
            font=("Arial", 11, "bold")
        )

        self.status.pack(pady=5)

    # -------------------------
    # Load Employees
    # -------------------------

    def load_employees(self):

        for row in self.employee_table.get_children():
            self.employee_table.delete(row)

        employees = get_employees()

        total_salary = 0

        for emp in employees:
            self.employee_table.insert("", tk.END, values=emp)
            salary = emp[5]

        if salary not in (None, ""):
                total_salary += float(salary)

        self.status.config(
            text=f"Employees: {len(employees)}    Total Salary: ₹{total_salary:,.2f}"
        )

    # -------------------------
    # Clear
    # -------------------------

    def clear_fields(self):

        self.name_entry.delete(0, tk.END)
        self.employee_id_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        self.designation_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        self.selected_id = None
        
        
    def select_employee(self, event):

        selected = self.employee_table.focus()

        if not selected:
            return

        values = self.employee_table.item(selected, "values")

        if not values:
            return

        self.clear_fields()

        self.selected_id = int(values[0])

        self.name_entry.insert(0, values[1])
        self.employee_id_entry.insert(0, values[2])
        self.department_entry.insert(0, values[3])
        self.designation_entry.insert(0, values[4])
        self.salary_entry.insert(0, values[5])
        self.email_entry.insert(0, values[6])
        self.phone_entry.insert(0, values[7])
            
    # -------------------------
    # Add Employee
    # -------------------------

    def add_employee_gui(self):
        if (
            not self.name_entry.get().strip()
            or not self.employee_id_entry.get().strip()
            or not self.department_entry.get().strip()
            or not self.designation_entry.get().strip()
            or not self.salary_entry.get().strip()
        ):
            messagebox.showerror(
                "Error",
                "Please fill all required fields."
            )
            return
        try:
            salary = float(self.salary_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Salary must be numeric."
            )
            return
        success = add_employee(
            self.name_entry.get().strip(),
            self.employee_id_entry.get().strip(),
            self.department_entry.get().strip(),
            self.designation_entry.get().strip(),
            self.salary_entry.get().strip(),
            self.email_entry.get().strip(),
            self.phone_entry.get().strip()
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Employee Added Successfully."
            )

            self.load_employees()
            self.clear_fields()

        else:

            messagebox.showerror(
                "Error",
                "Employee ID already exists."
            )
    def update_employee_gui(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select an employee first."
            )
            return

        update_employee(
            self.selected_id,
            self.name_entry.get().strip(),
            self.employee_id_entry.get().strip(),
            self.department_entry.get().strip(),
            self.designation_entry.get().strip(),
            float(self.salary_entry.get()),
            self.email_entry.get().strip(),
            self.phone_entry.get().strip(),   
        )

        messagebox.showinfo(
            "Success",
            "Employee updated successfully."
        )

        self.load_employees(),
        self.clear_fields(),
        self.selected_id = None
    def delete_employee_gui(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Warning",
                "Please select an employee first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm",
            "Delete this employee?"
        )

        if confirm:

            delete_employee(self.selected_id)

            messagebox.showinfo(
                "Success",
                "Employee deleted successfully."
            )

            self.load_employees()
            self.clear_fields()
            self.selected_id = None
    def search_employee_gui(self):

        keyword = self.search_entry.get().strip()

        employees = search_employees(keyword)

        for row in self.employee_table.get_children():
            self.employee_table.delete(row)

        for emp in employees:
            self.employee_table.insert("", tk.END, values=emp)

        self.status.config(
            text=f"Search Results : {len(employees)}"
    )
    def generate_report(self):

        employees = get_employees()

        total_employees = len(employees)

        total_salary = 0

        departments = {}

        for emp in employees:

            salary = float(emp[5])
            total_salary += salary

            dept = emp[3]

            if dept in departments:
                departments[dept] += 1
            else:
                departments[dept] = 1

        average_salary = 0

        if total_employees > 0:
            average_salary = total_salary / total_employees

        report = tk.Toplevel(self.root)

        report.title("Employee Report")

        report.geometry("450x500")

        report.resizable(False, False)

        tk.Label(
            report,
            text="Employee Report",
            font=("Arial",18,"bold")
        ).pack(pady=10)

        tk.Label(
            report,
            text=f"Total Employees : {total_employees}",
            font=("Arial",12)
        ).pack(anchor="w", padx=20, pady=5)

        tk.Label(
            report,
            text=f"Total Salary Expense : ₹{total_salary:,.2f}",
            font=("Arial",12)
        ).pack(anchor="w", padx=20, pady=5)

        tk.Label(
            report,
            text=f"Average Salary : ₹{average_salary:,.2f}",
            font=("Arial",12)
        ).pack(anchor="w", padx=20, pady=5)

        tk.Label(
            report,
            text="Department Summary",
            font=("Arial",13,"bold")
        ).pack(anchor="w", padx=20, pady=15)

        for dept, count in departments.items():

            tk.Label(
                report,
                text=f"{dept} : {count} Employee(s)",
                font=("Arial",11)
            ).pack(anchor="w", padx=40)
    def run(self):
        self.root.mainloop()
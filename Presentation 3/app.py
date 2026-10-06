import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import mysql.connector
from mysql.connector import Error, IntegrityError

APP_TITLE = "Sports Club Membership & Tournament Management System"
DEFAULT_DB = "sports_club"

# ---------- Database ----------
class Database:
    def __init__(self):
        self.conn = None
        self.config = {}

    def connect(self, host, port, user, password, database):
        self.config = {
            "host": host.strip(),
            "port": int(port),
            "user": user.strip(),
            "password": password,
            "database": database.strip(),
        }
        self.conn = mysql.connector.connect(**self.config)
        return self.conn.is_connected()

    def close(self):
        try:
            if self.conn and self.conn.is_connected():
                self.conn.close()
        except Exception:
            pass

    def execute(self, sql, params=(), fetch=False, commit=False):
        if not self.conn or not self.conn.is_connected():
            raise Error("Database is not connected.")
        cur = self.conn.cursor(dictionary=True)
        try:
            cur.execute(sql, params)
            rows = cur.fetchall() if fetch else None
            if commit:
                self.conn.commit()
            return rows
        finally:
            cur.close()

    def scalar(self, sql, params=()):
        rows = self.execute(sql, params, fetch=True)
        if not rows:
            return 0
        return next(iter(rows[0].values()))

# ---------- App ----------
class SportsClubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1280x760")
        self.minsize(1050, 650)
        self.configure(bg="#f4f7fb")
        self.db = Database()
        self.current_page = None
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self._styles()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_connect()

    def _styles(self):
        self.style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(15, 9))
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground="#14213d")
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground="#64748b")
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("Treeview", rowheight=30, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#0f172a")])

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ---------- Connection screen ----------
    def show_connect(self):
        self.clear()
        self.geometry("900x780")
        outer = tk.Frame(self, bg="#eef3f9")
        outer.pack(fill="both", expand=True)

        card = tk.Frame(outer, bg="white", padx=50, pady=28, highlightthickness=1, highlightbackground="#d7dee8")
        card.place(relx=0.5, rely=0.5, anchor="center", width=650, height=700)

        tk.Label(card, text="SPORTS CLUB", font=("Segoe UI", 26, "bold"), fg="#17315f", bg="white").pack(pady=(10, 3))
        tk.Label(card, text="Membership & Tournament Management System", font=("Segoe UI", 12), fg="#64748b", bg="white").pack(pady=(0, 18))
        tk.Label(card, text="Connect to your existing MySQL database", font=("Segoe UI", 11), fg="#334155", bg="white").pack(pady=(0, 12))

        form = tk.Frame(card, bg="white")
        form.pack(fill="x", padx=30)
        self.conn_vars = {
            "host": tk.StringVar(value="localhost"),
            "port": tk.StringVar(value="3306"),
            "user": tk.StringVar(value="root"),
            "password": tk.StringVar(value=""),
            "database": tk.StringVar(value=DEFAULT_DB),
        }
        labels = [("Host", "host"), ("Port", "port"), ("User", "user"), ("Password", "password"), ("Database", "database")]
        for r, (label, key) in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 10), fg="#334155", bg="white", anchor="w").grid(row=r, column=0, sticky="w", pady=5, padx=(0, 15))
            show = "*" if key == "password" else ""
            ent = tk.Entry(form, textvariable=self.conn_vars[key], show=show, font=("Segoe UI", 10), relief="solid", bd=1)
            ent.grid(row=r, column=1, sticky="ew", pady=5, ipady=5)
        form.columnconfigure(1, weight=1)

        self.connect_status = tk.Label(card, text="", font=("Segoe UI", 9), fg="#dc2626", bg="white", wraplength=520)
        self.connect_status.pack(pady=(8, 4))
        connect_btn = ttk.Button(card, text="CONNECT", style="Primary.TButton", command=self.connect_db)
        connect_btn.pack(pady=6, ipadx=45, ipady=2)
        self.bind("<Return>", lambda event: self.connect_db())
        tk.Label(card, text="Press Enter or click CONNECT to continue.", font=("Segoe UI", 9), fg="#64748b", bg="white").pack(pady=(8, 2))
        tk.Label(card, text="Your password is used only for this connection and is not saved.", font=("Segoe UI", 9), fg="#94a3b8", bg="white").pack(pady=(2, 0))

    def connect_db(self):
        try:
            ok = self.db.connect(
                self.conn_vars["host"].get(), self.conn_vars["port"].get(),
                self.conn_vars["user"].get(), self.conn_vars["password"].get(),
                self.conn_vars["database"].get()
            )
            if ok:
                self.show_main()
        except Exception as e:
            self.connect_status.config(text=f"Connection failed: {e}", fg="#dc2626")
            messagebox.showerror("Database Connection", str(e))

    # ---------- Main layout ----------
    def show_main(self):
        self.geometry("1280x760")
        self.clear()
        self.sidebar = tk.Frame(self, bg="#101a2c", width=245)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.content = tk.Frame(self, bg="#f4f7fb")
        self.content.pack(side="right", fill="both", expand=True)
        self.build_sidebar()
        self.show_dashboard()

    def build_sidebar(self):
        tk.Label(self.sidebar, text="SC", font=("Segoe UI", 20, "bold"), fg="#14213d", bg="white", width=3, height=1).pack(pady=(28, 7))
        tk.Label(self.sidebar, text="SPORTS CLUB", font=("Segoe UI", 14, "bold"), fg="white", bg="#101a2c").pack()
        tk.Label(self.sidebar, text="DBMS Management", font=("Segoe UI", 9), fg="#9fb0c8", bg="#101a2c").pack(pady=(2, 18))
        tk.Frame(self.sidebar, bg="#26334a", height=1).pack(fill="x", padx=18, pady=(0, 14))

        self.nav_buttons = []
        groups = [
            ("MAIN", [("Dashboard", self.show_dashboard)]),
            ("MEMBERSHIP", [("Members", lambda: self.show_table_page("MEMBER")), ("Membership Plans", lambda: self.show_table_page("MEMBERSHIP_PLAN")), ("Payments", lambda: self.show_table_page("PAYMENT"))]),
            ("SPORTS", [("Sports", lambda: self.show_table_page("SPORT")), ("Member Sports", lambda: self.show_table_page("MEMBER_SPORT")), ("Coaches", lambda: self.show_table_page("COACH")), ("Teams", lambda: self.show_table_page("TEAM")), ("Facilities", lambda: self.show_table_page("FACILITY")), ("Training Sessions", lambda: self.show_table_page("TRAINING_SESSION"))]),
            ("TOURNAMENTS", [("Tournaments", lambda: self.show_table_page("TOURNAMENT")), ("Participants", lambda: self.show_table_page("PARTICIPANT")), ("Fixtures", lambda: self.show_table_page("FIXTURE")), ("Results", lambda: self.show_table_page("RESULT"))]),
            ("EQUIPMENT", [("Equipment", lambda: self.show_table_page("EQUIPMENT")), ("Equipment Issues", lambda: self.show_table_page("EQUIPMENT_ISSUE"))]),
        ]
        for group, items in groups:
            tk.Label(self.sidebar, text=group, font=("Segoe UI", 9, "bold"), fg="#7186a4", bg="#101a2c", anchor="w").pack(fill="x", padx=25, pady=(8, 3))
            for name, cmd in items:
                b = tk.Button(self.sidebar, text=name, command=cmd, anchor="w", bd=0, relief="flat", bg="#101a2c", fg="#dbe7f7", activebackground="#1c2a43", activeforeground="white", font=("Segoe UI", 10), padx=25, pady=7, cursor="hand2")
                b.pack(fill="x", padx=8)
                self.nav_buttons.append((name, b))
        tk.Frame(self.sidebar, bg="#26334a", height=1).pack(fill="x", padx=18, pady=(15, 10))
        tk.Button(self.sidebar, text="Disconnect", command=self.show_connect, anchor="w", bd=0, bg="#101a2c", fg="#fca5a5", font=("Segoe UI", 10), padx=25, pady=8).pack(fill="x", padx=8)

    def page_header(self, title, subtitle=""):
        head = tk.Frame(self.content, bg="#f4f7fb")
        head.pack(fill="x", padx=30, pady=(25, 12))
        tk.Label(head, text=title, font=("Segoe UI", 25, "bold"), fg="#14213d", bg="#f4f7fb").pack(anchor="w")
        if subtitle:
            tk.Label(head, text=subtitle, font=("Segoe UI", 10), fg="#64748b", bg="#f4f7fb").pack(anchor="w", pady=(3, 0))

    # ---------- Dashboard ----------
    def show_dashboard(self):
        for w in self.content.winfo_children(): w.destroy()
        self.page_header("Dashboard", "Live information from your MySQL database")
        cards = tk.Frame(self.content, bg="#f4f7fb")
        cards.pack(fill="x", padx=30, pady=10)
        metrics = [
            ("Total Members", "SELECT COUNT(*) FROM MEMBER"),
            ("Active Members", "SELECT COUNT(*) FROM MEMBER WHERE Status='Active'"),
            ("Sports", "SELECT COUNT(*) FROM SPORT"),
            ("Tournaments", "SELECT COUNT(*) FROM TOURNAMENT"),
            ("Teams", "SELECT COUNT(*) FROM TEAM"),
            ("Facilities", "SELECT COUNT(*) FROM FACILITY"),
        ]
        for i, (label, sql) in enumerate(metrics):
            card = tk.Frame(cards, bg="white", highlightthickness=1, highlightbackground="#e2e8f0")
            card.grid(row=i//3, column=i%3, sticky="ew", padx=5, pady=5, ipadx=15, ipady=12)
            tk.Label(card, text=label, font=("Segoe UI", 10), fg="#64748b", bg="white").pack(anchor="w")
            try: value = self.db.scalar(sql)
            except Exception: value = "—"
            tk.Label(card, text=str(value), font=("Segoe UI", 25, "bold"), fg="#172b4d", bg="white").pack(anchor="w", pady=3)
        for c in range(3): cards.columnconfigure(c, weight=1)

        lower = tk.Frame(self.content, bg="#f4f7fb")
        lower.pack(fill="both", expand=True, padx=30, pady=15)
        left = tk.Frame(lower, bg="white", highlightthickness=1, highlightbackground="#e2e8f0")
        left.pack(side="left", fill="both", expand=True, padx=(0, 7))
        tk.Label(left, text="Upcoming Tournaments", font=("Segoe UI", 13, "bold"), fg="#14213d", bg="white").pack(anchor="w", padx=18, pady=15)
        try:
            rows = self.db.execute("SELECT Tournament_Name, Start_Date, End_Date FROM TOURNAMENT ORDER BY Start_Date LIMIT 8", fetch=True)
        except Exception:
            rows = []
        self.simple_tree(left, ["Tournament", "Start", "End"], [[r["Tournament_Name"], r["Start_Date"], r["End_Date"]] for r in rows])

        right = tk.Frame(lower, bg="white", highlightthickness=1, highlightbackground="#e2e8f0")
        right.pack(side="right", fill="both", expand=True, padx=(7, 0))
        tk.Label(right, text="Recent Members", font=("Segoe UI", 13, "bold"), fg="#14213d", bg="white").pack(anchor="w", padx=18, pady=15)
        try:
            rows = self.db.execute("SELECT Member_ID, Name, Status, Join_Date FROM MEMBER ORDER BY Member_ID DESC LIMIT 8", fetch=True)
        except Exception:
            rows = []
        self.simple_tree(right, ["ID", "Name", "Status", "Join Date"], [[r["Member_ID"], r["Name"], r["Status"], r["Join_Date"]] for r in rows])

    def simple_tree(self, parent, headers, rows):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        tree = ttk.Treeview(frame, columns=headers, show="headings", height=8)
        for h in headers:
            tree.heading(h, text=h)
            tree.column(h, width=max(90, 650//len(headers)), anchor="w")
        for row in rows: tree.insert("", "end", values=row)
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    # ---------- Generic table pages ----------
    TABLES = {
        "MEMBER": {"title":"Members", "pk":"Member_ID", "order":"Member_ID", "columns":["Member_ID","Name","DOB","Gender","Phone","Email","Address","Join_Date","Status","Plan_ID"]},
        "MEMBERSHIP_PLAN": {"title":"Membership Plans", "pk":"Plan_ID", "order":"Plan_ID", "columns":["Plan_ID","Plan_Name","Duration","Fee_Amount","Description"]},
        "PAYMENT": {"title":"Payments", "pk":"Payment_ID", "order":"Payment_ID", "columns":["Payment_ID","Payment_Date","Amount","Remarks","Mode","Member_ID"]},
        "SPORT": {"title":"Sports", "pk":"Sport_ID", "order":"Sport_ID", "columns":["Sport_ID","Sport_Name","Description"]},
        "MEMBER_SPORT": {"title":"Member Sports", "pk":"Member_ID", "order":"Member_ID, Sport_ID", "columns":["Member_ID","Sport_ID"]},
        "COACH": {"title":"Coaches", "pk":"Coach_ID", "order":"Coach_ID", "columns":["Coach_ID","Coach_Name","Phone","Email","Experience"]},
        "TEAM": {"title":"Teams", "pk":"Team_ID", "order":"Team_ID", "columns":["Team_ID","Team_Name","Sport_ID","Coach_ID"]},
        "FACILITY": {"title":"Facilities", "pk":"Facility_ID", "order":"Facility_ID", "columns":["Facility_ID","Facility_Name","Location","Type","Availability"]},
        "TRAINING_SESSION": {"title":"Training Sessions", "pk":"Session_ID", "order":"Session_ID", "columns":["Session_ID","Session_Date","Start_Time","End_Time","Team_ID","Facility_ID"]},
        "TOURNAMENT": {"title":"Tournaments", "pk":"Tournament_ID", "order":"Tournament_ID", "columns":["Tournament_ID","Tournament_Name","Sport_ID","Start_Date","End_Date","Description"]},
        "PARTICIPANT": {"title":"Participants", "pk":"Participant_ID", "order":"Participant_ID", "columns":["Participant_ID","Tournament_ID","Member_ID","Team_ID","Role"]},
        "FIXTURE": {"title":"Fixtures", "pk":"Fixture_ID", "order":"Fixture_ID", "columns":["Fixture_ID","Fixture_Date","Time","Venue","Tournament_ID"]},
        "RESULT": {"title":"Results", "pk":"Result_ID", "order":"Result_ID", "columns":["Result_ID","Home_Score","Away_Score","Winner","Remarks","Fixture_ID"]},
        "EQUIPMENT": {"title":"Equipment", "pk":"Equipment_ID", "order":"Equipment_ID", "columns":["Equipment_ID","Equipment_Name","Category","Quantity"]},
        "EQUIPMENT_ISSUE": {"title":"Equipment Issues", "pk":"Issue_ID", "order":"Issue_ID", "columns":["Issue_ID","Issue_Date","Return_Date","Condition","Member_ID","Equipment_ID"]},
    }

    def show_table_page(self, table):
        for w in self.content.winfo_children(): w.destroy()
        meta = self.TABLES[table]
        self.page_header(meta["title"], f"View, insert and delete records from {table}")
        toolbar = tk.Frame(self.content, bg="#f4f7fb")
        toolbar.pack(fill="x", padx=30, pady=(0, 10))
        ttk.Button(toolbar, text="Refresh", command=lambda: self.show_table_page(table)).pack(side="left")
        ttk.Button(toolbar, text="Add Record", style="Primary.TButton", command=lambda: self.open_insert(table)).pack(side="left", padx=8)
        ttk.Button(toolbar, text="Delete Selected", command=lambda: self.delete_selected(table, tree)).pack(side="left")
        tk.Label(toolbar, text="Double-click a row to view details", bg="#f4f7fb", fg="#64748b", font=("Segoe UI", 9)).pack(side="right")

        box = tk.Frame(self.content, bg="white", highlightthickness=1, highlightbackground="#e2e8f0")
        box.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        tree = ttk.Treeview(box, columns=meta["columns"], show="headings")
        for col in meta["columns"]:
            tree.heading(col, text=col.replace("_", " "))
            tree.column(col, width=130, minwidth=90, anchor="w")
        try:
            rows = self.db.execute(f"SELECT * FROM {table} ORDER BY {meta['order']}", fetch=True)
        except Exception as e:
            messagebox.showerror("Database Error", str(e)); rows=[]
        for row in rows:
            tree.insert("", "end", values=[row.get(c) for c in meta["columns"]])
        tree.bind("<Double-1>", lambda e: self.view_selected(tree, meta["columns"]))
        y = ttk.Scrollbar(box, orient="vertical", command=tree.yview)
        x = ttk.Scrollbar(box, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        tree.grid(row=0, column=0, sticky="nsew")
        y.grid(row=0, column=1, sticky="ns")
        x.grid(row=1, column=0, sticky="ew")
        box.rowconfigure(0, weight=1); box.columnconfigure(0, weight=1)

    def view_selected(self, tree, columns):
        sel = tree.selection()
        if not sel: return
        vals = tree.item(sel[0], "values")
        win = tk.Toplevel(self); win.title("Record Details"); win.geometry("650x500"); win.configure(bg="white")
        tk.Label(win, text="Record Details", font=("Segoe UI", 18, "bold"), bg="white", fg="#14213d").pack(anchor="w", padx=25, pady=20)
        body = tk.Frame(win, bg="white"); body.pack(fill="both", expand=True, padx=25)
        for i,(c,v) in enumerate(zip(columns, vals)):
            tk.Label(body, text=c.replace("_", " "), font=("Segoe UI", 9, "bold"), fg="#64748b", bg="white").grid(row=i, column=0, sticky="nw", pady=7, padx=(0,20))
            tk.Label(body, text=str(v), font=("Segoe UI", 10), fg="#0f172a", bg="white", wraplength=430, justify="left").grid(row=i, column=1, sticky="w", pady=7)

    def delete_selected(self, table, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Delete", "Select a record first."); return
        meta = self.TABLES[table]
        vals = tree.item(sel[0], "values")
        pk_cols = [x.strip() for x in meta["pk"].split(",")]
        try:
            where = " AND ".join([f"{c}=%s" for c in pk_cols])
            params = tuple(vals[meta["columns"].index(c)] for c in pk_cols)
        except Exception:
            messagebox.showerror("Delete", "Unable to identify the selected record."); return
        if not messagebox.askyesno("Confirm Delete", f"Delete the selected {meta['title'][:-1] if meta['title'].endswith('s') else meta['title']} record?\n\nThis action cannot be undone."):
            return
        try:
            self.db.execute(f"DELETE FROM {table} WHERE {where}", params, commit=True)
            messagebox.showinfo("Deleted", "Record deleted successfully.")
            self.show_table_page(table)
        except IntegrityError:
            messagebox.showerror("Cannot Delete", "This record is referenced by another table. Delete the related child records first, or choose a record without dependencies.")
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))

    # ---------- Insert dialogs ----------
    def next_id(self, table, col):
        return int(self.db.scalar(f"SELECT COALESCE(MAX({col}),0)+1 FROM {table}"))

    def open_insert(self, table):
        builders = {
            "MEMBER": self.insert_member,
            "MEMBERSHIP_PLAN": self.insert_plan,
            "PAYMENT": self.insert_payment,
            "SPORT": self.insert_sport,
            "MEMBER_SPORT": self.insert_member_sport,
            "COACH": self.insert_coach,
            "TEAM": self.insert_team,
            "FACILITY": self.insert_facility,
            "TRAINING_SESSION": self.insert_training,
            "TOURNAMENT": self.insert_tournament,
            "PARTICIPANT": self.insert_participant,
            "FIXTURE": self.insert_fixture,
            "RESULT": self.insert_result,
            "EQUIPMENT": self.insert_equipment,
            "EQUIPMENT_ISSUE": self.insert_issue,
        }
        builders[table]()

    def dialog(self, title, width=650, height=620):
        w = tk.Toplevel(self); w.title(title); w.geometry(f"{width}x{height}"); w.configure(bg="#f4f7fb"); w.transient(self); w.grab_set()
        tk.Label(w, text=title, font=("Segoe UI", 19, "bold"), bg="#f4f7fb", fg="#14213d").pack(anchor="w", padx=25, pady=(22,4))
        body = tk.Frame(w, bg="white", padx=25, pady=20); body.pack(fill="both", expand=True, padx=25, pady=15)
        return w, body

    def field(self, body, row, label, var, options=None, readonly=False, password=False):
        tk.Label(body, text=label, bg="white", fg="#334155", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", pady=7, padx=(0,15))
        if options is not None:
            widget = ttk.Combobox(body, textvariable=var, values=options, state="readonly", font=("Segoe UI", 10))
        else:
            widget = tk.Entry(body, textvariable=var, show="*" if password else "", state="readonly" if readonly else "normal", font=("Segoe UI", 10), relief="solid", bd=1)
        widget.grid(row=row, column=1, sticky="ew", pady=7, ipady=5)
        return widget

    def dialog_buttons(self, w, body, save):
        row = body.grid_size()[1] + 1
        ttk.Button(body, text="Cancel", command=w.destroy).grid(row=row, column=0, pady=20, sticky="w")
        ttk.Button(body, text="Save Record", style="Primary.TButton", command=save).grid(row=row, column=1, pady=20, sticky="e")
        body.columnconfigure(1, weight=1)

    def lookup(self, table, id_col, label_col):
        rows = self.db.execute(f"SELECT {id_col}, {label_col} FROM {table} ORDER BY {label_col}", fetch=True)
        return [f"{r[id_col]} | {r[label_col]}" for r in rows]

    def selected_id(self, value): return int(value.split(" | ",1)[0])

    def insert_member(self):
        w,b=self.dialog("Add Member", 680, 620)
        vars={k:tk.StringVar() for k in ["name","dob","gender","phone","email","address","join","status","plan"]}
        vars["gender"].set("Female"); vars["status"].set("Active"); vars["dob"].set("2007-01-01"); vars["join"].set(str(date.today()))
        plan_opts=self.lookup("MEMBERSHIP_PLAN","Plan_ID","Plan_Name")
        labels=[("Name","name"),("DOB (YYYY-MM-DD)","dob"),("Gender","gender"),("Phone","phone"),("Email","email"),("Address","address"),("Join Date (YYYY-MM-DD)","join"),("Status","status"),("Membership Plan","plan")]
        for i,(l,k) in enumerate(labels): self.field(b,i,l,vars[k], ["Male","Female","Other"] if k=="gender" else (["Active","Inactive"] if k=="status" else (plan_opts if k=="plan" else None)))
        def save():
            try:
                pid=self.selected_id(vars["plan"].get());
                self.db.execute("INSERT INTO MEMBER (Member_ID,Name,DOB,Gender,Phone,Email,Address,Join_Date,Status,Plan_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.next_id("MEMBER","Member_ID"),vars["name"].get(),vars["dob"].get(),vars["gender"].get(),vars["phone"].get(),vars["email"].get(),vars["address"].get(),vars["join"].get(),vars["status"].get(),pid),commit=True); w.destroy(); self.show_table_page("MEMBER")
            except Exception as e: messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_plan(self):
        w,b=self.dialog("Add Membership Plan",650,500); v={k:tk.StringVar() for k in ["name","duration","fee","desc"]}
        for i,(l,k) in enumerate([("Plan Name","name"),("Duration","duration"),("Fee Amount","fee"),("Description","desc")]): self.field(b,i,l,v[k])
        def save():
            try: self.db.execute("INSERT INTO MEMBERSHIP_PLAN (Plan_ID,Plan_Name,Duration,Fee_Amount,Description) VALUES (%s,%s,%s,%s,%s)",(self.next_id("MEMBERSHIP_PLAN","Plan_ID"),v["name"].get(),v["duration"].get(),v["fee"].get(),v["desc"].get()),commit=True); w.destroy(); self.show_table_page("MEMBERSHIP_PLAN")
            except Exception as e: messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_payment(self):
        w,b=self.dialog("Add Payment",650,500); v={k:tk.StringVar() for k in ["date","amount","remarks","mode","member"]}; v["date"].set(str(date.today())); v["mode"].set("Cash")
        opts=self.lookup("MEMBER","Member_ID","Name")
        for i,(l,k) in enumerate([("Payment Date","date"),("Amount","amount"),("Remarks","remarks"),("Mode","mode"),("Member","member")]): self.field(b,i,l,v[k],["Cash","UPI","Card","Bank Transfer"] if k=="mode" else (opts if k=="member" else None))
        def save():
            try: self.db.execute("INSERT INTO PAYMENT (Payment_ID,Payment_Date,Amount,Remarks,Mode,Member_ID) VALUES (%s,%s,%s,%s,%s,%s)",(self.next_id("PAYMENT","Payment_ID"),v["date"].get(),v["amount"].get(),v["remarks"].get(),v["mode"].get(),self.selected_id(v["member"].get())),commit=True); w.destroy(); self.show_table_page("PAYMENT")
            except Exception as e: messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_sport(self):
        w,b=self.dialog("Add Sport",600,420); v={k:tk.StringVar() for k in ["name","desc"]}
        for i,(l,k) in enumerate([("Sport Name","name"),("Description","desc")]): self.field(b,i,l,v[k])
        self.dialog_buttons(w,b,lambda:self.simple_insert(w,"SPORT","Sport_ID",[v["name"].get(),v["desc"].get()],"INSERT INTO SPORT (Sport_ID,Sport_Name,Description) VALUES (%s,%s,%s)"))

    def insert_coach(self):
        w,b=self.dialog("Add Coach",620,500); v={k:tk.StringVar() for k in ["name","phone","email","exp"]}
        for i,(l,k) in enumerate([("Coach Name","name"),("Phone","phone"),("Email","email"),("Experience","exp")]): self.field(b,i,l,v[k])
        self.dialog_buttons(w,b,lambda:self.simple_insert(w,"COACH","Coach_ID",[v["name"].get(),v["phone"].get(),v["email"].get(),v["exp"].get()],"INSERT INTO COACH (Coach_ID,Coach_Name,Phone,Email,Experience) VALUES (%s,%s,%s,%s,%s)"))

    def insert_team(self):
        w,b=self.dialog("Add Team",620,460); v={k:tk.StringVar() for k in ["name","sport","coach"]}; sports=self.lookup("SPORT","Sport_ID","Sport_Name"); coaches=self.lookup("COACH","Coach_ID","Coach_Name")
        self.field(b,0,"Team Name",v["name"]); self.field(b,1,"Sport",v["sport"],sports); self.field(b,2,"Coach",v["coach"],coaches)
        def save():
            try:self.db.execute("INSERT INTO TEAM (Team_ID,Team_Name,Sport_ID,Coach_ID) VALUES (%s,%s,%s,%s)",(self.next_id("TEAM","Team_ID"),v["name"].get(),self.selected_id(v["sport"].get()),self.selected_id(v["coach"].get())),commit=True);w.destroy();self.show_table_page("TEAM")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_facility(self):
        w,b=self.dialog("Add Facility",620,480); v={k:tk.StringVar() for k in ["name","loc","type","avail"]};v["avail"].set("Available")
        for i,(l,k) in enumerate([("Facility Name","name"),("Location","loc"),("Type","type"),("Availability","avail")]): self.field(b,i,l,v[k],["Available","Unavailable"] if k=="avail" else None)
        self.dialog_buttons(w,b,lambda:self.simple_insert(w,"FACILITY","Facility_ID",[v["name"].get(),v["loc"].get(),v["type"].get(),v["avail"].get()],"INSERT INTO FACILITY (Facility_ID,Facility_Name,Location,Type,Availability) VALUES (%s,%s,%s,%s,%s)"))

    def insert_tournament(self):
        w,b=self.dialog("Add Tournament",650,500); v={k:tk.StringVar() for k in ["name","sport","start","end","desc"]};v["start"].set(str(date.today()))
        sports=self.lookup("SPORT","Sport_ID","Sport_Name")
        for i,(l,k) in enumerate([("Tournament Name","name"),("Sport","sport"),("Start Date","start"),("End Date","end"),("Description","desc")]): self.field(b,i,l,v[k],sports if k=="sport" else None)
        def save():
            try:self.db.execute("INSERT INTO TOURNAMENT (Tournament_ID,Tournament_Name,Sport_ID,Start_Date,End_Date,Description) VALUES (%s,%s,%s,%s,%s,%s)",(self.next_id("TOURNAMENT","Tournament_ID"),v["name"].get(),self.selected_id(v["sport"].get()),v["start"].get(),v["end"].get(),v["desc"].get()),commit=True);w.destroy();self.show_table_page("TOURNAMENT")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_equipment(self):
        w,b=self.dialog("Add Equipment",620,440); v={k:tk.StringVar() for k in ["name","cat","qty"]}
        for i,(l,k) in enumerate([("Equipment Name","name"),("Category","cat"),("Quantity","qty")]): self.field(b,i,l,v[k])
        self.dialog_buttons(w,b,lambda:self.simple_insert(w,"EQUIPMENT","Equipment_ID",[v["name"].get(),v["cat"].get(),v["qty"].get()],"INSERT INTO EQUIPMENT (Equipment_ID,Equipment_Name,Category,Quantity) VALUES (%s,%s,%s,%s)"))

    def insert_member_sport(self):
        w,b=self.dialog("Assign Sport to Member",600,400); v={"member":tk.StringVar(),"sport":tk.StringVar()};members=self.lookup("MEMBER","Member_ID","Name");sports=self.lookup("SPORT","Sport_ID","Sport_Name")
        self.field(b,0,"Member",v["member"],members);self.field(b,1,"Sport",v["sport"],sports)
        def save():
            try:self.db.execute("INSERT INTO MEMBER_SPORT (Member_ID,Sport_ID) VALUES (%s,%s)",(self.selected_id(v["member"].get()),self.selected_id(v["sport"].get())),commit=True);w.destroy();self.show_table_page("MEMBER_SPORT")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_training(self):
        w,b=self.dialog("Add Training Session",650,500);v={k:tk.StringVar() for k in ["date","start","end","team","facility"]};v["date"].set(str(date.today()));teams=self.lookup("TEAM","Team_ID","Team_Name");fac=self.lookup("FACILITY","Facility_ID","Facility_Name")
        for i,(l,k) in enumerate([("Session Date","date"),("Start Time (HH:MM:SS)","start"),("End Time (HH:MM:SS)","end"),("Team","team"),("Facility","facility")]):self.field(b,i,l,v[k],teams if k=="team" else (fac if k=="facility" else None))
        def save():
            try:self.db.execute("INSERT INTO TRAINING_SESSION (Session_ID,Session_Date,Start_Time,End_Time,Team_ID,Facility_ID) VALUES (%s,%s,%s,%s,%s,%s)",(self.next_id("TRAINING_SESSION","Session_ID"),v["date"].get(),v["start"].get(),v["end"].get(),self.selected_id(v["team"].get()),self.selected_id(v["facility"].get())),commit=True);w.destroy();self.show_table_page("TRAINING_SESSION")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_participant(self):
        w,b=self.dialog("Add Participant",620,500);v={k:tk.StringVar() for k in ["tour","member","team","role"]};t=self.lookup("TOURNAMENT","Tournament_ID","Tournament_Name");m=self.lookup("MEMBER","Member_ID","Name");teams=self.lookup("TEAM","Team_ID","Team_Name")
        for i,(l,k) in enumerate([("Tournament","tour"),("Member","member"),("Team","team"),("Role","role")]):self.field(b,i,l,v[k],t if k=="tour" else (m if k=="member" else (teams if k=="team" else None)))
        def save():
            try:self.db.execute("INSERT INTO PARTICIPANT (Participant_ID,Tournament_ID,Member_ID,Team_ID,Role) VALUES (%s,%s,%s,%s,%s)",(self.next_id("PARTICIPANT","Participant_ID"),self.selected_id(v["tour"].get()),self.selected_id(v["member"].get()),self.selected_id(v["team"].get()),v["role"].get()),commit=True);w.destroy();self.show_table_page("PARTICIPANT")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_fixture(self):
        w,b=self.dialog("Add Fixture",620,500);v={k:tk.StringVar() for k in ["date","time","venue","tour"]};v["date"].set(str(date.today()));t=self.lookup("TOURNAMENT","Tournament_ID","Tournament_Name")
        for i,(l,k) in enumerate([("Fixture Date","date"),("Time","time"),("Venue","venue"),("Tournament","tour")]):self.field(b,i,l,v[k],t if k=="tour" else None)
        def save():
            try:self.db.execute("INSERT INTO FIXTURE (Fixture_ID,Fixture_Date,Time,Venue,Tournament_ID) VALUES (%s,%s,%s,%s,%s)",(self.next_id("FIXTURE","Fixture_ID"),v["date"].get(),v["time"].get(),v["venue"].get(),self.selected_id(v["tour"].get())),commit=True);w.destroy();self.show_table_page("FIXTURE")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_result(self):
        w,b=self.dialog("Add Result",620,500);v={k:tk.StringVar() for k in ["home","away","winner","remarks","fixture"]};f=self.lookup("FIXTURE","Fixture_ID","Venue")
        for i,(l,k) in enumerate([("Home Score","home"),("Away Score","away"),("Winner","winner"),("Remarks","remarks"),("Fixture","fixture")]):self.field(b,i,l,v[k],f if k=="fixture" else None)
        def save():
            try:self.db.execute("INSERT INTO RESULT (Result_ID,Home_Score,Away_Score,Winner,Remarks,Fixture_ID) VALUES (%s,%s,%s,%s,%s,%s)",(self.next_id("RESULT","Result_ID"),v["home"].get(),v["away"].get(),v["winner"].get(),v["remarks"].get(),self.selected_id(v["fixture"].get())),commit=True);w.destroy();self.show_table_page("RESULT")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def insert_issue(self):
        w,b=self.dialog("Add Equipment Issue",620,500);v={k:tk.StringVar() for k in ["date","ret","condition","member","equipment"]};v["date"].set(str(date.today()));m=self.lookup("MEMBER","Member_ID","Name");e=self.lookup("EQUIPMENT","Equipment_ID","Equipment_Name")
        for i,(l,k) in enumerate([("Issue Date","date"),("Return Date","ret"),("Condition","condition"),("Member","member"),("Equipment","equipment")]):self.field(b,i,l,v[k],m if k=="member" else (e if k=="equipment" else None))
        def save():
            try:self.db.execute("INSERT INTO EQUIPMENT_ISSUE (Issue_ID,Issue_Date,Return_Date,`Condition`,Member_ID,Equipment_ID) VALUES (%s,%s,%s,%s,%s,%s)",(self.next_id("EQUIPMENT_ISSUE","Issue_ID"),v["date"].get(),v["ret"].get() or None,v["condition"].get(),self.selected_id(v["member"].get()),self.selected_id(v["equipment"].get())),commit=True);w.destroy();self.show_table_page("EQUIPMENT_ISSUE")
            except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)
        self.dialog_buttons(w,b,save)

    def simple_insert(self,w,table,id_col,values,sql):
        try:self.db.execute(sql,(self.next_id(table,id_col),*values),commit=True);w.destroy();self.show_table_page(table)
        except Exception as e:messagebox.showerror("Insert Error",str(e),parent=w)

    def on_close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = SportsClubApp()
    app.mainloop()

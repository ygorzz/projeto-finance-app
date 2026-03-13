from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from helpers import login_required, apology, brl
from flask_session import Session
from datetime import datetime
import locale

app = Flask(__name__)
# Sessions expiram quando fecha o navegado
app.config["SESSION_PERMANENT"] = False
# Salva o id da sessão em um arquivo 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")


# FUNÇÕES AUXILIARES #

# Verifica se email é válido
def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
    
# Verifica se email já existe 
def email_already_exists(email):
    email_exists = db.execute("SELECT id FROM users WHERE email = ?", email)
    if len(email_exists) > 0:
        return True
    else:
        return False

# Verifica se username já existe
def username_already_exists(username):
    username_exists = db.execute("SELECT id FROM users WHERE username = ?", username)
    if len(username_exists) > 0:
        return True
    else:
        return False
   
# Insere user no BD 
def register_user(username, email, password):
    return db.execute("INSERT INTO users (username, email, hash_password) VALUES (?, ?, ?)", username, email, generate_password_hash(password))

# Verifica se user está no BD - /login
def user_is_registered(username, password):
    rows = db.execute("SELECT hash_password FROM users WHERE username = ?", username)
    
    if len(rows) != 1:
        return False
        
    if check_password_hash(rows[0]["hash_password"], password):
        return True
    else:
        return False

# Retorna id do user - /login
def get_user_id(username):
    rows = db.execute("SELECT id FROM users WHERE username = ?", username)
    id = rows[0]["id"]
    return id

# Retorna o username do user - /dashboard
def get_user_username():
    rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = rows[0]["username"]
    return username

# Seleciona * tabela colors - /categories
def get_colors():
    return db.execute("SELECT * FROM colors")

# Retorna o id de uma respectiva cor - /categories
def get_color_id(color):
    rows = db.execute("SELECT id FROM colors WHERE code = ?", color)
    id = rows[0]["id"]
    return id

# Insere categoria no BD - /categories
def insert_category(category, id_color):
     return db.execute("INSERT INTO categories (user_id, name, id_color) VALUES (?, ?, ?)", session["user_id"], category, id_color)

# Retorna infos das categorias - /categories
def get_categories_name_color():
    return db.execute("SELECT c.id, c.name, colors.code FROM categories AS c JOIN colors ON c.id_color = colors.id WHERE user_id = ?", session["user_id"])

# Retorna infos das categorias - /budget e /cash_flow
def get_categories_name_id():
    return db.execute("SELECT name, id FROM categories WHERE user_id = ?", session["user_id"])

# Retorna gasto por categoria - /dashboard
def spent_by_category(month, year):
    
    if not month:
        month = datetime.now().strftime('%m')
        
    if not year:
        year = datetime.now().strftime('%Y')
        
    # Garante que month terá dois dígitos, (ex: "3" -> "03"), para que a query funcione
    # Formata para str pois o input date manda uma str para o BD
    month = str(month).zfill(2)
        
    return db.execute("SELECT COALESCE(c.name, 'Sem categoria') AS name, SUM(t.amount) AS total_amount FROM transactions AS t LEFT JOIN categories AS c ON t.category_id = c.id WHERE t.user_id = ? AND t.amount < 0 AND strftime('%m', t.date) = ? AND strftime('%Y', t.date) = ? GROUP BY t.category_id", session["user_id"], month, year)

# Verifica se categoria já existe - /categories e /check_categories
def category_already_exists(category):
    categories = db.execute("SELECT id FROM categories WHERE user_id = ? AND name = ?", session["user_id"], category)
    if len(categories) != 1:
        return False
    else:
        return True

# Insere um orçamento no BD - /budgets
def insert_budget(category_id, amount):
    return db.execute("INSERT INTO budgets (user_id, category_id, amount) VALUES (?, ?, ?)", session["user_id"], category_id, amount)

# Retorna infos de orçamentos para serem exibidas - /budgets
def print_budgets():    
    # LEFT JOIN: garante que o orçamento apareça mesmo sem gastos
    # COALESCE: se o gasto for NULL (sem transações), ele transforma em 0
    return db.execute("SELECT b.id, c.name, colors.code, b.amount, COALESCE(SUM(CASE WHEN t.amount < 0 THEN t.amount ELSE 0 END), 0) AS total_spent, (COALESCE(SUM(CASE WHEN t.amount < 0 THEN t.amount ELSE 0 END), 0) / b.amount * 100) AS percentage FROM categories AS c JOIN budgets AS b ON c.id = b.category_id LEFT JOIN transactions AS t ON c.id = t.category_id JOIN colors ON c.id_color = colors.id WHERE c.user_id = ? GROUP BY c.name", session["user_id"])

# Insere uma transação no BD - /transactions
def insert_transaction(category_id, date, amount):
    db.execute("INSERT INTO transactions (user_id, category_id, date, amount) VALUES (?, ?, ?, ?)", session["user_id"], category_id, date, amount)

# Retorna dinheiro total do user - /expenses_are_greater...
def get_total_cash():
    cash = db.execute("SELECT COALESCE(SUM(t.amount), 0) AS total_cash FROM transactions AS t WHERE user_id = ?", session["user_id"])
    cash = cash[0]["total_cash"]
    return cash

# Retorna infos das transações - /cash_flow
def get_transaction_name_amount():
    return db.execute("SELECT t.amount, c.name FROM transactions AS t JOIN categories AS c ON t.category_id = c.id WHERE c.user_id = ? ORDER BY t.id DESC LIMIT 3", session["user_id"])

# Retorna infos das transações, com limite - /dashboard
def get_transaction_name_amount_date(limit, month, year):
    
    if not month:
        month = datetime.now().strftime('%m')
        
    if not year:
        year = datetime.now().strftime('%Y')
        
    # Garante que month terá dois dígitos, (ex: "3" -> "03"), para que a query funcione
    # Formata para str pois o input date manda uma str para o BD
    month = str(month).zfill(2)
    year = str(year)
    
    return db.execute("SELECT t.amount, COALESCE(c.name, 'Sem categoria') AS name, t.date FROM transactions AS t LEFT JOIN categories AS c ON t.category_id = c.id WHERE c.user_id = ? AND strftime('%m', t.date) = ? AND strftime('%Y', t.date) = ? ORDER BY t.date DESC, t.id DESC LIMIT ?", session["user_id"], month, year, limit)

# Retorna infos de todas as transações - /history
def get_transactions_history():
    return db.execute("SELECT t.id, t.amount, COALESCE(c.name, 'Sem categoria') AS category_name, t.date FROM transactions AS t LEFT JOIN categories AS c ON t.category_id = c.id WHERE t.user_id = ? ORDER BY t.id DESC", session["user_id"])

# Retorna entradas - /dashboard
def get_incomes(month, year): 
    
    if not month:
        month = datetime.now().strftime('%m')
        
    if not year:
        year = datetime.now().strftime('%Y')
        
    # Garante que o mês tenha dois dígitos (ex: "3" -> "03")
    # Formata para str pois o input date manda uma str para o BD
    month = str(month).zfill(2)
    year = str(year)
    
    total_incomes = db.execute("SELECT COALESCE(SUM(amount), 0) AS total_incomes FROM transactions WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ? AND amount > 0", session["user_id"], month, year)
    total_incomes = total_incomes[0]["total_incomes"]
    return total_incomes

# Retorna despesas - /dashboard
def get_expenses(month, year):
    
    if not month:
        month = datetime.now().strftime('%m')
        
    if not year:
        year = datetime.now().strftime('%Y')
        
    # Garante que o mês tenha dois dígitos (ex: "3" -> "03")
    # Formata para str pois o input date manda uma str para o BD
    month = str(month).zfill(2)
    year = str(year)
    
    total_expenses = db.execute("SELECT COALESCE(SUM(amount), 0) AS total_expenses FROM transactions WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ? AND amount < 0", session["user_id"], month, year)
    total_expenses = total_expenses[0]["total_expenses"]
    return total_expenses

# Retorna infos de orçamentos para serem exibidas - /dashboard
def print_budgets_dashboard():    
    # LEFT JOIN: garante que o orçamento apareça mesmo sem gastos
    # COALESCE: se o gasto for NULL (sem transações), ele transforma em 0
    return db.execute("SELECT c.name, colors.code, b.amount, ABS(COALESCE(SUM(t.amount), 0)) AS total_spent, (ABS(COALESCE(SUM(t.amount), 0)) / b.amount * 100) AS percentage FROM categories AS c JOIN budgets AS b ON c.id = b.category_id LEFT JOIN transactions AS t ON c.id = t.category_id  JOIN colors ON c.id_color = colors.id WHERE c.user_id = ? GROUP BY c.name HAVING (ABS(COALESCE(SUM(t.amount), 0)) / b.amount * 100) > 50", session["user_id"])

# Verifica se valor is Not a Number - /budget e /cash_flow
def is_nan(value):
    try:
        # Ao tentar converter para float verificamos se o valor é um numero
        value = float(value)
        return False
    except ValueError:
        return True

# Retorna anos em que houve transações - /dashboard (filtro de busca)
def select_years():
    return db.execute("SELECT DISTINCT(strftime('%Y', date)) AS year FROM transactions WHERE user_id = ? ", session["user_id"])
    
# Deleções do BD
def delete_category(id):
    return db.execute("DELETE FROM categories WHERE id = ? AND user_id = ?", id, session["user_id"])

def delete_budget(id):
    return db.execute("DELETE FROM budgets WHERE id = ? AND user_id = ? ", id, session["user_id"])

def delete_transaction(id):
    return db.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", id, session["user_id"])


# VARIÁVEIS AUXILIARES #

MAX_USERNAME = 20
MIN_USERNAME = 4
MAX_PASSWORD = 24   
MIN_PASSWORD = 8


# ROTAS #

@app.route("/")
@login_required
def index():
    
    return redirect("/dashboard")


@app.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        
        # Armazrena as entradas do usuário e as formata
        username = request.form.get("username", "").strip() # é case sensitive
        email = request.form.get("email", "").lower().strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # TRATAMENTO DE ERROS
        # Dict para armazenar os erros e exibir no html
        errors = {}
        
        if not username:
            errors["username"] = "Nome de usuário obrigatório"
        
        elif not username.isalnum():
            errors["username"] = "Nome de usuário deve conter apenas números e letras"
        
        # Verifica se username ja está existe no DB
        if username_already_exists(username) == True:
            errors["username"] = "Nome de usuário já existe"
        
        elif len(username) < MIN_USERNAME or len(username) > MAX_USERNAME:
            errors["username"] = "Nome de usuário deve conter entre 4 e 12 caracteres"
        
        if not email:
            errors["email"] = "Email obrigatório"

        # Verifica se email ja está cadastrado no DB
        if email_already_exists(email) == True:
            errors["email"] = "Esse email já está cadastrado"
        
        # Verifica formato do email
        elif email_is_valid(email) == False:
            errors["email"] = "Email inválido"
            
        password_errors = []
        if not password:
            password_errors.append("Senha Obrigatória")

        # Valida força mínima da senha
        if len(password) < MIN_PASSWORD or len(password) > MAX_PASSWORD:
            password_errors.append("Entre 8 e 24 caracteres")
        
        if not any(char.isalpha() for char in password):
            password_errors.append("Ao menos uma letra")
        
        if not any(char.isdigit() for char in password):
            password_errors.append("Ao menos um número")
        
        # Se a lista não está vazia
        if password_errors:
            errors["password"] = password_errors
        
        if not confirmation:
            errors["confirmation"] = "Confirmação obrigatória"
        
        elif confirmation != password:
            errors["confirmation"] = "Confirmação inválida"
        
        # Se houver erros
        if errors:
            return render_template("register.html", errors=errors, username=username, email=email)

        # Tenta inserir o user no BD, caso dê algum erro imprime um aviso 
        try:
            register_user(username, email, password)
            return redirect("/login")
        except Exception as e:
            print("Erro no banco de dados: {e}")
            return apology("Erro interno do servidor. Tente novamente.", 500)
            
    # GET
    # para que register.html rode na primeira vez, passamos dados vazio para ele
    return render_template("register.html", username = "", email = "", errors = "")



@app.route("/login", methods=["GET", "POST"])
def login():
    
    # POST
    if request.method == "POST":
        
        username = request.form.get("username").strip()
        password = request.form.get("password")
        
        # TRATAMENTO DE ERROS
        errors = {}
        
        if not username:
            errors["username"] = "Nome de usuário é obrigatório"
        elif len(username) < MIN_USERNAME or len(username) > MAX_USERNAME:
            errors["user_pass"] = "Usuário ou senha inválidos"
            
        if not password:
            errors["password"] = "Senha é obrigatória"
        elif len(password) < MIN_PASSWORD or len(password) > MAX_PASSWORD or not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
            errors["user_pass"] = "Usuário ou senha inválidos"

        if user_is_registered(username, password) == True:
            session["user_id"] = get_user_id(username)
            return redirect("/")
        else:
            errors["user_pass"] = "Usuário ou senha incorretos"
        
        if errors:
            return render_template("login.html", errors=errors)
    
    # GET
    return render_template("login.html", errors = "")


@app.route("/logout")
def logout():
    # Apaga a sessão
    session.clear()
    return redirect("/login")


@app.route("/categories", methods=["GET", "POST"])
def categories():  
    
    colors = get_colors()
    categories = get_categories_name_color()
    
    # POST
    if request.method == "POST":
        
        category = request.form.get("category").strip()
        color = request.form.get("category_color")
        
        # TRATAMENTO DE ERROS
        errors = {}
        
        if not category:
            errors["category"] = "Nome da categoria obrigatório"
        elif category_already_exists(category):
            errors["category"] = "Essa categoria já existe"
        
        if errors:
            return render_template("categories.html", categories=categories, colors=colors, errors=errors)
            
        # Cor padrão
        if not color:
            color = '#4A5759'
            
        # Insere categoria no BD
        color_id = get_color_id(color)
        insert_category(category, color_id)
    
        return redirect("/categories")
    # GET
    return render_template("categories.html", categories=categories, colors=colors, errors="")


@app.route("/budget", methods=["GET", "POST"])
def budget():
    
    # Printa os orçamentos na tela
    budgets = print_budgets()
    # Seleciona as categorias do user
    categories = get_categories_name_id()
    
    # POST
    if request.method == "POST":
        
        # Retorna o id da categoria que esta no value da option
        category_id = request.form.get("select-category")
        amount = request.form.get("amount").strip()
        
        # TRATAMENTO DE ERROS
        errors = {}
        
        if not category_id:
            errors["category"] = "Categoria obrigatória"
        
        if not amount:
            errors["amount"] = "Quantia obrigatória"
        elif is_nan(amount):
            errors["amount"] = "A quantia deve ser um número"
                
        if errors:
            return render_template("budget.html", categories=categories, budgets=budgets, brl=brl, round=round, abs=abs, errors=errors)
        
        # Insere o orçamento no BD
        insert_budget(category_id, amount)
            
        return redirect("/budget")
    
    # GET
    return render_template("budget.html", categories=categories, budgets=budgets, brl=brl, round=round, abs=abs, errors="")


@app.route("/cash_flow", methods=["GET", "POST"])
def cash_flow():
    
    categories = get_categories_name_id()
    last_transactions = get_transaction_name_amount()
    incomes = get_incomes("", "")
    expenses = get_expenses("", "")
    total_cash = incomes + expenses
    
    # POST
    if request.method == "POST":
        
        form_type = request.form.get("form-type")
        amount = request.form.get("amount") # vem como string
        date = request.form.get("date")
        category_id = request.form.get("category")
        
        # TRATAMENTO DE ERROS
        errors = {}
        
        if form_type == "income":
            
            if not amount:
                errors["amount_income"] = "Valor obrigatório"
            elif is_nan(amount):
                errors["amount_income"] = "O valor deve ser um número"
            else:
                # 1 - Passa str para float  
                # 2 - Força valor positivo
                amount = abs(float(amount))
                if amount == 0:
                    errors["amount_income"] = "O valor deve ser maior que 0"
                    
                
            if not date:
                errors["date_income"] = "Data obrigatória"
                
            if not category_id:
                errors["category_income"] = "Categoria obrigatória"
            
        elif form_type == "expense":
            
            if not amount:
                errors["amount_expense"] = "Valor obrigatório"
            elif is_nan(amount):
                errors["amount_expense"] = "O valor deve ser um número"
            else:
                # 1 - Passa str para float  
                # 2 - Força valor positivo
                amount = float(amount)
                if amount == 0:
                    errors["amount_expense"] = "O valor deve ser maior que 0"
                elif amount > total_cash:
                    errors["amount_expense"] = "Saldo indisponível"
                amount = -abs(amount)
                
            if not date:
                errors["date_expense"] = "Data obrigatória"
                
            if not category_id:
                errors["category_expense"] = "Categoria obrigatória"
            
        if errors:
            return render_template("cash_flow.html", categories=categories, total_cash=total_cash, brl=brl, last_transactions=last_transactions, errors=errors)
        
        insert_transaction(category_id, date, amount) 
        
        return redirect("/cash_flow")   
    
    # GET
    return render_template("cash_flow.html", categories=categories, total_cash=total_cash, brl=brl, last_transactions=last_transactions, errors="")


@app.route("/dashboard")
def dashboard():
    
    # Muda a localização do sistema para traduzir o nome do mês
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    current_date = {}
    current_date["year"] = datetime.now().strftime('%Y')
    # Retorna o nome do mês por extenso em inglês(padrão), capitalize -> 1° letra maiuscula
    current_date["month"] = datetime.now().strftime('%B').capitalize() 

    # Dados vindo do form para filtrar
    month_selected = request.args.get("select-month")
    year_selected = request.args.get("select-year")

    # Dados para serem exibidos
    username = get_user_username()
    years = select_years()
    limit_transactions = 5
    last_transactions = get_transaction_name_amount_date(limit_transactions, month_selected, year_selected)
    total_incomes = get_incomes(month_selected, year_selected)
    total_expenses = get_expenses(month_selected, year_selected)
    budgets = print_budgets_dashboard()
    
    return render_template("dashboard.html", brl=brl, round=round, last_transactions=last_transactions, total_incomes=total_incomes, total_expenses=total_expenses, budgets=budgets, username=username, years=years, current_date=current_date)    


@app.route("/history")
def history():
    
    transactions = get_transactions_history()
    
    return render_template("history.html", brl=brl, transactions=transactions)


# ROTAS PARA VALIDAÇÕES DOS FORMULÁRIOS VIA JS

@app.route("/check_username", methods=["POST"])
def check_username():
    
    # Transforma a string json recebida em um dict
    data = request.get_json()
    username = data.get("username", "").strip() # é case sensitive
    
    if not username:
        return jsonify({"success": False})
    
    # Retorna true ou false 
    response = username_already_exists(username)
    
    if response:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    
    
@app.route("/check_email", methods=["POST"])
def check_email():
    
    # Transforma a string json recebida em um dict
    data = request.get_json()
    email = data.get("email", "").strip()
    
    if not email:
        return jsonify({"success": False})
    
    response = email_already_exists(email)
    
    if response:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    
    
@app.route('/check_user_is_registered', methods=["POST"])
# Se user está registrado retorna True
def check_user_is_registered():
    
    # Transforma a string json recebida em um dict
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    
    if not password or not username:
        return jsonify({"success": False})
    
    response = user_is_registered(username, password)
    
    if response:
        return jsonify({"success": True})
    else:         
        return jsonify({"success": False})


@app.route("/check_category", methods=["POST"])
def check_category():
    
    # Transforma a string json recebida em um dict
    data = request.get_json()
    category = data.get("category", "").strip()
    
    if not category:
        return jsonify({"success": False})
    
    response = category_already_exists(category)
    
    if response:
        return jsonify({"success": True})
    else: 
        return jsonify({"success": False})
    
    
@app.route("/expenses_are_greater_than_total_cash", methods=["POST"])
def expenses_are_greater_than_total_cash():
    
    # Transforma a string json recebida em um dict
    data = request.get_json()
    
    expense = data.get("amount")
    
    if expense is None:
        return jsonify({"success": False})
    
    # Coverte str para float
    expense = float(expense)
    total_cash = get_total_cash()
    
    if expense > total_cash:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    
    
@app.route("/get_spent_by_category")
def get_spent_by_category():
    
    month = request.args.get("month")
    year = request.args.get("year")
    
    datas = spent_by_category(month, year)
    
    if not datas:
        return jsonify({"datas": "empty"})
    else:
        return jsonify({"datas": datas})
    
    
@app.route("/delete_category/<id>", methods=["DELETE"])
def delete_category_by_id(id):
    
    # Ativa as FKs nessa conexão
    # Fazemos isso dentro da função para garantir que esta conexão específica saiba das regras - para DELENTE CASCADE(budgets) e SET NULL(transactions).
    db.execute("PRAGMA foreign_keys = ON;")
    
    delete_category(id)
    
    return jsonify({"success": True})


@app.route('/delete_budget/<id>', methods=["DELETE"])
def delete_budget_by_id(id):
    
    delete_budget(id)
    
    return jsonify({"success": True})


@app.route("/delete_transaction/<id>", methods=["DELETE"])
def delete_transaction_by_id(id):
    
    delete_transaction(id)
    
    return jsonify({"success": True})

import streamlit as st
from sympy import symbols, Eq, sqrt, log, exp, solve, simplify, latex
from sympy import Integer

x = symbols('x')

st.set_page_config(page_title="Ecuații Avansate Interactiv", page_icon="🧮", layout="centered")

def L(expr):
    return f"${latex(expr)}$"

# ----------------- Ecuații logaritmice -----------------
def log_equation_steps(a,b,c):
    steps=[]
    eq = Eq(log(a*x + b), c)
    steps.append(("Ecuația inițială", L(eq)))
    eq1 = Eq(a*x + b, exp(c))
    steps.append(("Ridicăm la exponent", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

# ----------------- Ecuații exponențiale -----------------
def exp_equation_steps(a,b,c):
    steps=[]
    eq = Eq(exp(a*x + b), c)
    steps.append(("Ecuația inițială", L(eq)))
    eq1 = Eq(a*x + b, log(c))
    steps.append(("Aplicăm log natural", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

# ----------------- Ecuații iraționale -----------------
def radical_equation_steps(a,b,c):
    steps=[]
    eq = Eq(sqrt(a*x + b), c)
    steps.append(("Ecuația inițială", L(eq)))
    eq1 = Eq(a*x + b, c**2)
    steps.append(("Ridicăm la pătrat", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

# ----------------- UI -----------------
st.title("🧮 Ecuații Avansate Interactiv")
st.write("Rezolvarea pas cu pas a ecuațiilor logaritmice, exponentiale și iraționale")

mode = st.selectbox("Tipul ecuației", ["Ecuație logaritmică","Ecuație exponențială","Ecuație irațională"])

steps = []

# ----------------- Input și generare pași -----------------
if mode=="Ecuație logaritmică":
    a = st.number_input("a",1)
    b = st.number_input("b",0)
    c = st.number_input("c",1)
    if st.button("Generează pașii"):
        steps = log_equation_steps(a,b,c)

elif mode=="Ecuație exponențială":
    a = st.number_input("a",1)
    b = st.number_input("b",0)
    c = st.number_input("c",2)
    if st.button("Generează pașii"):
        steps = exp_equation_steps(a,b,c)

elif mode=="Ecuație irațională":
    a = st.number_input("a",1)
    b = st.number_input("b",0)
    c = st.number_input("c",2)
    if st.button("Generează pașii"):
        steps = radical_equation_steps(a,b,c)

# ----------------- Afișare pași -----------------
st.divider()
if steps:
    st.subheader("Pașii de rezolvare:")
    for idx, (title, desc) in enumerate(steps, start=1):
        st.markdown(f"**Pas {idx}: {title}**")
        st.markdown(desc)
else:
    st.info("Completează coeficienții și apasă 'Generează pașii' pentru a vedea rezolvarea.")

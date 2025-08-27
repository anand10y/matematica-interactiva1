import streamlit as st
from sympy import symbols, Eq, solve, latex, sqrt, log, exp, Rational

x = symbols('x')

st.set_page_config(page_title="Ecuații Avansate Interactiv", page_icon="🧮", layout="centered")

def L(expr):
    return f"${latex(expr)}$"

# ----------------- Funcții pentru pași -----------------
def log_equation_steps(a, b, c, d):
    steps=[]
    eq = Eq(log(b*x + c, a), d)
    steps.append(("Ecuația inițială", L(eq)))
    eq1 = Eq(b*x + c, a**d)
    steps.append(("Ridicăm la puterea bazei", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

def exp_equation_steps(a, b, c, d):
    steps=[]
    if a == 'e':
        eq = Eq(exp(b*x + c), d)
    else:
        eq = Eq(a**(b*x + c), d)
    steps.append(("Ecuația inițială", L(eq)))
    if a == 'e':
        eq1 = Eq(b*x + c, log(d))
        steps.append(("Aplicăm log natural", L(eq1)))
    else:
        eq1 = Eq(b*x + c, log(d)/log(a))
        steps.append(("Aplicăm log baza a", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

def radical_equation_steps(n, a, b, c):
    steps=[]
    if n==2:
        eq = Eq(sqrt(a*x + b), c)
    else:
        eq = Eq((a*x + b)**Rational(1,3), c)
    steps.append(("Ecuația inițială", L(eq)))
    eq1 = Eq(a*x + b, c**n)
    steps.append((f"Ridicăm la puterea {n}", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

# ----------------- UI -----------------
st.title("🧮 Ecuații Avansate Interactiv")
st.write("Exponențiale, Logaritmice și Iraționale – pași detaliați")

mode = st.selectbox("Tipul ecuației", ["Ecuații exponențiale","Ecuații logaritmice","Ecuații iraționale"])

if "steps" not in st.session_state: st.session_state.steps=[]
if "step_idx" not in st.session_state: st.session_state.step_idx=0
if "show_all" not in st.session_state: st.session_state.show_all=False

def reset_steps(new_steps):
    st.session_state.steps = new_steps
    st.session_state.step_idx = 0

# ----------------- Input pe orizontală -----------------
if mode=="Ecuații logaritmice":
    st.subheader("Ecuație logaritmică: log_b(bx + c) = d")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        a = st.number_input("baza a", 2, step=1)
    with col2:
        b = st.number_input("coeficient b", 1)
    with col3:
        c = st.number_input("constanta c", 0)
    with col4:
        d = st.number_input("d", 1)
    st.latex(r"\log_{a}{(b \cdot x + c)} = d")

elif mode=="Ecuații exponențiale":
    st.subheader("Ecuație exponențială: a^(bx + c) = d")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        a = st.selectbox("baza a", ['e',2,3,5,10])
    with col2:
        b = st.number_input("coeficient b", 1)
    with col3:
        c = st.number_input("constanta c", 0)
    with col4:
        d = st.number_input("d", 2)
    if a=='e':
        st.latex(r"e^{b \cdot x + c} = d")
    else:
        st.latex(rf"{a}^{{{b} \cdot x + {c}}} = {d}")

else:
    st.subheader("Ecuație irațională: radical ordin n")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        n = st.selectbox("ordin radical n", [2,3])
    with col2:
        a = st.number_input("coeficient a",1)
    with col3:
        b = st.number_input("constanta b",0)
    with col4:
        c = st.number_input("d",2)
    if n==2:
        st.latex(r"\sqrt{a \cdot x + b} = c")
    else:
        st.latex(r"\sqrt[3]{a \cdot x + b} = c")

# ----------------- Generează pași -----------------
if st.button("Generează pașii"):
    if mode=="Ecuații logaritmice":
        reset_steps(log_equation_steps(a,b,c,d))
    elif mode=="Ecuații exponențiale":
        reset_steps(exp_equation_steps(a,b,c,d))
    else:
        reset_steps(radical_equation_steps(n,a,b,c))
    st.session_state.show_all=False

# ----------------- Navigare și Vezi toți pașii -----------------
st.divider()
if st.session_state.steps:
    if st.button("Vezi toți pașii"):
        st.session_state.show_all = not st.session_state.show_all

    if st.session_state.show_all:
        st.subheader("Toți pașii:")
        for idx, (title, desc) in enumerate(st.session_state.steps,start=1):
            st.markdown(f"**Pas {idx}: {title}**")
            st.markdown(desc)
    else:
        total = len(st.session_state.steps)
        idx = st.session_state.step_idx
        title, desc = st.session_state.steps[idx]
        st.subheader(f"Pas {idx+1}/{total}: {title}")
        st.markdown(desc)
        c1,c2,c3 = st.columns([1,2,1])
        with c1:
            if st.button("⬅️ Înapoi", disabled=idx==0):
                st.session_state.step_idx -=1
        with c3:
            if st.button("Înainte ➡️", disabled=idx==total-1):
                st.session_state.step_idx +=1
else:
    st.info("Completează parametrii și apasă 'Generează pașii' pentru a vedea rezolvarea.")

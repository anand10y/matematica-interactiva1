import streamlit as st
from sympy import symbols, Eq, sqrt, log, exp, solve, latex

x = symbols('x')

st.set_page_config(page_title="Ecuații Avansate Interactiv", page_icon="🧮", layout="centered")

def L(expr):
    return f"${latex(expr)}$"

# ----------------- Funcții pentru pași -----------------
def log_equation_steps(a,b,c):
    steps=[]
    eq = Eq(log(a*x + b), c)
    steps.append(("Ecuația inițială", L(eq)))
    eq1 = Eq(a*x + b, exp(c))
    steps.append(("Ridicăm la exponent", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

def exp_equation_steps(a,b,c):
    steps=[]
    eq = Eq(exp(a*x + b), c)
    steps.append(("Ecuația inițială", L(eq)))
    eq1 = Eq(a*x + b, log(c))
    steps.append(("Aplicăm log natural", L(eq1)))
    sol = solve(eq1, x)
    steps.append(("Rezolvăm pentru x", f"x = {sol}"))
    return steps

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
st.title("🧮 Ecuații Avansate Interactiv – Elevi")
st.write("Logaritmice, exponențiale și iraționale")

mode = st.selectbox("Tipul ecuației", ["Ecuație logaritmică","Ecuație exponențială","Ecuație irațională"])

if "steps" not in st.session_state: st.session_state.steps=[]
if "step_idx" not in st.session_state: st.session_state.step_idx=0
if "show_all" not in st.session_state: st.session_state.show_all=False

def reset_steps(new_steps):
    st.session_state.steps = new_steps
    st.session_state.step_idx = 0

# ----------------- Input pe orizontală -----------------
col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input("a", 1)
with col2:
    b = st.number_input("b", 0)
with col3:
    c = st.number_input("c", 1)

st.markdown("**Formulă generală:**")
if mode=="Ecuație logaritmică":
    st.latex(r"\log(a \cdot x + b) = c")
elif mode=="Ecuație exponențială":
    st.latex(r"e^{a \cdot x + b} = c")
else:
    st.latex(r"\sqrt{a \cdot x + b} = c")

# ----------------- Generează pași -----------------
if st.button("Generează pașii"):
    if mode=="Ecuație logaritmică":
        reset_steps(log_equation_steps(a,b,c))
    elif mode=="Ecuație exponențială":
        reset_steps(exp_equation_steps(a,b,c))
    else:
        reset_steps(radical_equation_steps(a,b,c))
    st.session_state.show_all = False

# ----------------- Vizualizare pași -----------------
st.divider()

if st.session_state.steps:
    # Buton Vezi toți pașii
    if st.button("Vezi toți pașii"):
        st.session_state.show_all = not st.session_state.show_all

    if st.session_state.show_all:
        st.subheader("Toți pașii:")
        for idx, (title, desc) in enumerate(st.session_state.steps, start=1):
            st.markdown(f"**Pas {idx}: {title}**")
            st.markdown(desc)
    else:
        total = len(st.session_state.steps)
        idx = st.session_state.step_idx
        title, desc = st.session_state.steps[idx]

        st.subheader(f"Pas {idx+1}/{total}: {title}")
        st.markdown(desc)

        c1, c2, c3 = st.columns([1,2,1])
        with c1:
            if st.button("⬅️ Înapoi", disabled=idx==0):
                st.session_state.step_idx -= 1
        with c3:
            if st.button("Înainte ➡️", disabled=idx==total-1):
                st.session_state.step_idx += 1
else:
    st.info("Completează coeficienții și apasă 'Generează pașii' pentru a vedea rezolvarea.")

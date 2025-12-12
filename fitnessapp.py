import streamlit as st
import math

# ======================================================
#                 HELPER FUNCTIONS
# ======================================================

# ---- cm → inch ----
CM_TO_INCH = 0.3937007874
def cm_to_inch(cm): return cm * CM_TO_INCH

# ---- Bodyfat US Navy Formules ----


def bf_male(height, neck, waist):
    h = cm_to_inch(height)
    n = cm_to_inch(neck)
    w = cm_to_inch(waist)
    if w <= n:
        raise ValueError("Taille moet groter zijn dan nek.")
    return 86.010 * math.log10(w - n) - 70.041 * math.log10(h) + 36.76


def bf_female(height, neck, waist, hip):
    h = cm_to_inch(height)
    n = cm_to_inch(neck)
    w = cm_to_inch(waist)
    h2 = cm_to_inch(hip)
    if (w + h2) <= n:
        raise ValueError("Taille + heup moet groter zijn dan nek.")
    return 163.205 * math.log10(w + h2 - n) - 97.684 * math.log10(h) - 78.387

# ---- BMR / TDEE ----


def bmr_mifflin(sex, weight, height, age):
    if sex == "Man":
        return 10 * weight + 6.25 * height - 5 * age + 5
    return 10 * weight + 6.25 * height - 5 * age - 161


activity_levels = {
    "Weinig of geen sport": 1.2,
    "Licht actief (1–3x/week)": 1.375,
    "Matig actief (3–5x/week)": 1.55,
    "Zeer actief (6–7x/week)": 1.725,
    "Extreem actief (2x per dag)": 1.9
}

# ======================================================
#                 STREAMLIT INTERFACE
# ======================================================

st.set_page_config(page_title="Fitness App", page_icon="💪")

st.title("💪 Fitness Calculator App")
tab1, tab2 = st.tabs(["📏 Bodyfat Calculator", "🔥 Kcal / TDEE Calculator"])

# ======================================================
#                  TAB 1 – BODYFAT
# ======================================================

with tab1:

    st.header("📏 Bodyfat Calculator (US Navy)")

    sex = st.radio("Geslacht", ["Man", "Vrouw"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Lengte (cm)", 50.0, 250.0, 170.0)
        neck = st.number_input("Nekomtrek (cm)", 20.0, 80.0, 40.0)

    waist = st.number_input("Tailleomtrek (cm)", 30.0, 200.0, 85.0)

    hip = None
    if sex == "Vrouw":
        hip = st.number_input("Heupomtrek (cm)", 30.0, 200.0, 95.0)

    if st.button("Bereken vetpercentage"):
        try:
            if sex == "Man":
                bf = bf_male(height, neck, waist)
            else:
                bf = bf_female(height, neck, waist, hip)

            bf = max(0, min(bf, 75))  # clamp
            st.success(f"Je vetpercentage: **{bf:.1f}%**")

        except ValueError as e:
            st.error(str(e))

# ======================================================
#                  TAB 2 – KCAL / TDEE
# ======================================================

with tab2:

    st.header("🔥 Kcal & TDEE Calculator (Mifflin-St Jeor)")

    sex2 = st.radio("Geslacht (kcal)", ["Man", "Vrouw"], horizontal=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Gewicht (kg)", 20.0, 250.0, 77.0)
    with col2:
        height2 = st.number_input("Lengte (cm)", 120.0, 250.0, 169.0)
    with col3:
        age = st.number_input("Leeftijd", 10, 100, 30)

    activity = st.selectbox("Activiteit", list(activity_levels.keys()))
    factor = activity_levels[activity]

    if st.button("Bereken caloriebehoefte"):
        bmr = bmr_mifflin(sex2, weight, height2, age)
        tdee = bmr * factor

        st.success(f"✨ BMR: **{bmr:.0f} kcal/dag**")
        st.success(f"🔥 TDEE (onderhoud): **{tdee:.0f} kcal/dag**")

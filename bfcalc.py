import streamlit as st
import math

# ============================
# Conversie constant
# ============================
CM_TO_INCH = 0.3937007874


def cm_to_inch(cm: float) -> float:
    """Converteert centimeters naar inches."""
    return cm * CM_TO_INCH


# ============================
# US NAVY FORMULES
# ============================

def bf_male(height_cm: float, neck_cm: float, waist_cm: float) -> float:
    """Bereken vetpercentage voor mannen volgens US Navy formule."""
    if height_cm <= 0 or neck_cm <= 0 or waist_cm <= 0:
        raise ValueError("Lengte, nek en taille moeten groter zijn dan 0.")

    h = cm_to_inch(height_cm)
    n = cm_to_inch(neck_cm)
    w = cm_to_inch(waist_cm)

    if w <= n:
        raise ValueError("Bij mannen moet taille groter zijn dan nek.")

    bf = 86.010 * math.log10(w - n) - 70.041 * math.log10(h) + 36.76
    return bf


def bf_female(height_cm: float, neck_cm: float, waist_cm: float, hip_cm: float) -> float:
    """Bereken vetpercentage voor vrouwen volgens US Navy formule."""
    if height_cm <= 0 or neck_cm <= 0 or waist_cm <= 0 or hip_cm <= 0:
        raise ValueError(
            "Lengte, nek, taille en heup moeten groter zijn dan 0.")

    h = cm_to_inch(height_cm)
    n = cm_to_inch(neck_cm)
    w = cm_to_inch(waist_cm)
    hip = cm_to_inch(hip_cm)

    if (w + hip) <= n:
        raise ValueError(
            "Bij vrouwen moet (taille + heup) groter zijn dan nek.")

    bf = 163.205 * math.log10(w + hip - n) - 97.684 * math.log10(h) - 78.387
    return bf


# ============================
# STREAMLIT UI
# ============================

st.set_page_config(
    page_title="Bodyfat Calculator (US Navy)",
    page_icon="📏",
    layout="centered"
)

st.title("📏 Bodyfat Calculator (US Navy Methode)")
st.caption(
    "Input in centimeters • Automatische conversie naar inches • Formules per geslacht")

# Geslacht kiezen
sex = st.radio("Geslacht", ["Man", "Vrouw"], horizontal=True)

# Inputvelden (gemeenschappelijk)
col1, col2 = st.columns(2)
with col1:
    height_cm = st.number_input(
        "Lengte (cm)",
        min_value=50.0,
        max_value=250.0,
        value=170.0,
        step=0.1
    )
with col2:
    neck_cm = st.number_input(
        "Nekomtrek (cm)",
        min_value=20.0,
        max_value=80.0,
        value=40.0,
        step=0.1
    )

waist_cm = st.number_input(
    "Tailleomtrek (cm)",
    min_value=30.0,
    max_value=200.0,
    value=85.0,
    step=0.1
)

hip_cm = None
if sex == "Vrouw":
    hip_cm = st.number_input(
        "Heupomtrek (cm)",
        min_value=30.0,
        max_value=200.0,
        value=95.0,
        step=0.1
    )

# =====================================
# BEREKEN BUTTON
# =====================================

if st.button("Bereken vetpercentage"):
    try:
        if sex == "Man":
            bf = bf_male(height_cm, neck_cm, waist_cm)
        else:
            bf = bf_female(height_cm, neck_cm, waist_cm, hip_cm)

        # Veiligheids clamp
        bf = max(0.0, min(bf, 75.0))

        st.success(f"Geschat vetpercentage: **{bf:.1f}%**")
        st.info(
            "Tip: meet altijd op hetzelfde tijdstip (bijvoorbeeld 's ochtends nuchter).")

    except ValueError as e:
        st.error(str(e))
    except Exception:
        st.error("Er is een onverwachte fout opgetreden. Controleer je input.")

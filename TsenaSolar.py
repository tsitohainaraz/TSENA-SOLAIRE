import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Tsena Solaire Malagasy",
    page_icon="☀️",
    layout="wide"
)

# Configuration CSS personnalisée
st.markdown("""
<style>
    .main-header {
        color: #FF6B00;
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sub-header {
        color: #2E86C1;
        font-size: 1.8em;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .result-box {
        background-color: #F4F6F6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF6B00;
        margin: 15px 0;
    }
    .price-box {
        background-color: #E8F8F5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .stButton > button {
        background-color: #FF6B00;
        color: white;
        font-weight: bold;
        padding: 10px 24px;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #E65B00;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<div class="main-header">☀️ TSENA SOLAIRE MALAGASY ☀️</div>', unsafe_allow_html=True)
st.markdown("### Plateforme de Devis Automatique d'Énergie Solaire")

# Initialisation des données
if 'materiels' not in st.session_state:
    st.session_state.materiels = []

# Section 1: Saisie des matériels
st.markdown('<div class="sub-header">1. Saisie de vos équipements</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    nom = st.text_input("Nom du matériel", key="nom")
with col2:
    puissance_unitaire = st.number_input("Puissance (W)", min_value=1, step=1, key="puissance")
with col3:
    quantite = st.number_input("Quantité", min_value=1, step=1, key="quantite")
with col4:
    heures_jour = st.number_input("Heures/jour", min_value=0.0, step=0.5, key="heures_jour")
with col5:
    heures_nuit = st.number_input("Heures/nuit", min_value=0.0, step=0.5, key="heures_nuit")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("➕ Ajouter l'équipement"):
        if nom:
            puissance_totale = puissance_unitaire * quantite
            energie_jour = puissance_totale * heures_jour
            energie_nuit = puissance_totale * heures_nuit
            
            st.session_state.materiels.append({
                "Nom": nom,
                "Puissance unitaire (W)": puissance_unitaire,
                "Quantité": quantite,
                "Puissance totale (W)": puissance_totale,
                "Heures/jour": heures_jour,
                "Energie jour (Wh)": energie_jour,
                "Heures/nuit": heures_nuit,
                "Energie nuit (Wh)": energie_nuit
            })
            st.success(f"✅ {nom} ajouté!")
        else:
            st.warning("Veuillez entrer un nom pour le matériel")

with col_btn2:
    if st.button("🗑️ Réinitialiser la liste"):
        st.session_state.materiels = []
        st.success("Liste réinitialisée!")

# Affichage du tableau des matériels
if st.session_state.materiels:
    df_materiels = pd.DataFrame(st.session_state.materiels)
    st.markdown("#### 📋 Liste de vos équipements")
    st.dataframe(df_materiels, use_container_width=True)
    
    # Calculs totaux
    total_puissance = df_materiels["Puissance totale (W)"].sum()
    total_energie_jour = df_materiels["Energie jour (Wh)"].sum()
    total_energie_nuit = df_materiels["Energie nuit (Wh)"].sum()
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.metric("Puissance totale installée", f"{total_puissance:,.0f} W")
    with col_t2:
        st.metric("Énergie consommée de jour", f"{total_energie_jour:,.0f} Wh")
    with col_t3:
        st.metric("Énergie consommée de nuit", f"{total_energie_nuit:,.0f} Wh")
else:
    st.info("💡 Commencez par ajouter vos équipements ci-dessus")

# Section 2: Configuration du système
st.markdown('<div class="sub-header">2. Configuration de votre système solaire</div>', unsafe_allow_html=True)

col_config1, col_config2, col_config3 = st.columns(3)

with col_config1:
    st.markdown("#### 🔋 Batteries")
    type_batterie = st.selectbox(
        "Type de batteries",
        ["Batterie Acide", "Batteries Gel", "Batteries Lithium LFP04"]
    )
    marque_batterie = st.selectbox(
        "Marque de batteries",
        ["HAISIC", "SRNE", "CHINA ESS"]
    )

with col_config2:
    st.markdown("#### ☀️ Panneaux solaires")
    puissance_panneau = st.selectbox(
        "Puissance des panneaux",
        [60, 80, 110, 210, 550, 580]
    )
    
    # Information sur les panneaux
    st.markdown('<div class="price-box">', unsafe_allow_html=True)
    st.markdown("**Prix des panneaux:**")
    st.markdown("- 110W: 130.000 Ar")
    st.markdown("- 210W: 180.000 Ar")
    st.markdown("- 550W: 500.000 Ar")
    st.markdown("- 580W: 600.000 Ar")
    st.markdown('</div>', unsafe_allow_html=True)

with col_config3:
    st.markdown("#### 🔌 Convertisseur Hybride")
    marque_convertisseur = st.selectbox(
        "Marque du convertisseur",
        ["SRNE", "HAISIC", "HONG FENG"]
    )
    
    # Informations sur les convertisseurs
    st.markdown('<div class="price-box">', unsafe_allow_html=True)
    st.markdown("**Gammes de prix:**")
    st.markdown("- 1000W: 300.000 - 500.000 Ar")
    st.markdown("- 2000W: 500.000 - 800.000 Ar")
    st.markdown("- 3000W: 800.000 - 1.200.000 Ar")
    st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Génération du devis
st.markdown('<div class="sub-header">3. Génération du devis</div>', unsafe_allow_html=True)

if st.button("🚀 Générer mon devis complet", type="primary"):
    if not st.session_state.materiels:
        st.error("⚠️ Veuillez d'abord ajouter au moins un équipement!")
    else:
        # Calculs avancés
        energie_jour_totale = total_energie_jour
        energie_nuit_totale = total_energie_nuit
        energie_totale_quotidienne = energie_jour_totale + energie_nuit_totale
        
        # Calcul avec rendement (85% pour les pertes)
        rendement_systeme = 0.85
        energie_panneau_requise = energie_totale_quotidienne / rendement_systeme
        
        # Heures d'ensoleillement à Madagascar (moyenne)
        heures_ensoleillement = 5.5
        
        # Calcul nombre de panneaux
        energie_panneau_jour = puissance_panneau * heures_ensoleillement
        nombre_panneaux = np.ceil(energie_panneau_requise / energie_panneau_jour)
        
        # Calcul capacité batterie
        autonomie_jours = 2  # Autonomie souhaitée en jours
        profondeur_decharge = {
            "Batterie Acide": 0.5,
            "Batteries Gel": 0.7,
            "Batteries Lithium LFP04": 0.8
        }[type_batterie]
        
        capacite_batterie_wh = (energie_nuit_totale * autonomie_jours) / profondeur_decharge
        # Supposons des batteries de 12V 100Ah = 1200Wh
        capacite_batterie_unit = 1200
        nombre_batteries = np.ceil(capacite_batterie_wh / capacite_batterie_unit)
        
        # Calcul puissance convertisseur
        marge_securite = 1.25
        puissance_convertisseur = total_puissance * marge_securite
        
        # Calcul des prix
        prix_panneaux = {
            60: 80000, 80: 100000, 110: 130000,
            210: 180000, 550: 500000, 580: 600000
        }[puissance_panneau]
        
        prix_batteries = {
            "Batterie Acide": {"HAISIC": 150000, "SRNE": 180000, "CHINA ESS": 120000},
            "Batteries Gel": {"HAISIC": 250000, "SRNE": 300000, "CHINA ESS": 220000},
            "Batteries Lithium LFP04": {"HAISIC": 450000, "SRNE": 500000, "CHINA ESS": 400000}
        }[type_batterie][marque_batterie]
        
        # Prix convertisseur basé sur puissance
        if puissance_convertisseur <= 1000:
            prix_conv = 300000
        elif puissance_convertisseur <= 2000:
            prix_conv = 500000
        else:
            prix_conv = 800000
        
        # Calcul coûts
        cout_panneaux = nombre_panneaux * prix_panneaux
        cout_batteries = nombre_batteries * prix_batteries
        cout_convertisseur = prix_conv
        cout_accessoires = 200000  # Câbles, régulateurs, etc.
        
        cout_total = cout_panneaux + cout_batteries + cout_convertisseur + cout_accessoires
        
        # Affichage des résultats
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### 📊 RÉSULTATS DE VOTRE CONSOMMATION")
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.metric("Énergie utilisée le jour", f"{energie_jour_totale:,.0f} Wh")
            st.metric("Énergie utilisée la nuit", f"{energie_nuit_totale:,.0f} Wh")
            st.metric("Énergie totale quotidienne", f"{energie_totale_quotidienne:,.0f} Wh")
        
        with col_r2:
            st.metric("Énergie à produire (avec rendement)", f"{energie_panneau_requise:,.0f} Wh")
            st.metric("Nombre de panneaux solaires", int(nombre_panneaux))
            st.metric("Nombre de batteries", int(nombre_batteries))
        
        st.markdown(f"**Puissance du convertisseur recommandée:** {puissance_convertisseur:,.0f} W")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Devis détaillé
        st.markdown("### 💰 DEVIS DÉTAILLÉ")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("#### Détail des coûts")
            st.markdown(f"**Panneaux solaires ({int(nombre_panneaux)} × {puissance_panneau}W):**")
            st.markdown(f"- Prix unitaire: {prix_panneaux:,} Ar")
            st.markdown(f"- Total: **{cout_panneaux:,} Ar**")
            
            st.markdown(f"**Batteries ({int(nombre_batteries)} × {type_batterie}):**")
            st.markdown(f"- Marque: {marque_batterie}")
            st.markdown(f"- Prix unitaire: {prix_batteries:,} Ar")
            st.markdown(f"- Total: **{cout_batteries:,} Ar**")
            
            st.markdown(f"**Convertisseur hybride:**")
            st.markdown(f"- Marque: {marque_convertisseur}")
            st.markdown(f"- Puissance: {puissance_convertisseur:,.0f} W")
            st.markdown(f"- Prix: **{cout_convertisseur:,} Ar**")
            
            st.markdown(f"**Accessoires (câbles, régulateur, etc.):**")
            st.markdown(f"- Estimation: **{cout_accessoires:,} Ar**")
        
        with col_d2:
            st.markdown("#### 🧾 RÉCAPITULATIF FINANCIER")
            st.markdown('<div class="price-box">', unsafe_allow_html=True)
            st.markdown(f"### TOTAL HT: **{cout_total:,} Ar**")
            st.markdown(f"### TVA (20%): **{cout_total * 0.2:,.0f} Ar**")
            st.markdown(f"### TOTAL TTC: **{cout_total * 1.2:,.0f} Ar**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("#### 📅 Validité du devis")
            st.info(f"Ce devis est valable jusqu'au {(datetime.now().replace(day=30) + pd.DateOffset(months=1)).strftime('%d/%m/%Y')}")
        
        # Option de téléchargement
        st.markdown("---")
        st.markdown("### 📥 Exporter votre devis")
        
        # Création d'un rapport texte
        rapport = f"""
        DEVIS TSENA SOLAIRE MALAGASY
        =============================
        Date: {datetime.now().strftime('%d/%m/%Y')}
        
        CONSOMMATION ESTIMÉE:
        - Énergie jour: {energie_jour_totale:,.0f} Wh
        - Énergie nuit: {energie_nuit_totale:,.0f} Wh
        - Énergie totale: {energie_totale_quotidienne:,.0f} Wh/jour
        
        SYSTÈME RECOMMANDÉ:
        - Panneaux solaires: {int(nombre_panneaux)} × {puissance_panneau}W
        - Batteries: {int(nombre_batteries)} × {type_batterie} ({marque_batterie})
        - Convertisseur: {marque_convertisseur} {puissance_convertisseur:,.0f}W
        
        DÉTAIL DES COÛTS:
        1. Panneaux solaires: {cout_panneaux:,} Ar
        2. Batteries: {cout_batteries:,} Ar
        3. Convertisseur: {cout_convertisseur:,} Ar
        4. Accessoires: {cout_accessoires:,} Ar
        
        TOTAL HT: {cout_total:,} Ar
        TVA (20%): {cout_total * 0.2:,.0f} Ar
        TOTAL TTC: {cout_total * 1.2:,.0f} Ar
        
        Validité: 30 jours
        """
        
        st.download_button(
            label="📄 Télécharger le devis (PDF)",
            data=rapport,
            file_name=f"devis_tsena_solaire_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# Section 4: Informations supplémentaires
with st.expander("ℹ️ Informations importantes"):
    st.markdown("""
    ### Notes techniques:
    
    **Hypothèses de calcul:**
    - Rendement système: 85% (pertes incluses)
    - Autonomie: 2 jours
    - Heures d'ensoleillement: 5.5h/jour (moyenne Madagascar)
    
    **Profondeur de décharge:**
    - Batterie Acide: 50%
    - Batteries Gel: 70%
    - Batteries Lithium: 80%
    
    **Garanties:**
    - Panneaux: 25 ans
    - Batteries: 2-5 ans selon type
    - Convertisseur: 2 ans
    
    **Services inclus:**
    - Étude technique gratuite
    - Installation professionnelle
    - Formation à l'utilisation
    - Support technique 24/7
    """)

# Pied de page
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>☀️ <b>Tsena Solaire Malagasy</b> - Votre partenaire en énergie solaire à Madagascar</p>
        <p>📞 Contact: +261 34 00 000 00 | ✉️ contact@tsenasolaire.mg</p>
        <p>📍 Antananarivo, Madagascar</p>
    </div>
    """,
    unsafe_allow_html=True
)
import streamlit as st
import plotly.express as px
from pathlib import Path
import os 
from PIL import Image


from src.data_filter import DataFilter
from src.helper import load_data

import warnings 
warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="Tableau de Bord des Ventes",
    page_icon=":bar_chart:", 
    layout="wide"
)

style_path = Path("./templates/css/style.css")
file_css = open(style_path, "r", encoding="utf-8")
st.markdown(f"<style>{file_css.read()}</style>", unsafe_allow_html=True)

st.title(" :bar_chart: Analyse des Ventes Adidas : Tendances et Performances ")
st.markdown(f"<style> <br> <br> </style>", unsafe_allow_html=True)

data_path = Path("./data/processed/sales_adidas.csv")
data = load_data(data_path)

image_path = Path("./templates/image/adidas.png")
image = Image.open(image_path)

#--------------------------------SIDEBAR------------------#
st.sidebar.image(image, caption='')
with st.sidebar.expander(label="Description"):
    st.sidebar.markdown(
        "Adidas, une entreprise allemande fondée en 1949,\
        est devenue l'un des plus importants fabricants mondiaux d'articles de sport.\
        Spécialisée dans les chaussures, les vêtements et les accessoires,\
        la société jouit d'une renommée internationale dans les domaines\
        de la mode et du sport grâce à sa présence étendue à l'échelle mondiale."
    )
st.sidebar.title("Paramètres de Filtrage")
regions = st.sidebar.multiselect(
    label="Région", 
    options= data["Region"].unique()
)

years = st.sidebar.multiselect(
    label="Année", 
    options= data["Year"].unique()
)

products = st.sidebar.multiselect(
    label="Produits", 
    options= data["Product"].unique()
)


#---------------------------Filtrer le Dataframe ------------#

filter = DataFilter()
filtered_df = filter.filter_data(data, regions, years, products)
try:
    #-------------------------------KPIs Units Sold ---------------------#
    
    df_quarter = filter.filter_Quarter(filtered_df, years)
    year = df_quarter["Year"].unique()[0]
    def taux_evaluation(q1, q2):
        count_q1 = df_quarter[df_quarter["Quarter"]==q1].values.reshape(-1)[-1]  
        count_q2 = df_quarter[df_quarter["Quarter"]==q2].values.reshape(-1)[-1]
        return 100*(count_q2 - count_q1)/count_q1


    
    #--------------------Filtrer le Dataframe Sans Les Dates-------------#
    month_df = filter.filter_data_no_year(filtered_df, regions, products)

    #--------------------------------taux Units Solds ----------------------#
    st.subheader("Évolution de la Quantité de Ventes par Trimestre")
    with st.expander(label="Description"):
        st.markdown(
            "La section 'Évolution de la Quantité de Ventes par Trimestre'\
            présente une analyse détaillée de la variation du volume des ventes\
            de produits Adidas au cours de chaque trimestre. \
            Cette étude permet de comprendre comment la quantité de produits\
            vendus a évolué au fil des périodes spécifiques de l'année, \
            segmentées en trimestres. Cette représentation permet de voir rapidement\
            et clairement les variations dans les ventes trimestrielles,\
            ce qui peut fournir des informations précieuses\
            pour la prise de décisions commerciales stratégiques. "
        )
    st.markdown("<style> <br> <br> </style>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        vent_1 = df_quarter[df_quarter["Quarter"]==1].values.reshape(-1)[-1]
        tau_1 = taux_evaluation(q1=1, q2=1)
        st.metric(
        label=f"Ventes T1 {year}", 
        value=f'{vent_1}', 
        delta= f'{round(tau_1, 3)}%')

    with col2:
        vent_2 = df_quarter[df_quarter["Quarter"]==2].values.reshape(-1)[-1]
        tau_2 = taux_evaluation(q1=1, q2=2)
        st.metric(
            label=f"Ventes T2 {year}", 
            value=f'{vent_2}', 
            delta= f'{round(tau_2, 3)}%'
        )

    with col3:
        vent_3 = df_quarter[df_quarter["Quarter"]==3].values.reshape(-1)[-1]
        tau_3 = taux_evaluation(q1=2, q2=3)
        st.metric(
            label=f"Ventes T3 {year}", 
            value=f'{vent_3}', 
            delta= f'{round(tau_2, 3)}%')
    with col4:
        vent_4 = df_quarter[df_quarter["Quarter"]==4].values.reshape(-1)[-1]
        tau_4 = taux_evaluation(q1=3, q2=4)
        st.metric(
            label=f"Ventes T4 {year}", 
            value=f'{vent_4}', 
            delta= f'{round(tau_4, 3)}%'
        )

    #------------------Evolution des Sales par State-------------------#
    df_state = filtered_df[["Gender", "State", "Total Sales"]].groupby(by=["State", "Gender"], as_index=False).sum()
    df_state_sort = df_state.sort_values(by="Total Sales", ascending=False)
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        st.subheader("Tendance des ventes de produits en ($) selon les différents États")
        with st.expander(label="Description"):
            st.markdown("Cette section offre une analyse approfondie \
                de l'évolution des ventes de produits Adidas,\
                mesurées en dollars, réparties selon les différents États.\
                En examinant ces tendances de ventes par État, regroupées par sexe,\
                les décideurs peuvent identifier les régions où les produits Adidas\
                rencontrent le plus de succès et celles qui nécessitent\
                peut-être une attention particulière,\
                en tenant compte des préférences en fonction du genre.")

        fig_s = px.bar(data_frame=df_state_sort, 
                    x="State", y="Total Sales", 
                    color="Gender", barmode="group", 
                    color_discrete_map= {"Male":"blue", "Female":"red"})

        st.plotly_chart(fig_s, use_container_width=True)

    with col_s2:
        st.subheader("Quantité de Ventes par Détaillant")
        with st.expander(label="Description"):
            st.markdown("Cette étude présente une analyse détaillée\
                de la quantité de produits Adidas vendus\
                par différents détaillants. Elle met en lumière les\
                performances de vente spécifiques à chaque détaillant.\
                En examinant ces données, nous pouvons identifier\
                les détaillants qui connaissent le plus de succès\
                dans la vente de produits Adidas.")
        df_ret = filtered_df[["Retailer", "Units Sold"]].groupby("Retailer", as_index=False).sum()
        fig_s2 = px.bar(data_frame=df_ret, x="Retailer", y="Units Sold", color="Retailer")
        st.plotly_chart(fig_s2, use_container_width=True)
    #-----------------Retailer Par Sales Method -----------------#
    st.subheader("Distribution des ventes en fonction de la méthode de vente pour chaque détaillant")
    with st.expander(label="Description"):
        st.markdown("Cette étude offre une analyse détaillée de la répartition des ventes\
                de produits Adidas en fonction de la méthode de vente,\
                spécifique à chaque détaillant.\
                Chaque camembert représente un détaillant, \
                où les parts de chaque tranche correspondent\
                à la méthode de vente utilisée.")
    st.markdown("<style> <br> <br> </style>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns(3)
    retailers = filtered_df["Retailer"].unique()
    with col_r1 :
        try:
            st.subheader(retailers[0])
            df_foot = filtered_df[filtered_df["Retailer"] == retailers[0]][["Units Sold",
                                                                        "Sales Method"]].groupby("Sales Method",
                                                                                                as_index=False).sum()
            fig = px.pie(df_foot, values="Units Sold", names="Sales Method", hole=0.5)
            fig.update_traces(text = df_foot["Sales Method"], textposition = "inside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass
        try:
            st.subheader(retailers[1])
            df_foot = filtered_df[filtered_df["Retailer"] == retailers[1]][["Units Sold",
                                                                        "Sales Method"]].groupby("Sales Method",
                                                                                                as_index=False).sum()
            fig = px.pie(df_foot, values="Units Sold", names="Sales Method", hole=0.5)
            fig.update_traces(text = df_foot["Sales Method"], textposition = "inside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass
        

    #---------------------------------COL1-------------------#
    with col_r2 :
        try:
            st.subheader(retailers[3])
            df_foot = filtered_df[filtered_df["Retailer"] == retailers[3]][["Units Sold",
                                                                        "Sales Method"]].groupby("Sales Method",
                                                                                                as_index=False).sum()
            fig = px.pie(df_foot, values="Units Sold", names="Sales Method", hole=0.5)
            fig.update_traces(text = df_foot["Sales Method"], textposition = "inside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass
        try:
            st.subheader(retailers[4])
            df_foot = filtered_df[filtered_df["Retailer"] == retailers[4]][["Units Sold",
                                                                        "Sales Method"]].groupby("Sales Method",
                                                                                                as_index=False).sum()
            fig = px.pie(df_foot, values="Units Sold", names="Sales Method", hole=0.5)
            fig.update_traces(text = df_foot["Sales Method"], textposition = "inside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass

    with col_r3:
        try:
            st.subheader(retailers[2])
            df_foot = filtered_df[filtered_df["Retailer"] == retailers[2]][["Units Sold",
                                                                    "Sales Method"]].groupby("Sales Method",
                                                                                            as_index=False).sum()
            fig = px.pie(df_foot, values="Units Sold", names="Sales Method", hole=0.5)
            fig.update_traces(text = df_foot["Sales Method"], textposition = "inside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass
        
        try:
            st.subheader(retailers[5])
            df_foot = filtered_df[filtered_df["Retailer"] == retailers[5]][["Units Sold",
                                                                        "Sales Method"]].groupby("Sales Method",
                                                                                                as_index=False).sum()
            fig = px.pie(df_foot, values="Units Sold", names="Sales Method", hole=0.5)
            fig.update_traces(text = df_foot["Sales Method"], textposition = "inside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        except:
            pass

    colm_1, colm_2 = st.columns([2, 1])
    with colm_1:
        st.subheader("Évolution des Ventes Mensuelles par Année")
        with st.expander(label="Description"):
            st.markdown("La section 'Évolution des Ventes Mensuelles par Année'\
                présente une analyse détaillée de l'évolution des ventes de produits\
                Adidas au cours de chaque mois, pour les années 2020 et 2021.\
                Cette visualisation permet d'observer les variations \
                et les tendances générales des ventes de produits Adidas\
                au fil de ces deux années. Le graphique montre les tendances\
                de vente mensuelles pour ces deux années, avec chaque ligne \
                représentant une année différente. Les marqueurs facilitent \
                l'identification des points spécifiques de chaque mois.")
        fig_m = px.line(data_frame=month_df, x="Month", y="Total Sales", 
                    color="Year", markers=True, 
                    color_discrete_map={"2020":"red"})
        st.plotly_chart(fig_m, use_container_width=True)

    with colm_2:
        st.subheader("Répartition des Bénéfices par Genre, Détaillant et Méthode de Vente")
        with st.expander(label="Description") :
            st.markdown("La section 'Répartition des Bénéfices par Genre, Détaillant et Méthode de Vente'\
                offre une analyse approfondie de la distribution des bénéfices générés \
                par les ventes de produits Adidas, en prenant en compte trois facteurs essentiels\
                : le genre des clients, le détaillant et la méthode de vente. \
                Cette visualisation fournit une vue globale de la manière\
                dont les bénéfices sont distribués en fonction du genre des clients,\
                du détaillant et de la méthode de vente.")
        fig_m2 = px.sunburst(data_frame=filtered_df, 
                    path= ["Gender", "Retailer", "Sales Method"], 
                    values= "Operating Profit", hover_data=["Operating Profit"], 
                    color="Retailer", branchvalues="total")
        #fig_m2.update_layout(width=800, height=650)
        st.plotly_chart(fig_m2, use_container_width=True)
except:
    pass
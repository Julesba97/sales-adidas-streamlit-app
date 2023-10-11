import pandas as pd
from .logger import logger

class DataFilter:
    def __init__(self) -> None:
        pass
    def filter_data(self, data, regions, years, products) -> pd.DataFrame:
        """
        Filtre les données d'entrée en fonction de critères spécifiés.

        Args:
            data (pd.DataFrame): Le DataFrame d'entrée contenant les données à filtrer.
            regions (list): Une liste de noms de régions à inclure dans les données filtrées.
            years (list): Une liste d'années à inclure dans les données filtrées.
            products (list): Une liste de noms de produits à inclure dans les données filtrées.

        Returns:
            pd.DataFrame: Un DataFrame contenant les données filtrées.
        """
        try :
            if not regions:
                regions = data["Region"].unique()
            if not years: 
                years = data["Year"].unique()
            if not products:
                products = data["Product"].unique()
            logger.info(f"Les régions sélectionnées pour le filtrage des données : {regions}")
            logger.info(f"Années sélectionnées pour le filtrage des données : {years}")
            logger.info(f"Produits sélectionnés pour le filtrage des données : {products}")
            
            filtered_df = data[(data["Region"].isin(regions)) & 
                            (data["Year"].isin(years)) & 
                            (data["Product"].isin(products))]
            logger.info("Le DataFrame filtré a été retourné avec succès.")
            return filtered_df
        except Exception as e:
            logger.exception(e)
    
    def filter_data_no_year(self, data, regions, products) -> pd.DataFrame:
        """
        Filtre les données d'entrée en fonction des régions et des produits spécifiés.

        Args:
            data (pd.DataFrame): Le DataFrame d'entrée contenant les données à filtrer.
            regions (list): Une liste de noms de régions à inclure dans les données filtrées.
            products (list): Une liste de noms de produits à inclure dans les données filtrées.

        Returns:
            pd.DataFrame: Un DataFrame contenant les données filtrées.
        """
        data_ = data.copy()
        try:
            if not regions:
                regions = data_["Region"].unique()
            if not products:
                products = data_["Product"].unique()
            logger.info(f"Les régions sélectionnées pour le filtrage des données : {regions}")
            logger.info(f"Produits sélectionnés pour le filtrage des données : {products}")
            filtered_df= data_[(data_["Region"].isin(regions)) & (data_["Product"].isin(products))]
            month_df = filtered_df[["Year", "Month", "Month Name", "Total Sales"]].groupby(by=["Year", "Month Name", "Month"],
                                                                            as_index=False).sum()
            month_df = month_df.sort_values(by="Month")
            month_df = month_df.drop(columns=["Month"])
            month_df.rename(columns={'Month Name': 'Month'}, inplace=True)
            
            logger.info("Le DataFrame de Total Sales par mois a été créé avec succès.")
            return month_df
        except Exception as e:
            logger.exception(e)
            
    def filter_Quarter(self, data, years) -> pd.DataFrame:
        """
        Filtre les données en fonction des trimestres spécifiés.

        Args:
            data (pd.DataFrame): Le DataFrame d'entrée contenant les données à filtrer.
            years (list): Une liste d'années à inclure dans les données filtrées.

        Returns:
            pd.DataFrame: Un DataFrame contenant les données filtrées.
        """
        data_ = data.copy()
        group_quarter_df = data_[["Year", "Quarter", "Units Sold"]].groupby(by=["Year","Quarter"],
                                                                        as_index=False).count()
        group_quarter_20_df = group_quarter_df[group_quarter_df["Year"]==2020]
        group_quarter_21_df = group_quarter_df[group_quarter_df["Year"]==2021] 
        
        if len(years) == 2 or len(years) == 0 or 2021 in years:
            return group_quarter_21_df
        else:
            return group_quarter_20_df
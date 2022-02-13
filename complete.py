from itertools import product
import pandas as pd
from typing import List


class Complete:
    """complete function to replication the complete() function in R dplyr"""

    def __init__(self, df: pd.DataFrame, columns:List, nest=None, fill=None):
        self.df = df
        self.nest = nest
        if all(isinstance(x, str) for x in columns):
            self.columns = [self.df[c] for c in columns]
            self.column_names = columns
        elif all(isinstance(x, pd.Series) for x in columns):
            self.columns = columns
            self.column_names = [col.name for col in columns]  

        self.fill = fill    

    def nesting(self) -> List[str]:
        """
        Generate all possible existing combinations in the columns defind in `nest`
        """
        return self.df[self.nest].drop_duplicates(keep="first").values.tolist()

    def product_without_nest(self) -> pd.DataFrame:
        def get_product():
            product_list = []

            for series in self.columns:
                product_list.append(list(set(series)))

            col_list = (self.column_names)

            df = pd.DataFrame(list(product(*product_list)), columns=col_list)
            return df

        def merge_product_to_df():
            """
            """
        
            all_headers = self.column_names
            complete_df = self.get_product_2()
    
            df_full = pd.merge(
                    complete_df,
                    self.df,
                    how="left",
                    on=all_headers)
        
            return df_full

        return merge_product_to_df    

    def product_with_nest(self):
        def get_product():
            """

            """
            product_list = []
            product_list.append(self.nesting())
            for series in self.columns:
                product_list.append(list(set(series)))

            col_list = ["nest"] + (self.column_names)

            df = pd.DataFrame(list(product(*product_list)), columns=col_list)
            return df

        def merge_product_to_df():
            """
            """
        
            all_headers = self.nest + self.column_names
            complete_df = get_product()

            complete_df2 = pd.DataFrame(
                complete_df["nest"].values.tolist(),
                columns=self.nest)

            complete_df2[self.column_names] = complete_df[self.column_names] 
            del complete_df   
            df_full = pd.merge(
                    complete_df2,
                    self.df,
                    how="left",
                    on=all_headers)
        
            return df_full
        
        return merge_product_to_df()

    
    def fill_df(self, df):
        for key in self.fill:
            df[key] = df[key].fillna(self.fill[key])

        return df    
 


    def run(self):
        """
        """
        if self.fill != None:
            if self.nest != None:
                return self.fill_df(self.product_with_nest())
            elif self.nest == None:
                return self.fill_df(self.product_without_nest())
                
        elif self.fill == None:
            if self.nest != None:
                return self.product_with_nest()
            elif self.nest == None:
                return self.product_without_nest()


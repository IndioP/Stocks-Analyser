from constants import *

import re
import pandas as pd
import streamlit as st

SHOW_ADD_PRODUCTS_SESSION = False

class Bridges():
    def __init__(self) -> None:
        if 'show_add_products_session' not in st.session_state:
            st.session_state['show_add_products_session'] = False
        
        if 'data' not in st.session_state:
            st.session_state['data'] = pd.DataFrame.from_dict(structure)
        
    def __main__(self) -> None: 
        self.add_product = st.button("Adicionar produto")
        print("Cheguei aqui!")
        
        if self.add_product == CLICKED:
            st.session_state['show_add_products_session'] = True
        
        if st.session_state['show_add_products_session']:
            self.__show_options_add_product__()
        
        st.text(st.session_state)
    
    def __update__table__(self):
        self.main_table = st.dataframe(st.session_state['data'])
    
    def __hide_options_add_product__(self):
        self.add_product_btn_dif = None
        self.add_product_clothing_type = None
        self.add_product_product_amount = None
        self.add_product_add_button = None
    
    def __show_options_add_product__(self):
        with st.form(key='add_product_form'):
            print("Estou em show_product")
            c_type = self.add_product_clothing_type = st.text_input("Tipo da roupa: ", key=random_id(10))
            dif = self.add_product_btn_dif = st.selectbox("Dificuldade: ", range(1, 11), key=random_id(10))
            amount = self.add_product_product_amount = st.number_input("Quantidade: ", key=random_id(10))
            
            cost = self.add_product_product_cost = st.text_input("Custo de produção: ", placeholder='R$ ', key=random_id(10))
            if not re.match(r'^-?\d+(?:\,\d+)$', cost) is None:
                st.text("Insira um número válido!")
            
            n_pieces = self.add_product_n_pieces_to_make = st.number_input("Peças para costurar: ", key=random_id(10))
            if n_pieces and n_pieces.isdigit():
                st.text("Insira um número válido!")
            
            price = self.add_product_product_price = st.text_input("Preço: ", placeholder='R$ ', key=random_id(10))
            if not re.match(r'^-?\d+(?:\,\d+)$', price) is None:
                st.text("Insira um número válido!")
            
            btn = self.add_product_add_btn = st.form_submit_button("Adicionar")
            
        if btn:
            st.session_state['data'] = pd.concat([pd.DataFrame.from_dict({
                "Tipo da peça": [c_type],
                "Dificuldade": [dif],
                "Quantidade": [amount],
                "Custo de produção": [cost],
                "Peças para costurar": [n_pieces],
                "Preço": [price]
            }), st.session_state['data']])
            st.success("Produto adicionado com sucesso!")
            st.session_state['show_add_products_session'] = False
            self.__hide_options_add_product__()
            return


if __name__ == '__main__':
    app = Bridges()
    app.__main__()

from typing import Any

import pandas as pd
import streamlit as st

from swedeb_demo.api.dummy_api import ADummyApi  # type: ignore
from swedeb_demo.components.meta_data_display import MetaDataDisplay  # type: ignore


class ToolTab:
    def __init__(
        self, another_api: ADummyApi, shared_meta: MetaDataDisplay, tab_key: str
    ):
        self.api = another_api
        self.search_display = shared_meta
        self.TAB_KEY = tab_key
        self.HITS_PER_PAGE = f"{self.TAB_KEY}_hits_per_page"

    def init_session_state(self, session_dict: dict) -> None:
        for k, v in session_dict.items():
            if k not in st.session_state:
                st.session_state[k] = v

    def get_search_box(self) -> str:
        if f"search_box_{self.TAB_KEY}" not in st.session_state:
            return ""
        return st.session_state[f"search_box_{self.TAB_KEY}"]

    def handle_search_click(self, st_dict_when_button_clicked: dict) -> bool:
        for k, v in st_dict_when_button_clicked.items():
            st.session_state[k] = v

    def display_settings_info(
        self, n_hits: int, with_search_hits: bool = True, hits: str = ""
    ) -> None:
        settings = self.search_display.get_current_settings()
        if with_search_hits:
            searches = f"{self.get_search_box()}"

            st.info(
                f"Resultat för sökningen `{searches}` {hits}  \n\n{settings}"
                f"\n\n**Antal träffar:** {n_hits}"
            )
        else:
            st.info(
                f"Resultat för sökningen: \n \n{settings}"
                f"\n\n**Antal träffar:** {n_hits}"
            )

    def display_settings_info_no_hits(self, with_search_hits: bool = True) -> None:
        settings = self.search_display.get_current_settings()
        searches = f"{self.get_search_box()}"

        if with_search_hits:
            st.info(
                f"Inga resultat för sökningen `{searches}`.  "
                f"\n{settings}  \n Utöka filtreringen eller försök med "
                "ett annat sökord för att få fler träffar."
            )
        else:
            st.info(
                f"Inga resultat för sökningen:  \n{settings}.  \n"
                "Utöka filtreringen för att få fler träffar."
            )

    def add_hit_selector(self, hits: list) -> Any:
        hit_selector = st.multiselect(
            label="Välj ord att inkludera",
            options=hits,
            default=hits,
        )

        return hit_selector

    def draw_line(self) -> None:
        st.markdown(
            """<hr style="height:2px;border:none;color:#111111;background-color:#111111;" /> """,  # noqa: E501
            unsafe_allow_html=True,
        )

    @st.cache_data
    def convert_df(_self, df: pd.DataFrame, index: bool) -> bytes:
        df_down = df.copy()
        if "Protokoll" in df_down.columns:
            # remove number from protocoll string
            df_down["Protokoll"] = df_down["Protokoll"].apply(lambda x: x.split("_")[0])
        return df_down.to_csv(index=index).encode("utf-8")

    def add_download_button(
        self,
        data: pd.DataFrame,
        file_name: str,
        button_label: str = None,
        index: bool = False,
    ) -> None:
        st.download_button(
            label="Ladda ner som csv" if button_label is None else button_label,
            data=self.convert_df(data, index),
            file_name=file_name,
            mime="text/csv",
        )

    def get_sort_direction(self, key) -> None:
        if key not in st.session_state:
            st.session_state[key] = True
        else:
            st.session_state[key] = not st.session_state[key]
        return st.session_state[key]

    def add_hits_per_page(self, key):
        st.selectbox(
            "Antal resultat per sida",
            options=[5, 10, 20, 50],
            key=key,
        )

    def has_and_is(self, key):
        if key not in st.session_state:
            return False
        return st.session_state[key]

    def set_sorting(self, sorting_key):
        st.session_state[self.ASCENDING_KEY] = self.get_sort_direction(
            f"{sorting_key}_{self.TAB_KEY}"
        )
        st.session_state[self.SORT_KEY] = sorting_key
        self.table_display.reset_page()

    def add_search_button(self, message: str) -> None:
        st.button(
            message,
            key=f"search_button_{self.TAB_KEY}",
            on_click=self.handle_button_click,
        )

    def add_sort_button(self, text, column_name):
        st.button(
            text,
            key=f"sb_{column_name}_{self.TAB_KEY}",
            on_click=self.set_sorting,
            args=(column_name,),
        )

    def add_sort_buttons(self, texts, st_columns, column_names):
        for text, st_col, col_name in zip(texts, st_columns, column_names):
            with st_col:
                self.add_sort_button(text, col_name)

import math
from typing import Any

import pandas as pd
import streamlit as st


class TableDisplay:
    def __init__(
        self,
        current_container_key: str,
        current_page_name: str,
        party_abbrev_to_color: dict,
        expanded_speech_key: str,
        table_type: str,
        data_key: str,
    ) -> None:
        self.top_container = st.container()
        self.table_container = st.container()
        self.prev_next_container = st.container()

        self.current_container = current_container_key
        self.current_page_name = current_page_name
        self.table_type = table_type
        self.data_key = data_key
        self.hits_per_page = st.session_state["hits_per_page_all"]
        self.type = type
        dummy_pdf = "https://www.riksdagen.se/sv/sok/?avd=dokument&doktyp=prot"
        self.link = f"[protokoll]({dummy_pdf})"
        self.party_colors = party_abbrev_to_color
        self.expanded_speech_key = expanded_speech_key

    def get_next_button_id(self) -> str:
        if "button_id" not in st.session_state:
            st.session_state["button_id"] = 0
        else:
            st.session_state["button_id"] += 1
        return st.session_state["button_id"]

    def write_table(self) -> None:
        if self.data_key in st.session_state:
            current_page, max_pages = self.get_current_page(
                len(st.session_state[self.data_key])
            )
            current_df = self.get_current_df(current_page)
            with self.table_container:
                if self.table_type == "table":
                    self.display_partial_table(current_df)
                elif self.table_type == "kwic":
                    # self.display_partial_kwic(st.session_state[self.data_key])
                    self.display_partial_kwic(current_df)
                else:
                    self.display_partial_source(current_df)

            self.add_buttons(current_page, max_pages)

    def get_current_df(self, current_page):
        return st.session_state[self.data_key].iloc[
            current_page
            * self.hits_per_page : ((current_page + 1) * self.hits_per_page)
        ]

    def get_current_page(self, n_rows):
        current_page = st.session_state[self.current_page_name]
        max_pages = math.ceil(n_rows / self.hits_per_page) - 1
        if current_page > max_pages:
            st.session_state[self.current_page_name] = 0
            current_page = 0
        return current_page, max_pages

    def add_buttons(self, current_page: int, max_pages: int) -> None:
        with self.prev_next_container:
            button_col_v, _, info_col, _, button_col_h = st.columns([1, 1, 1, 1, 1])

            if current_page > 0:
                button_col_v.button(
                    "Föregående",
                    key=f"{self.current_container}_F",
                    on_click=self.decrease_page,
                )
            if current_page < max_pages:
                button_col_h.button(
                    "Nästa",
                    key=f"{self.current_container}_B",
                    on_click=self.increase_page,
                )
            info_col.caption(
                f"Sida {current_page + 1} av {max_pages + 1}."
                f" Totalt {len(st.session_state[self.data_key])} träffar."
            )

    def display_partial_table(self, current_df: pd.DataFrame) -> None:
        st.dataframe(current_df.style.format(thousands=" "))

    def display_partial_source(self, current_df: pd.DataFrame) -> None:
        for i, row in current_df.iterrows():
            self.write_wt_row(i, row)

    def display_partial_kwic(self, current_df: pd.DataFrame) -> None:
        for i, row in current_df.iterrows():
            self.write_kwic_row(i, row)

    def get_party_with_color(self, party: str) -> str:
        if party == "?":
            return "Metadata saknas"
        if party in self.party_colors:
            color = self.party_colors[party]
            return f'<p style="color:{color}";>{party}</p>'
        return party

    def update_speech_state(
        self, protocol: str, speaker: str, year: str, hit=None
    ) -> None:
        st.session_state[self.expanded_speech_key] = True
        st.session_state["selected_protocol"] = protocol
        st.session_state["selected_speaker"] = speaker
        st.session_state["selected_year"] = year
        if hit is not None:
            st.session_state["selected_hit"] = hit

    def get_kwick_columns(self) -> Any:
        return st.columns([3, 3, 3, 2, 2, 2, 2, 2])

    def write_kwic_row(self, i: int, row: pd.Series) -> None:
        (
            left_col,
            hit_col,
            right_col,
            party_col,
            year_col,
            speaker_col,
            gender_col,
            prot_col,
            # expander_col,
        ) = self.get_kwick_columns()
        # gender_col.write(self.translate_gender(["Kön"], short=True))
        speaker = "Metadata saknas" if row["Talare"] == "" else row["link"]
        speaker_col.write(speaker)
        party_col.markdown(
            self.get_party_with_color(row["Parti"]), unsafe_allow_html=True
        )

        year_col.write(str(row["År"]))
        with prot_col:
            st.button(
                "Visa",
                key=f"{self.current_container}_b_kwic_{self.get_next_button_id()}",
                on_click=self.update_speech_state,
                args=(row["Protokoll"], speaker, row["År"], row["Sökord"]),
            )
        left_col.write(row["Kontext Vänster"])
        hit_col.markdown(f"**{row['Sökord']}**")
        right_col.write(row["Kontext Höger"])
        gender_col.write(self.translate_gender(row["Kön"], short=True))

    def write_wt_row(self, i: int, row: pd.Series) -> None:
        if "hit" in row:
            (
                speaker_col,
                gender_col,
                year_col,
                party_col,
                link_col,
                hit_col,
                expander_col,
            ) = self.get_columns(include_hit=True)
            hit_col.write(row["hit"])
        else:
            (
                speaker_col,
                year_col,
                gender_col,
                party_col,
                link_col,
                expander_col,
            ) = self.get_columns(include_hit=False)

        gender_col.write(self.translate_gender(row["Kön"]))
        speaker = "Metadata saknas" if row["Talare"] == "" else row["link"]
        speaker_col.write(speaker)
        year_col.write(str(row["År"]))
        party_col.markdown(
            self.get_party_with_color(row["Parti"]), unsafe_allow_html=True
        )
        with link_col:
            st.write(
                self.link.replace(
                    "protokoll", self.translate_protocol(row["Protokoll"])
                ),
                unsafe_allow_html=True,
            )
        with expander_col:
            hit = None
            if "hit" in row:
                hit = row["hit"]

            st.button(
                "Visa hela",
                key=f"{self.current_container}_b_wt_{self.get_next_button_id()}",
                on_click=self.update_speech_state,
                args=(row["Protokoll"], speaker, row["År"], hit),
            )

    def translate_gender(self, gender: str, short: bool = False) -> str:
        if gender == "man":
            if short:
                return "M"
            return "Man"
        elif gender == "woman":
            if short:
                return "K"
            return "Kvinna"
        else:
            if short:
                return "?"
            return "Okänt"

    def get_columns(self, include_hit=False) -> Any:
        if include_hit:
            return st.columns([2, 2, 1, 1, 2, 2, 2])
        else:
            return st.columns([2, 2, 1, 1, 2, 2])

    def increase_page(self) -> None:
        st.session_state[self.current_page_name] += 1

    def decrease_page(self) -> None:
        st.session_state[self.current_page_name] -= 1

    def reset_page(self) -> None:
        st.session_state[self.current_page_name] = 0

    @st.cache_data
    def convert_df(_self, df: pd.DataFrame) -> bytes:
        return df.to_csv(index=False).encode("utf-8")

    def translate_protocol(self, protocol_name: str) -> str:
        split = protocol_name.split("-")
        if "fk" in protocol_name or "ak" in protocol_name:
            chamber = split[3]
            chamber = chamber.replace("ak", "Andra kammaren")
            chamber = chamber.replace("fk", "Första kammaren")
            year = split[1]
            return f"{chamber} {year}:{split[5].split('_')[0]}"
        else:
            year_and_number = split[1]
        return f"{year_and_number[0:4]}:{year_and_number[4:]} "

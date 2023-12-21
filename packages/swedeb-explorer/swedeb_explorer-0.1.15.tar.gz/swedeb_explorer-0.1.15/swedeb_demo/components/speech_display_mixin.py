import streamlit as st

from swedeb_demo.api.dummy_api import ADummyApi  # type: ignore


class ExpandedSpeechDisplay:
    def display_expanded_speech(
        self,
        reset_dict: dict,
        api: ADummyApi,
        tab_key: str,
        search_hit: str = None,
    ) -> None:
        if (
            "selected_protocol" in st.session_state
            and st.session_state["selected_protocol"] is not None
        ):
            selected_protocol = st.session_state["selected_protocol"]
            if "ak" in selected_protocol or "fk" in selected_protocol:
                ch = "kammaren"

                ch = "kammaren"
                chamber = f"Andra {ch}" if "ak" in selected_protocol else f"Första {ch}"

                simplified_protocol = (
                    selected_protocol.split("-")[1]
                    + ":"
                    + selected_protocol.split("-")[5].split("_")[0]
                )
            else:
                chamber = ""
                simplified_protocol = selected_protocol.split("-")[1]
            dummy_pdf = "https://www.riksdagen.se/sv/sok/?avd=dokument&doktyp=prot"
            link = f"[{simplified_protocol}]({dummy_pdf})"
            col_1, col_3 = st.columns([3, 1])
            speaker_intro = api.get_speaker_note(selected_protocol)

            with col_1:
                info_text = f"""
                **Talare**: {st.session_state['selected_speaker']}  
                
                **År**: {st.session_state['selected_year']}  

                **Hela protokollet** {link}, {chamber}
                
                **Talarintroduktion**: {speaker_intro}

                """

                st.info(info_text)

            with col_3:
                st.button(
                    "Stäng och återgå",
                    key=f"close_button_{tab_key}",
                    on_click=self.reset_speech_state,
                    args=(reset_dict,),
                )
            st.write("**Hela anförandet:**")

            text = api.get_speech_text(st.session_state["selected_protocol"])
            # causes InvalidCharacterError: The string contains invalid characters.
            text = text.replace("<", " ").replace(">", " ")

            text = text.replace("\n", "<br><br>")
            if search_hit is not None:
                if search_hit not in text:
                    search_hit = search_hit.lower()
                    if search_hit not in text:
                        search_hit = search_hit.capitalize()
                text = text.replace(
                    search_hit,
                    f'<span style="background-color: #FFFF00">{search_hit}</span>',
                )
            st.markdown(
                f'<p style="border-width:2px; border-style:solid; border-color:#000000; padding: 1em;">{text}</p>',  # noqa: E501
                unsafe_allow_html=True,
            )

    def reset_speech_state(self, reset_dict: dict) -> None:
        st.session_state["selected_protocol"] = None
        for k, v in reset_dict.items():
            st.session_state[k] = v

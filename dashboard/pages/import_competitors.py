import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from services.competitor_import_service import CompetitorImportService


def show():

    st.header("Import Competitors")

    st.write(
        "Upload a TXT file containing competitor website URLs. "
        "Use one URL per line."
    )

    uploaded_file = st.file_uploader(
        "Choose a TXT file",
        type=["txt"]
    )

    if uploaded_file is not None:

        try:
            content = uploaded_file.getvalue().decode("utf-8-sig")

            st.subheader("File Preview")

            st.code(content, language="text")

            if st.button("Import Competitors", type="primary"):

                db = SessionLocal()

                try:
                    service = CompetitorImportService(db)

                    results = service.import_from_text(content)

                    st.success(
                        f"{len(results['imported'])} competitors imported."
                    )

                    st.info(
                        f"{len(results['duplicates'])} duplicates skipped."
                    )

                    st.warning(
                        f"{len(results['invalid'])} invalid entries."
                    )

                    if results["imported"]:

                        st.subheader("Imported Competitors")

                        st.dataframe(
                            pd.DataFrame(results["imported"]),
                            use_container_width=True
                        )

                    if results["duplicates"]:

                        st.subheader("Duplicates")

                        st.write(results["duplicates"])

                    if results["invalid"]:

                        st.subheader("Invalid Entries")

                        st.dataframe(
                            pd.DataFrame(results["invalid"]),
                            use_container_width=True
                        )

                finally:
                    db.close()

        except UnicodeDecodeError:

            st.error(
                "Unable to read this file. Please upload a UTF-8 TXT file."
            )
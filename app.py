
import streamlit as st
import pandas as pd

def load_text_file(file, delimiter):
    try:
        return pd.read_csv(file, delimiter=delimiter)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def main():
    st.title("Library Inventory Comparison Tool (Text File Version)")

    st.markdown("""Upload your **Horizon export** file (tab-separated) and your **inventory wand** file (comma-separated).

Both files must include a header row. They should both have a **Barcode** column to match on.""")

    export_file = st.file_uploader("Upload Horizon Export File (TSV)", type=["txt", "tsv"])
    scanned_file = st.file_uploader("Upload Scanned Inventory File (CSV)", type=["csv", "txt"])

    if export_file and scanned_file:
        export_df = load_text_file(export_file, delimiter='\t')
        scanned_df = load_text_file(scanned_file, delimiter=',')

        if export_df is not None and scanned_df is not None:
            try:
                export_df["Barcode"] = export_df["Barcode"].astype(str)
                scanned_df["Barcode"] = scanned_df["Barcode"].astype(str)

                status_options = sorted(export_df["Item Status"].dropna().unique().tolist())
                selected_statuses = st.multiselect("Select item statuses to include in the comparison:", status_options, default=["Checked In", "Lost"])

                filtered_export = export_df[export_df["Item Status"].isin(selected_statuses)]
                missing_items = filtered_export[~filtered_export["Barcode"].isin(scanned_df["Barcode"])]

                st.success(f"Comparison complete. {len(missing_items)} items not found in scanned inventory.")
                st.dataframe(missing_items)

                csv = missing_items.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Missing Items Report",
                    data=csv,
                    file_name="missing_items_text_input.csv",
                    mime="text/csv",
                )

            except KeyError as e:
                st.error(f"Missing expected column: {e}")

if __name__ == "__main__":
    main()

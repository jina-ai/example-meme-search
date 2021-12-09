import streamlit as st
import random
import os
from config import image_endpoint, text_endpoint, top_k, images_path
from helper import search_by_file, search_by_text, UI, create_temp_file

endpoint = image_endpoint
matches = []

# Layout
st.set_page_config(page_title="Jina meme search")
st.markdown(
    body=UI.css,
    unsafe_allow_html=True,
)
st.write(
    "<style>div.row-widget.stRadio > div{flex-direction:row; margin-left:auto; margin-right: auto; align: center}</style>",
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.markdown(UI.about_block, unsafe_allow_html=True)

st.markdown(UI.repo_banner, unsafe_allow_html=True)

st.header("What do you want to search with?")
media_type = st.radio("", ["Text", "Image"])

if media_type == "Image":
    upload_cell, preview_cell = st.columns([12, 1])
    query = upload_cell.file_uploader("")
    if query:
        uploaded_image = create_temp_file(query)
        preview_cell.image(uploaded_image)
        if st.button(label="Search"):
            if not query:
                st.markdown("Please enter a query")
            else:
                matches = search_by_file(image_endpoint, "/tmp/query.png")

elif media_type == "Text":
    query = st.text_input("", key="text_search_box")
    search_fn = search_by_text
    if st.button("Search", key="text_search"):
        matches = search_by_text(query, text_endpoint, top_k)
    st.subheader("...or search from a sample")
    sample_texts = [
        "squidward school",
        "so you're telling me willy wonka",
        "seagull kitkat",
    ]
    for text in sample_texts:
        if st.button(text):
            matches = search_by_text(text, text_endpoint, top_k)


# Results area
cell1, cell2, cell3 = st.columns(3)
cell4, cell5, cell6 = st.columns(3)
cell7, cell8, cell9 = st.columns(3)
all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

for cell, match in zip(all_cells, matches):
    if media_type == "Text":
        cell.image("http:" + match["tags"]["image_url"])
    else:
        cell.image(match["uri"], use_column_width="auto")

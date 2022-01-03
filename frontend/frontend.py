import streamlit as st
from config import IMAGE_PORT, IMAGE_SERVER, DEBUG, TEXT_PORT, TEXT_SERVER, TEXT_SAMPLES
from helper import search_by_file, search_by_text, UI, convert_file_to_document, get_image_url

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

if DEBUG:
    with st.sidebar.expander("Debug"):
        TEXT_SERVER = st.text_input(label="Text server", value=TEXT_SERVER)
        TEXT_PORT = st.text_input(label="Text port", value=TEXT_PORT)
        IMAGE_SERVER = st.text_input(label="Image server", value=IMAGE_SERVER)
        IMAGE_PORT = st.text_input(label="Image port", value=IMAGE_PORT)

st.markdown(UI.repo_banner, unsafe_allow_html=True)

st.header("What do you want to search with?")
media_type = st.radio("", ["Text", "Image"])

if media_type == "Image":
    upload_cell, preview_cell = st.columns([12, 1])
    query = upload_cell.file_uploader("")
    if query:
        doc = convert_file_to_document(query)
        if st.button(label="Search"):
            if not query:
                st.markdown("Please enter a query")
            else:
                matches = search_by_file(document=doc, server=IMAGE_SERVER, port=IMAGE_PORT)

elif media_type == "Text":
    query = st.text_input("", key="text_search_box")
    search_fn = search_by_text
    if st.button("Search", key="text_search"):
        matches = search_by_text(input=query, server=TEXT_SERVER, port=TEXT_PORT)
    st.subheader("...or search from a sample")
    
    for text in TEXT_SAMPLES:
        if st.button(text):
            matches = search_by_text(input=text, server=TEXT_SERVER, port=TEXT_PORT)


# Results area
cell1, cell2, cell3 = st.columns(3)
cell4, cell5, cell6 = st.columns(3)
cell7, cell8, cell9 = st.columns(3)
all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

for cell, match in zip(all_cells, matches):
    if media_type == "Text":
        cell.image("http:" + match.tags["image_url"])
    else:
        cell.image(get_image_url(match.uri), use_column_width="auto")
        # cell.image(match.uri, use_column_width="auto")

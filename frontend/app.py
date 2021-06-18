import streamlit as st
from frontend_config import frontend_endpoint, images_path
import requests

image_size = 128


def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(frontend_endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches


# layout
max_width = 1200
padding = 2


st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Jina Meme Search")
# modality = st.sidebar.radio(label="I want to search using...", options=('Text', 'Image'))

# if modality == "Text":
query = st.text_input(label="Search for a meme based on caption")
# else:
    # query = st.file_uploader("Upload image")

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:
        # Set up grid
        cell1, cell2, cell3 = st.beta_columns(3)
        cell4, cell5, cell6 = st.beta_columns(3)
        cell7, cell8, cell9 = st.beta_columns(3)

        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        matches = get_data(query=query, endpoint=frontend_endpoint, top_k=10)
        for cell, match in zip(all_cells, matches):
            # st.write(match["tags"])
            cell.image('http:'+match["tags"]["image_url"])
            # st.image(images_path+match["tags"]["image_name"])

        # for match in matches:
            # col1, col2 = st.beta_columns([1, 4])
            # with col1:
                # st.image(match["tags"]["Icon URL"])

            # with col2:
                # app_name = f'**[{sanitize_string(match["tags"]["Name"])}]({match["tags"]["URL"]})**'
                # app_rating = f'{get_star_string(match["tags"]["Average User Rating"])}'
                # app_genres = f'<small>{match["tags"]["Genres"]}</small>'
                # app_desc = shorten_string(sanitize_string(match["text"]), word_count=50)

                # st.markdown(f"""
                            # {app_name}\t{app_rating}\n
                            # {app_genres}\n
                            # {app_desc}
                            # """, unsafe_allow_html=True)

                # st.markdown(
                    # f'**[{sanitize_string(match["tags"]["Name"])}]({match["tags"]["URL"]})**     {get_star_string(match["tags"]["Average User Rating"])}'
                # )
                # st.markdown(f'<small>{match["tags"]["Genres"]}</small>', unsafe_allow_html=True)
                # st.markdown(
                    # f'{shorten_string(sanitize_string(match["text"]), word_count=50)}'
                # )
                # st.button(
                    # label=get_price_string(match["tags"]["Price"]), key=match["id"]
                # )

st.sidebar.title("Jina Meme Search")
st.sidebar.markdown(
    """
This is an example meme search engine using the [Jina neural search framework](https://github.com/jina-ai/jina/).

**Note: click the search button instead of hitting Enter. We're working on fixing this!**

- Backend: [Jina](https://github.com/jina-ai/jina/)
- Frontend: [Streamlit](https://www.streamlit.io/)

[Visit the repo](https://github.com/alexcg1/jina-app-store-example)

<a href="https://github.com/jina-ai/jina/"><img src="https://github.com/alexcg1/jina-app-store-example/blob/a8f64332c6a5b3ae42df07d4bd615ff1b7ece4d9/frontend/powered_by_jina.png?raw=true" width=256></a>
""", unsafe_allow_html=True
)

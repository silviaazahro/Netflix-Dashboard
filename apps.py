# Importing the required modules
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# Reading the CSV file
url_data = 'https://github.com/silviaazahro/Netflix-/raw/main/cleaned_data.csv'
df = pd.read_csv(url_data)

# Ensure all genre values are in lowercase
df['genre'] = df['genre'].str.lower()

# Dashboard title
st.title("Netflix Streaming Dashboard 2024")

# Netflix logo
img = Image.open('Netflix_Logo.png')
st.sidebar.image(img)

# Sidebar for page selection
page = st.sidebar.selectbox("Choose The Page", ["Genre Distribution", "Most Streamed", "Descriptive Statistics"])

if page == "Genre Distribution":
    # List all unique genres
    all_genres = df['genre'].str.split(',').explode().str.strip().unique()
    all_genres = sorted(set(all_genres))  # Sort and remove duplicates
    
    # Dropdown for selecting a genre
    selected_genre = st.sidebar.selectbox("Select Genre", all_genres)
    
    # Filter the DataFrame based on the selected genre
    filtered_df = df[df['genre'].str.contains(selected_genre, case=False, na=False)]
    
    # Displaying genre distribution for the selected genre
    st.subheader(f"Top 10 Shows in {selected_genre} Genre")

    # Get the top 10 shows based on votes (or use rating if you prefer)
    top_10_shows = filtered_df.sort_values(by='votes', ascending=False).head(10)

    # Visualization of top 10 shows
    fig = px.bar(
        top_10_shows,
        x='votes',
        y='title',
        color='votes',
        color_continuous_scale='blues',
        title=f'Top 10 Shows in {selected_genre} Genre',
        labels={'votes': 'Votes', 'title': 'Show Title'},
        text='votes'
    )
    fig.update_layout(
        yaxis_title='Show Title',
        xaxis_title='Votes',
        yaxis=dict(
            tickmode='array',
            tickvals=top_10_shows['title'],
            ticktext=[t if len(t) <= 50 else t[:47] + '...' for t in top_10_shows['title']],
            autorange='reversed'
        ),
        xaxis=dict(tickformat=',')
    )
    
    # Adjusting y-axis to rotate labels
    fig.update_yaxes(tickangle=-45)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Displaying the top 10 shows table
    st.table(top_10_shows[['title', 'year', 'rating', 'votes']].reset_index(drop=True))

elif page == "Most Streamed":
    # Most Streamed visualization options
    statistic_option = st.sidebar.selectbox(
        "Choose The Statistics",
        ["Top 10 Most Streamed", "Top 10 Most Popular"]
    )

    if statistic_option == "Top 10 Most Streamed":
        # Sort by 'votes' and get the top 10 shows
        top_10_streamed = df.sort_values(by='votes', ascending=False).head(10)

        st.subheader("Top 10 Most Streamed Netflix Shows 2024")
        
        # Visualization of the top 10 streamed shows
        fig = px.bar(
            top_10_streamed,
            x='votes',
            y='title',
            color='votes',
            color_continuous_scale='reds',
            title='Top 10 Most Streamed Netflix Shows 2024',
            labels={'votes': 'Votes', 'title': 'Show Title'},
            text='votes'
        )
        fig.update_layout(
            yaxis_title='Show Title',
            xaxis_title='Votes',
            yaxis=dict(
                tickmode='array',
                tickvals=top_10_streamed['title'],
                ticktext=[t if len(t) <= 50 else t[:47] + '...' for t in top_10_str

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION (Dark Theme) ---
st.set_page_config(
    page_title="IPL Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set Streamlit's default theme to dark mode via a config file or st.set_page_config.
# For a truly 'attractive dark theme', you can add a file in a folder:
# .streamlit/config.toml
# With the following content:
# [theme]
# primaryColor="#FF4B4B"  # IPL-like accent color (red/orange)
# backgroundColor="#0E1117"
# secondaryBackgroundColor="#262730"
# textColor="#FAFAFA"
# font="sans serif"

# --- TITLE & HEADER ---
st.title("🏏 IPL Data Analysis Dashboard")
st.markdown("---") # Horizontal line for separation

# --- BUTTONS for Navigation ---
 #st.sidebar.header("Navigation")
analysis_option = st.sidebar.radio(
    "Select Analysis",
    ('Home', 'Best Batsman', 'Best Bowler', 'Top Teams Performance')
)

# --- CACHING DATA LOAD (Speed up app) ---
# Use st.cache_data to load data only once
@st.cache_data
def load_data():
    try:
        # Adjust paths if needed
        match_df = pd.read_csv('data/matches.csv')
        delivery_df = pd.read_csv('data/deliveries.csv')
    except FileNotFoundError:
        st.error("Data files (matches.csv or deliveries.csv) not found in the 'data' folder. Please check your path.")
        st.stop()
    return match_df, delivery_df

match_df, delivery_df = load_data()



def get_best_batsman(delivery_df, top_n=10):
    """Calculates the top N batsmen by total runs."""
    batsman_runs = delivery_df.groupby('batsman')['batsman_runs'].sum().reset_index()
    top_batsmen = batsman_runs.sort_values(by='batsman_runs', ascending=False).head(top_n)
    return top_batsmen

def plot_batsman_runs(df):
    """Generates a Matplotlib bar chart for top batsmen."""
    # Set the dark theme style for Matplotlib
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Custom colors for a better dark-mode visual
    bars = ax.bar(df['batsman'], df['batsman_runs'], color='#FF4B4B', edgecolor='white') 
    
    ax.set_title(f'Top {len(df)} Batsmen by Total Runs', color='white', fontsize=16)
    ax.set_xlabel('Batsman', color='white')
    ax.set_ylabel('Total Runs', color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 50, int(yval), 
                ha='center', va='bottom', color='white', fontsize=10)
    
    plt.tight_layout()
    return fig

def get_best_bowler(delivery_df, top_n=10):
    """Calculates the top N bowlers by total wickets."""
    # Consider only 'wicket' dismissal types (not run outs)
    wickets = delivery_df[delivery_df['dismissal_kind'].isin(['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'])]
    
    bowler_wickets = wickets.groupby('bowler')['dismissal_kind'].count().reset_index(name='Wickets Taken')
    top_bowlers = bowler_wickets.sort_values(by='Wickets Taken', ascending=False).head(top_n)
    return top_bowlers

def plot_bowler_wickets(df):
    """Generates a Matplotlib bar chart for top bowlers."""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Custom colors
    bars = ax.bar(df['bowler'], df['Wickets Taken'], color='#00FFFF', edgecolor='white') # Cyan for bowlers
    
    ax.set_title(f'Top {len(df)} Bowlers by Total Wickets', color='white', fontsize=16)
    ax.set_xlabel('Bowler', color='white')
    ax.set_ylabel('Total Wickets', color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), 
                ha='center', va='bottom', color='white', fontsize=10)
    
    plt.tight_layout()
    return fig

def get_top_teams_wins(match_df, top_n=5):
    """Calculates the top N teams by total wins."""
    team_wins = match_df['winner'].value_counts().reset_index()
    team_wins.columns = ['Team', 'Total Wins']
    return team_wins.head(top_n)

def plot_top_teams(df):
    """Generates a Matplotlib bar chart for top teams."""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Custom colors
    bars = ax.bar(df['Team'], df['Total Wins'], color=['#FFFF00', '#FF4B4B', '#0000FF', '#7CFC00', '#FFA500'], edgecolor='white') 
    
    ax.set_title(f'Top {len(df)} Winning Teams (All Seasons)', color='white', fontsize=16)
    ax.set_xlabel('Team', color='white')
    ax.set_ylabel('Total Wins', color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), 
                ha='center', va='bottom', color='white', fontsize=10)
    
    plt.tight_layout()
    return fig

# --- Main Content based on Selection ---
if analysis_option == 'Home':
    st.header("Welcome to the IPL Analytics Hub")
    st.write("Use the **sidebar** to navigate between different analyses, including top players and team performance graphs.")
    
elif analysis_option == 'Best Batsman':
    st.header("👑 Top IPL Batsmen Analysis")
    
    top_n = st.slider("Select number of Top Batsmen to display", 5, 20, 10)
    
    top_batsmen_df = get_best_batsman(delivery_df, top_n)
    
    st.subheader(f"Top {top_n} Batsmen by Total Runs")
    st.dataframe(top_batsmen_df, use_container_width=True) # Display as an attractive table
    
    # Display the chart
    batsman_fig = plot_batsman_runs(top_batsmen_df)
    st.pyplot(batsman_fig)


elif analysis_option == 'Best Bowler':
    st.header("🎯 Top IPL Bowlers Analysis")
    
    top_n = st.slider("Select number of Top Bowlers to display", 5, 20, 10)
    
    top_bowlers_df = get_best_bowler(delivery_df, top_n)
    
    st.subheader(f"Top {top_n} Bowlers by Total Wickets")
    st.dataframe(top_bowlers_df, use_container_width=True)
    
    # Display the chart
    bowler_fig = plot_bowler_wickets(top_bowlers_df)
    st.pyplot(bowler_fig)

elif analysis_option == 'Top Teams Performance':
    st.header("🏆 Top Team Performance Over Seasons")
    
    top_n = st.slider("Select number of Top Teams to display", 3, 10, 5)
    
    top_teams_df = get_top_teams_wins(match_df, top_n)
    
    st.subheader(f"Top {top_n} Teams by Total Wins")
    st.dataframe(top_teams_df, use_container_width=True)
    
    # Display the chart
    team_fig = plot_top_teams(top_teams_df)
    st.pyplot(team_fig)

# Run the app: Save this as app.py and run 'streamlit run app.py' in your terminal

# app.py (near the top, after st.set_page_config)

# --- Add Logo/Header Image ---
# Use an IPL logo PNG (make sure the path is correct)
st.sidebar.image("images/ipl_logo.png", use_container_width=True)

st.sidebar.header("Navigation")
# ... rest of the sidebar code ...
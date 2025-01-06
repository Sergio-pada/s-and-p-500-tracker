import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

st.title("S&P 500 Performance (Last 10 years)")
# Fetch S&P 500 data
sp500 = yf.Ticker("^GSPC")
data = sp500.history(period="10y")  # Get the last 10 years of data

# Display the date range
start_date = data.index.min().date()
end_date = data.index.max().date()
st.write(f"Data from **{start_date}** to **{end_date}**")

# Calculate daily returns
data['Return'] = data['Close'].pct_change()

# Add a column for the day of the week
data['Day of Week'] = data.index.day_name()

# Calculate average return by day of the week and sort from high to low
average_returns = data.groupby('Day of Week')['Return'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']).sort_values(ascending=False)

# Convert to DataFrame for proper ordering in the bar chart
average_returns_df = average_returns.reset_index()

# Set the 'Day of Week' as a categorical type with the desired order
average_returns_df['Day of Week'] = pd.Categorical(average_returns_df['Day of Week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], ordered=True)

# Calculate average return by month
data['Month'] = data.index.month_name()  # Extract month names
average_returns_month = data.groupby('Month')['Return'].mean().reindex(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']).sort_values(ascending=False)

# Convert to DataFrame for proper ordering in the bar chart
average_returns_month_df = average_returns_month.reset_index()

# Set the 'Month' as a categorical type with the desired order
average_returns_month_df['Month'] = pd.Categorical(average_returns_month_df['Month'], 
                                                    categories=['January', 'February', 'March', 'April', 'May', 'June', 
                                                                'July', 'August', 'September', 'October', 'November', 'December'], 
                                                    ordered=True)

# Visualization for Day of the Week
st.subheader("Average Stock Market Returns by Day of the Week")
day_chart = alt.Chart(average_returns_df).mark_bar().encode(
    x='Day of Week',
    y=alt.Y('Return:Q', axis=alt.Axis(title='Average Return (%)', format='%')),
).properties(
    title='Average Stock Market Returns by Day of the Week'
)
st.altair_chart(day_chart, use_container_width=True)

# Visualization for Month
st.subheader("Average Stock Market Returns by Month")
month_chart = alt.Chart(average_returns_month_df).mark_bar().encode(
    x='Month',
    y=alt.Y('Return:Q', axis=alt.Axis(title='Average Return (%)', format='%')),
).properties(
    title='Average Stock Market Returns by Month'
)
st.altair_chart(month_chart, use_container_width=True)

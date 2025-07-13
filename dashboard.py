import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from cronometer import CronometerClient

def create_dashboard():
    """
    Creates an interactive dashboard with two time-series plots of calorie data.
    """
    username = os.getenv('CRONOMETER_USER')
    password = os.getenv('CRONOMETER_PASS')

    if not username or not password:
        print("Error: CRONOMETER_USER and CRONOMETER_PASS environment variables must be set.")
        return

    client = CronometerClient(username, password)
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=365)  # Default to one year of data
    servings = client.get_servings(start_date, end_date)

    if not servings:
        print("No data downloaded from Cronometer.")
        return

    # Process the servings data
    df = pd.DataFrame(servings)
    df['Date'] = pd.to_datetime(df['date'])
    
    # Extract calorie information
    df['Calories'] = df['nutrients'].apply(lambda x: x.get('Energy', {}).get('amount', 0))
    
    # Aggregate calories per day
    daily_calories = df.groupby(df['Date'].dt.date)['Calories'].sum().reset_index()
    daily_calories.rename(columns={'Calories': 'Calories In'}, inplace=True)
    
    # Placeholder for Calories Out - Cronometer API for exercises is different
    daily_calories['Calories Out'] = 2000 # Placeholder value

    df = daily_calories
    df['Date'] = pd.to_datetime(df['Date'])
    df['Net Calories'] = df['Calories In'] - df['Calories Out']


    # Create the figure with two subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=("Daily Calorie Intake and Consumption", "Net Calories and Rolling Sum"))

    # Top plot: Daily calorie intake and consumption
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Calories In'], mode='lines', name='Calories In'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Calories Out'], mode='lines', name='Calories Out'), row=1, col=1)

    # Bottom plot: Double y-axis
    # Left y-axis: Daily net calories
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Net Calories'], mode='lines', name='Net Calories'), row=2, col=1)

    # Right y-axis: Rolling net calorie sum
    rolling_window = 7  # Default rolling window
    df['Rolling Net Sum'] = df['Net Calories'].rolling(window=rolling_window).sum()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Rolling Net Sum'], mode='lines', name=f'{rolling_window}-Day Rolling Sum'),
                  row=2, col=1, yaxis="y2")

    # Update layout
    fig.update_layout(
        title_text="Calorie Analysis Dashboard",
        xaxis_rangeslider_visible=True,
        yaxis=dict(title="Calories"),
        yaxis2=dict(title="Rolling Sum", overlaying="y", side="right"),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.1,
                y=1.2,
                showactive=True,
                buttons=list(
                    [
                        dict(
                            label=f"{days} days",
                            method="restyle",
                            args=[{"y": [df['Net Calories'].rolling(window=days).sum()], "name": f'{days}-Day Rolling Sum'}],
                        )
                        for days in [7, 14, 30, 60, 90]
                    ]
                ),
            )
        ]
    )
    fig.show()


if __name__ == '__main__':
    create_dashboard()
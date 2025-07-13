
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_dashboard(data_path):
    """
    Creates an interactive dashboard with two time-series plots of calorie data.

    Args:
        data_path (str): The path to the CSV file containing the calorie data.
    """
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: The file '{data_path}' was not found.")
        return

    # Assume the CSV has columns: 'Date', 'Calories In', 'Calories Out'
    # Data cleaning and preparation
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
    # Please replace 'calories.csv' with the actual path to your data file.
    create_dashboard('calories.csv')

"""
=============================================================================
CodeAlpha Data Analytics Internship
TASK 3: DATA VISUALIZATION & BUSINESS INTELLIGENCE DASHBOARDS
Project: End-to-End Operational & Commercial Food Delivery Visual Storytelling
Dataset: Order_delivery.csv
=============================================================================
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

# Set aesthetics
sns.set_theme(style="whitegrid", palette="tab10")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.autolayout'] = True

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "Order_delivery.csv")
if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.join(os.path.dirname(__file__), "Order_delivery.csv")
if not os.path.exists(DATA_PATH):
    DATA_PATH = "Order_delivery.csv"

VIS_DIR = os.path.join(os.path.dirname(__file__), "visualizations")
os.makedirs(VIS_DIR, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Order_Time'] = pd.to_datetime(df['Order_Time'], format='%d-%m-%Y %H:%M', errors='coerce')
    df['Order_Hour'] = df['Order_Time'].dt.hour
    df['Order_Day'] = df['Order_Time'].dt.day_name()
    return df

def generate_visual_stories(df):
    print("=" * 75)
    print("GENERATING TASK 3 VISUALIZATIONS & BUSINESS INTELLIGENCE STORYTELLING")
    print("=" * 75)

    # -----------------------------------------------------------------------
    # Story 1: Geographic Revenue & Order Volume Leaderboard
    # -----------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    city_metrics = df.groupby('City').agg({
        'Order_ID': 'count',
        'Total_Price': 'sum',
        'Delivery_Duration_Minutes': 'mean'
    }).reset_index().sort_values(by='Total_Price', ascending=False)

    sns.barplot(data=city_metrics, x='Total_Price', y='City', palette='Blues_r', ax=axes[0], edgecolor='black')
    axes[0].set_title('Total Revenue by City (EGP)', fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Total Revenue Generated (EGP)')
    axes[0].set_ylabel('City')

    sns.barplot(data=city_metrics, x='Delivery_Duration_Minutes', y='City', palette='Reds_r', ax=axes[1], edgecolor='black')
    axes[1].set_title('Average Delivery Duration by City (Minutes)', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Average Duration (Mins)')
    axes[1].set_ylabel('')

    plt.tight_layout()
    p1 = os.path.join(VIS_DIR, "01_city_revenue_and_speed_story.png")
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f" Saved: {p1}")

    # -----------------------------------------------------------------------
    # Story 2: Heatmap Matrix: Hourly Demand across Days of the Week
    # -----------------------------------------------------------------------
    plt.figure(figsize=(14, 7))
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_demand = df.pivot_table(index='Order_Day', columns='Order_Hour', values='Order_ID', aggfunc='count').reindex(day_order)
    
    sns.heatmap(pivot_demand, cmap='YlOrRd', annot=False, linewidths=0.5, cbar_kws={'label': 'Number of Orders'})
    plt.title('Order Demand Heatmap: Day of Week vs Hour of Day', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Hour of Day (00:00 - 23:00)', fontsize=12)
    plt.ylabel('Day of Week', fontsize=12)
    
    plt.tight_layout()
    p2 = os.path.join(VIS_DIR, "02_demand_heatmap_day_vs_hour.png")
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f" Saved: {p2}")

    # -----------------------------------------------------------------------
    # Story 3: Delivery Vehicle Efficiency Matrix across Traffic Conditions
    # -----------------------------------------------------------------------
    plt.figure(figsize=(11, 6))
    veh_traffic = df.groupby(['Driver_Vehicle', 'Traffic_Level'])['Delivery_Duration_Minutes'].mean().reset_index()
    
    sns.barplot(data=veh_traffic, x='Driver_Vehicle', y='Delivery_Duration_Minutes', hue='Traffic_Level',
                palette={'Low': '#2ecc71', 'Medium': '#f39c12', 'High': '#e74c3c'}, edgecolor='black')
    plt.title('Fleet Efficiency: Delivery Duration by Vehicle & Traffic Severity', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Driver Vehicle Type', fontsize=11)
    plt.ylabel('Avg Delivery Duration (Minutes)', fontsize=11)
    plt.legend(title='Traffic Level')
    plt.ylim(0, 50)

    plt.tight_layout()
    p3 = os.path.join(VIS_DIR, "03_fleet_vehicle_traffic_matrix.png")
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f" Saved: {p3}")

    # -----------------------------------------------------------------------
    # Story 4: Customer Payment Preferences & Average Basket Size
    # -----------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    pay_summary = df.groupby('Payment_Method').agg({'Order_ID': 'count', 'Total_Price': 'mean'}).reset_index()

    axes[0].pie(pay_summary['Order_ID'], labels=pay_summary['Payment_Method'], autopct='%1.1f%%',
                colors=['#3498db', '#9b59b6', '#1abc9c'], startangle=140, explode=(0.04, 0.04, 0.04),
                shadow=True, wedgeprops=dict(edgecolor='white', linewidth=2))
    axes[0].set_title('Payment Method Market Share (%)', fontsize=13, fontweight='bold')

    sns.barplot(data=pay_summary, x='Payment_Method', y='Total_Price', palette='Set2', ax=axes[1], edgecolor='black')
    axes[1].set_title('Average Order Value (Basket Size) by Payment Method', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Average Order Value (EGP)')
    axes[1].set_xlabel('Payment Method')
    for p in axes[1].patches:
        axes[1].annotate(f"{p.get_height():.2f} EGP", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', fontsize=11, fontweight='bold', xytext=(0, 6), textcoords='offset points')

    plt.tight_layout()
    p4 = os.path.join(VIS_DIR, "04_payment_share_and_basket_size.png")
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f" Saved: {p4}")

    # -----------------------------------------------------------------------
    # Story 5: Master C-Suite Visual Analytics Dashboard
    # -----------------------------------------------------------------------
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.25)

    # Panel 1: Top Item Popularity
    ax1 = fig.add_subplot(gs[0, 0])
    item_vol = df['Item_Name'].value_counts()
    sns.barplot(x=item_vol.values, y=item_vol.index, palette='mako', ax=ax1)
    ax1.set_title('1. Most Popular Menu Items', fontweight='bold', fontsize=12)

    # Panel 2: Order Fulfillment Funnel
    ax2 = fig.add_subplot(gs[0, 1])
    status_df = df['Order_Status'].value_counts()
    ax2.pie(status_df.values, labels=status_df.index, autopct='%1.1f%%', colors=['#27ae60', '#f1c40f', '#c0392b'], startangle=90)
    ax2.set_title('2. Order Completion Funnel', fontweight='bold', fontsize=12)

    # Panel 3: Distance vs Duration Violin Plot
    ax3 = fig.add_subplot(gs[0, 2])
    df['Distance_Band'] = pd.cut(df['Delivery_Distance_km'], bins=[0, 1.5, 3.0, 5.0, 10.0], labels=['<1.5km', '1.5-3km', '3-5km', '5km+'])
    sns.boxplot(data=df, x='Distance_Band', y='Delivery_Duration_Minutes', palette='coolwarm', ax=ax3)
    ax3.set_title('3. Delivery Duration across Distance Bands', fontweight='bold', fontsize=12)

    # Panel 4: Driver Availability Distribution
    ax4 = fig.add_subplot(gs[1, 0])
    sns.countplot(data=df, x='Driver_Availability', palette='Accent', ax=ax4, edgecolor='black')
    ax4.set_title('4. Driver Availability at Dispatch', fontweight='bold', fontsize=12)

    # Panel 5: Revenue Contribution by City
    ax5 = fig.add_subplot(gs[1, 1])
    city_rev = df.groupby('City')['Total_Price'].sum().sort_values(ascending=False).head(5)
    sns.barplot(x=city_rev.index, y=city_rev.values, palette='viridis', ax=ax5, edgecolor='black')
    ax5.set_title('5. Top 5 Revenue-Generating Cities', fontweight='bold', fontsize=12)
    ax5.tick_params(axis='x', rotation=25)

    # Panel 6: Peak Hour Density
    ax6 = fig.add_subplot(gs[1, 2])
    sns.histplot(df['Order_Hour'], bins=24, kde=True, color='#e67e22', ax=ax6)
    ax6.set_title('6. 24-Hour Order Volume Curve', fontweight='bold', fontsize=12)

    fig.suptitle('CodeAlpha Data Analytics: Task 3 — Executive Visual Intelligence Dashboard', fontsize=17, fontweight='bold', y=0.98)
    p5 = os.path.join(VIS_DIR, "05_master_executive_bi_dashboard.png")
    plt.savefig(p5, dpi=300)
    plt.close()
    print(f" Saved: {p5}")

if __name__ == "__main__":
    df = load_data()
    generate_visual_stories(df)
    print("\nTask 3 Data Visualization Pipeline Completed Successfully!")

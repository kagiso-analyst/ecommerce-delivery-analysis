import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD AND COMBINE THE DATASETS

orders_path = 'olist_orders_dataset.csv'
items_path = 'olist_order_items_dataset.csv'

# Load datasets
olist_orders = pd.read_csv(orders_path)
olist_order_items = pd.read_csv(items_path)

# Merge using the key 'order_id'
combined_orders_dataset = pd.merge(
    olist_orders,
    olist_order_items,
    on='order_id',
    how='inner'
)

# 2. CALCULATE DELIVERY TIME IN DAYS

# Convert date columns to datetime
combined_orders_dataset['order_purchase_timestamp'] = pd.to_datetime(combined_orders_dataset['order_purchase_timestamp'])
combined_orders_dataset['order_delivered_customer_date'] = pd.to_datetime(combined_orders_dataset['order_delivered_customer_date'])

# Calculate delivery time in days
combined_orders_dataset['delivery_time_days'] = (
    combined_orders_dataset['order_delivered_customer_date'] - 
    combined_orders_dataset['order_purchase_timestamp']
).dt.days

# Remove invalid delivery times (negative or unrealistic)
valid_deliveries = combined_orders_dataset[
    (combined_orders_dataset['delivery_time_days'] >= 0) & 
    (combined_orders_dataset['delivery_time_days'] <= 365)
]

# 3. CREATE HISTOGRAM

plt.figure(figsize=(12, 6))
plt.hist(valid_deliveries['delivery_time_days'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Distribution of Delivery Times', fontsize=16, fontweight='bold')
plt.xlabel('Delivery Time (Days)', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.show()

# 4. DELIVERY TIME ANALYSIS

average_delivery_time = valid_deliveries['delivery_time_days'].mean()
median_delivery_time = valid_deliveries['delivery_time_days'].median()
delivery_range = valid_deliveries['delivery_time_days'].max() - valid_deliveries['delivery_time_days'].min()

print("=== DELIVERY TIME ANALYSIS ===")
print(f"Average delivery time: {average_delivery_time:.2f} days")
print(f"Median delivery time: {median_delivery_time:.2f} days")
print(f"Delivery time range: {delivery_range} days")
print(f"Minimum delivery time: {valid_deliveries['delivery_time_days'].min()} days")
print(f"Maximum delivery time: {valid_deliveries['delivery_time_days'].max()} days")

# Identify outliers using IQR method
Q1 = valid_deliveries['delivery_time_days'].quantile(0.25)
Q3 = valid_deliveries['delivery_time_days'].quantile(0.75)
IQR = Q3 - Q1
outlier_threshold = Q3 + 1.5 * IQR

outliers = valid_deliveries[valid_deliveries['delivery_time_days'] > outlier_threshold]
print(f"Number of outliers (delivery time > {outlier_threshold:.2f} days): {len(outliers)}")

# 5. SAVE THE MERGED DATA FOR REUSE
combined_orders_dataset.to_csv('combined_orders_dataset.csv', index=False)

# Top Selling Products Analysis

print("\n" + "="*50)
print("Top Selling Products Analysis")
print("="*50)

# 1. Identify the top 10 most sold products based on the number of items sold
top_products = (combined_orders_dataset
    .groupby('product_id')
    .agg({
        'order_item_id': 'count',  # Count number of items sold
        'price': 'mean'  # Optional: get average price for context
    })
    .rename(columns={'order_item_id': 'quantity_sold', 'price': 'avg_price'})
    .sort_values('quantity_sold', ascending=False)
    .head(10)
    .reset_index()
)

print("\nTop 10 Most Sold Products:")
print(top_products[['product_id', 'quantity_sold', 'avg_price']])

# 2. Create a bar chart to display these top-selling products
plt.figure(figsize=(14, 8))

# Create horizontal bar chart (easier to read product IDs)
bars = plt.barh(
    range(len(top_products)),
    top_products['quantity_sold'],
    color='lightcoral',
    alpha=0.7,
    edgecolor='darkred'
)

# Customize the horizontal chart
plt.title('Top 10 Most Sold Products', fontsize=16, fontweight='bold')
plt.xlabel('Quantity Sold', fontsize=12)
plt.ylabel('Product ID', fontsize=12)
plt.yticks(range(len(top_products)), top_products['product_id'])

# Add value labels on bars
for bar, value in zip(bars, top_products['quantity_sold']):
    plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
             f'{int(value)}', ha='left', va='center', fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# 3. Reflection and Analysis
print("\n" + "="*40)
print("REFLECTION AND ANALYSIS")
print("="*40)

print("\nWhy certain products might be more popular than others:")
print("• ESSENTIAL ITEMS: Products that fulfill daily needs or basic requirements")
print("• COMPETITIVE PRICING: Affordable products with good value for money")
print("• POSITIVE REVIEWS: High ratings and positive customer feedback")
print("• EFFECTIVE MARKETING: Better product visibility and promotional efforts")
print("• SEASONAL DEMAND: Products aligned with current trends or seasons")
print("• PRODUCT QUALITY: Reliable and durable items that meet expectations")
print("• BRAND REPUTATION: Trusted brands with established customer loyalty")
print("• EASE OF USE: Simple, user-friendly products without complexity")

print("\nHow this information can be used in marketing strategies:")
print("• FOCUSED ADVERTISING: Allocate more budget to promote top-performing product categories")
print("• INVENTORY OPTIMIZATION: Ensure adequate stock levels for popular items")
print("• CROSS-SELLING: Bundle popular products with complementary items")
print("• CUSTOMER INSIGHTS: Analyze reviews of top products to understand success factors")
print("• PRICING STRATEGY: Use popular products as loss leaders to attract customers")
print("• SUPPLIER RELATIONS: Strengthen partnerships with suppliers of top products")
print("• PRODUCT DEVELOPMENT: Identify features that make products successful for new developments")
print("• TARGETED PROMOTIONS: Create special offers around best-selling items")

# Additional analysis: Calculate what percentage of total sales these top 10 represent
total_items_sold = combined_orders_dataset['order_item_id'].count()
top_10_total_sales = top_products['quantity_sold'].sum()
percentage_of_total = (top_10_total_sales / total_items_sold) * 100

print(f"\nAdditional Insights:")
print(f"Total items sold in dataset: {total_items_sold}")
print(f"Top 10 products account for: {top_10_total_sales} items ({percentage_of_total:.2f}% of total)")

# Price range analysis for top products
avg_price_top = top_products['avg_price'].mean()
min_price_top = top_products['avg_price'].min()
max_price_top = top_products['avg_price'].max()

print(f"Average price of top products: R${avg_price_top:.2f}")
print(f"Price range of top products: R${min_price_top:.2f} - R${max_price_top:.2f}")

print("\n Completed successfully!")

# Seller Revenue Analysis

print("\n" + "="*50)
print("Seller Revenue Analysis")
print("="*50)

# 1. Calculate the total revenue (product price + freight value) generated by each seller
seller_revenue = (combined_orders_dataset
    .groupby('seller_id')
    .agg({
        'price': 'sum',
        'freight_value': 'sum',
        'order_id': 'count'  # Count number of orders for context
    })
    .reset_index()
)

seller_revenue['total_revenue'] = seller_revenue['price'] + seller_revenue['freight_value']
seller_revenue = seller_revenue.rename(columns={'order_id': 'order_count'})

# Get top 10 sellers by revenue
top_sellers = seller_revenue.nlargest(10, 'total_revenue')

print("\nTop 10 Sellers by Revenue:")
print(top_sellers[['seller_id', 'total_revenue', 'order_count', 'price', 'freight_value']].round(2))

# 2. Create bar chart to display top sellers by revenue
plt.figure(figsize=(14, 8))

# Create horizontal bar chart
bars = plt.barh(
    range(len(top_sellers)),
    top_sellers['total_revenue'],
    color='lightgreen',
    alpha=0.7,
    edgecolor='darkgreen'
)

# Customize the chart
plt.title('Top 10 Sellers by Total Revenue', fontsize=16, fontweight='bold')
plt.xlabel('Total Revenue (R$)', fontsize=12)
plt.ylabel('Seller ID', fontsize=12)
plt.yticks(range(len(top_sellers)), top_sellers['seller_id'])

# Add value labels on bars
for bar, value in zip(bars, top_sellers['total_revenue']):
    plt.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2, 
             f'R$ {value:,.0f}', ha='left', va='center', fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# Additional visualization: Compare revenue components (price vs freight)
plt.figure(figsize=(14, 8))

# Create stacked bar chart
bar_width = 0.6
bars1 = plt.barh(
    range(len(top_sellers)),
    top_sellers['price'],
    bar_width,
    color='lightblue',
    label='Product Price',
    alpha=0.7
)

bars2 = plt.barh(
    range(len(top_sellers)),
    top_sellers['freight_value'],
    bar_width,
    left=top_sellers['price'],
    color='orange',
    label='Freight Value',
    alpha=0.7
)

plt.title('Top 10 Sellers Revenue Breakdown (Price vs Freight)', fontsize=16, fontweight='bold')
plt.xlabel('Revenue (R$)', fontsize=12)
plt.ylabel('Seller ID', fontsize=12)
plt.yticks(range(len(top_sellers)), top_sellers['seller_id'])
plt.legend()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# 3. Discussion and Analysis
print("\n" + "="*40)
print("DISCUSSION AND ANALYSIS")
print("="*40)

print("\nWhy top sellers might outperform others:")
print("• PRODUCT QUALITY & SELECTION: Offering high-quality products with good variety")
print("• COMPETITIVE PRICING: Strategic pricing that balances profit and customer value")
print("• OPERATIONAL EFFICIENCY: Faster order processing and shipping capabilities")
print("• CUSTOMER SERVICE: Excellent after-sales support and responsive communication")
print("• REVIEWS & RATINGS: High customer satisfaction leading to positive reviews")
print("• MARKETING EFFECTIVENESS: Better use of marketplace features and promotions")
print("• RELIABILITY: Consistent product availability and delivery performance")
print("• BRAND REPUTATION: Established trust and recognition among customers")

print("\nPotential factors contributing to revenue disparities among sellers:")
print("• GEOGRAPHIC LOCATION: Sellers in strategic locations with better logistics")
print("• SUPPLY CHAIN MANAGEMENT: Efficient inventory and supplier relationships")
print("• SELLER EXPERIENCE: More experienced sellers understanding market dynamics")
print("• PRODUCT NICHE: Specialization in high-demand or high-margin categories")
print("• TECHNOLOGY ADOPTION: Better use of analytics and automation tools")
print("• CUSTOMER RETENTION: Higher repeat purchase rates and customer loyalty")
print("• SCALABILITY: Ability to handle larger order volumes efficiently")
print("• MARKET TIMING: Early entry into high-growth product categories")

# Additional quantitative analysis
print("\n" + "="*40)
print("ADDITIONAL INSIGHTS")
print("="*40)

# Calculate percentage of total revenue from top sellers
total_revenue_all_sellers = seller_revenue['total_revenue'].sum()
top_10_revenue = top_sellers['total_revenue'].sum()
percentage_revenue_top_10 = (top_10_revenue / total_revenue_all_sellers) * 100

# Calculate average order value for top sellers
top_sellers['avg_order_value'] = top_sellers['total_revenue'] / top_sellers['order_count']

# Calculate freight as percentage of revenue
top_sellers['freight_percentage'] = (top_sellers['freight_value'] / top_sellers['total_revenue']) * 100

print(f"Total revenue from all sellers: R$ {total_revenue_all_sellers:,.2f}")
print(f"Revenue from top 10 sellers: R$ {top_10_revenue:,.2f}")
print(f"Top 10 sellers account for: {percentage_revenue_top_10:.2f}% of total revenue")

print(f"\nAverage Order Value for Top Sellers: R$ {top_sellers['avg_order_value'].mean():.2f}")
print(f"Average freight as % of revenue: {top_sellers['freight_percentage'].mean():.2f}%")

# Performance distribution analysis
print(f"\nRevenue Distribution Among Sellers:")
print(f"Number of sellers in dataset: {len(seller_revenue)}")
print(f"Average revenue per seller: R$ {seller_revenue['total_revenue'].mean():.2f}")
print(f"Median revenue per seller: R$ {seller_revenue['total_revenue'].median():.2f}")
print(f"Revenue standard deviation: R$ {seller_revenue['total_revenue'].std():.2f}")

# Identify revenue concentration
top_1_percent = int(len(seller_revenue) * 0.01)
top_1_percent_revenue = seller_revenue.nlargest(top_1_percent, 'total_revenue')['total_revenue'].sum()
percentage_top_1 = (top_1_percent_revenue / total_revenue_all_sellers) * 100

print(f"Top 1% of sellers account for: {percentage_top_1:.2f}% of total revenue")

print("\n Completed successfully!")

# Monthly Revenue Trends Analysis

print("\n" + "="*50)
print("Monthly Revenue Trends Analysis")
print("="*50)

# 1. Group the data by month and calculate the total revenue for each month

# Create a copy to avoid modifying original data
monthly_revenue = combined_orders_dataset.copy()

# Calculate total revenue per order item
monthly_revenue['total_revenue'] = monthly_revenue['price'] + monthly_revenue['freight_value']

# Extract year-month from purchase timestamp
monthly_revenue['order_month'] = monthly_revenue['order_purchase_timestamp'].dt.to_period('M')

# Group by month and calculate metrics
monthly_totals = (monthly_revenue
    .groupby('order_month')
    .agg({
        'total_revenue': 'sum',
        'order_id': 'nunique',  # Count unique orders
        'product_id': 'count'   # Count total items sold
    })
    .reset_index()
    .rename(columns={
        'order_id': 'order_count',
        'product_id': 'item_count'
    })
)

# Convert period to timestamp for plotting
monthly_totals['order_month'] = monthly_totals['order_month'].dt.to_timestamp()

# Sort by month to ensure proper line chart
monthly_totals = monthly_totals.sort_values('order_month')

print("\nMonthly Revenue Summary:")
print(monthly_totals[['order_month', 'total_revenue', 'order_count', 'item_count']].round(2))

# 2. Create line chart to visualize monthly revenue trends
plt.figure(figsize=(15, 8))

# Main revenue trend line
plt.plot(monthly_totals['order_month'], 
         monthly_totals['total_revenue'], 
         marker='o', 
         linewidth=3, 
         markersize=8,
         color='royalblue',
         label='Total Revenue')

# Customize the chart
plt.title('Monthly Revenue Trends', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Revenue (R$)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Add value annotations for peaks and valleys
max_revenue = monthly_totals['total_revenue'].max()
min_revenue = monthly_totals['total_revenue'].min()
max_month = monthly_totals.loc[monthly_totals['total_revenue'].idxmax(), 'order_month']
min_month = monthly_totals.loc[monthly_totals['total_revenue'].idxmin(), 'order_month']

plt.annotate(f'Peak: R$ {max_revenue:,.0f}', 
             xy=(max_month, max_revenue), 
             xytext=(10, 20), 
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='red'),
             fontweight='bold',
             color='red')

plt.annotate(f'Low: R$ {min_revenue:,.0f}', 
             xy=(min_month, min_revenue), 
             xytext=(10, -30), 
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='green'),
             fontweight='bold',
             color='green')

plt.legend()
plt.tight_layout()
plt.show()

# Additional visualization: Multiple metrics view
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

# Subplot 1: Revenue trend
ax1.plot(monthly_totals['order_month'], monthly_totals['total_revenue'], 
         marker='o', linewidth=2, color='royalblue')
ax1.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
ax1.set_ylabel('Revenue (R$)', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Subplot 2: Order count trend
ax2.plot(monthly_totals['order_month'], monthly_totals['order_count'], 
         marker='s', linewidth=2, color='coral')
ax2.set_title('Monthly Order Count Trend', fontsize=14, fontweight='bold')
ax2.set_xlabel('Month', fontsize=12)
ax2.set_ylabel('Number of Orders', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# 3. Analysis
print("\n" + "="*40)
print("TREND ANALYSIS")
print("="*40)

# Calculate growth metrics
monthly_totals['revenue_growth'] = monthly_totals['total_revenue'].pct_change() * 100
monthly_totals['avg_order_value'] = monthly_totals['total_revenue'] / monthly_totals['order_count']

# Identify top and bottom performing months
top_3_months = monthly_totals.nlargest(3, 'total_revenue')
bottom_3_months = monthly_totals.nsmallest(3, 'total_revenue')

print("\nTop 3 Highest Revenue Months:")
for _, row in top_3_months.iterrows():
    month_str = row['order_month'].strftime('%B %Y')
    print(f"  {month_str}: R$ {row['total_revenue']:,.2f} ({row['order_count']} orders)")

print("\nBottom 3 Lowest Revenue Months:")
for _, row in bottom_3_months.iterrows():
    month_str = row['order_month'].strftime('%B %Y')
    print(f"  {month_str}: R$ {row['total_revenue']:,.2f} ({row['order_count']} orders)")

# Seasonal analysis
print("\n" + "="*40)
print("SEASONAL PATTERNS ANALYSIS")
print("="*40)

print("\nNoticeable Patterns and Trends:")
print("• SEASONAL PEAKS: Look for consistent high-performance periods (e.g., holiday seasons)")
print("• GROWTH TREND: Observe if revenue is generally increasing over time")
print("• CYCLICAL PATTERNS: Identify repeating patterns across years")
print("• OUTLIER MONTHS: Months with unusually high or low performance")

print("\nPotential Reasons for Revenue Variations:")
print("• HOLIDAY SEASONS: Christmas, Black Friday, Cyber Monday promotions")
print("• SEASONAL DEMAND: Weather-related product demand changes")
print("• ECONOMIC FACTORS: Economic booms/recessions affecting consumer spending")
print("• MARKETING CAMPAIGNS: Major advertising or promotional activities")
print("• COMPETITIVE ACTIVITY: Competitor promotions affecting market share")
print("• EXTERNAL EVENTS: National events, sports tournaments, festivals")
print("• PLATFORM CHANGES: Marketplace policy or fee structure changes")

# Statistical analysis
print("\n" + "="*40)
print("STATISTICAL SUMMARY")
print("="*40)

print(f"Average Monthly Revenue: R$ {monthly_totals['total_revenue'].mean():,.2f}")
print(f"Median Monthly Revenue: R$ {monthly_totals['total_revenue'].median():,.2f}")
print(f"Highest Monthly Revenue: R$ {monthly_totals['total_revenue'].max():,.2f}")
print(f"Lowest Monthly Revenue: R$ {monthly_totals['total_revenue'].min():,.2f}")
print(f"Revenue Standard Deviation: R$ {monthly_totals['total_revenue'].std():,.2f}")

print(f"\nAverage Order Value: R$ {monthly_totals['avg_order_value'].mean():.2f}")
print(f"Average Monthly Orders: {monthly_totals['order_count'].mean():.0f}")

# Growth analysis
positive_growth_months = monthly_totals[monthly_totals['revenue_growth'] > 0]
if len(positive_growth_months) > 0:
    avg_positive_growth = positive_growth_months['revenue_growth'].mean()
    print(f"Average positive monthly growth: {avg_positive_growth:.2f}%")

# Challenge: Marketing strategies for low-performing months
print("\n" + "="*40)
print("MARKETING STRATEGIES FOR LOW-PERFORMING MONTHS")
print("="*40)

print("Suggested Strategies to Boost Revenue During Slow Periods:")
print("1. TARGETED PROMOTIONS: Run flash sales or limited-time discounts")
print("2. LOYALTY PROGRAMS: Introduce points-based rewards for repeat purchases")
print("3. EMAIL MARKETING: Re-engage dormant customers with personalized offers")
print("4. CROSS-SELLING: Create product bundles to increase average order value")
print("5. SEASONAL PRODUCTS: Introduce products relevant to the current season")
print("6. FREE SHIPPING: Offer free shipping thresholds to encourage larger orders")
print("7. SOCIAL MEDIA CAMPAIGNS: Increase social media advertising during slow periods")
print("8. PARTNERSHIPS: Collaborate with influencers or complementary brands")
print("9. RETARGETING ADS: Implement retargeting campaigns for cart abandoners")
print("10. CONTENT MARKETING: Create valuable content to drive organic traffic")

# Identify specific low months for targeted strategies
low_months = bottom_3_months['order_month'].dt.strftime('%B').tolist()
if low_months:
    print(f"\nFocus marketing efforts during: {', '.join(set(low_months))}")

print("\n Completed successfully!")
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

# Use non-interactive backend for server environments
matplotlib.use('Agg')


def generate_income_expense_chart(total_income: float, total_expense: float) -> BytesIO:
    """
    Generate Income vs Expense bar chart in memory (BytesIO).
    
    Args:
        total_income: Total income amount
        total_expense: Total expense amount
    
    Returns:
        BytesIO buffer containing PNG image
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
    
    # Data
    categories = ['Income', 'Expense']
    amounts = [total_income, total_expense]
    colors = ['#90EE90', '#FFB6C6']  # Light green for Income, Light pink/red for Expense
    
    # Create bar chart
    bars = ax.bar(categories, amounts, color=colors, edgecolor='#333333', linewidth=2)
    
    # Add value labels on top of bars
    for bar, amount in zip(bars, amounts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{amount:,.2f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='#333333')
    
    # Styling
    ax.set_ylabel('Amount', fontsize=12, fontweight='bold')
    ax.set_title('Income vs Expense Overview', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.4, linestyle='--', color='#cccccc')
    ax.set_axisbelow(True)
    
    # Format y-axis with thousand separators
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    # Set background color
    ax.set_facecolor('#f9f9f9')
    fig.patch.set_facecolor('white')
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Tight layout
    plt.tight_layout()
    
    # Save to BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    plt.close(fig)
    
    return buffer

import discord
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Data files
EXPENSES_FILE = "expenses.json"
BUDGETS_FILE = "budgets.json"

# Categories with emojis
CATEGORIES = {
    "food": "🍔 Food & Dining",
    "transport": "🚗 Transportation",
    "shopping": "🛍️ Shopping",
    "healthcare": "💊 Healthcare",
    "entertainment": "🎮 Entertainment",
    "bills": "💳 Bills & Utilities",
    "education": "🎓 Education",
    "housing": "🏠 Housing",
    "other": "💰 Other"
}

def load_expenses():
    """Load expenses from file"""
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_expenses(expenses):
    """Save expenses to file"""
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

def load_budgets():
    """Load budgets from file"""
    if os.path.exists(BUDGETS_FILE):
        with open(BUDGETS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_budgets(budgets):
    """Save budgets to file"""
    with open(BUDGETS_FILE, 'w') as f:
        json.dump(budgets, f, indent=2)

# Load data
expenses_data = load_expenses()
budgets_data = load_budgets()

def get_user_expenses(user_id):
    """Get expenses for a specific user"""
    user_id = str(user_id)
    if user_id not in expenses_data:
        expenses_data[user_id] = []
    return expenses_data[user_id]

def add_expense(user_id, amount, category, description):
    """Add a new expense"""
    user_id = str(user_id)
    expenses = get_user_expenses(user_id)
    
    expense_id = len(expenses) + 1
    expense = {
        "id": expense_id,
        "amount": float(amount),
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    
    expenses.append(expense)
    save_expenses(expenses_data)
    return expense

def filter_expenses_by_period(expenses, period):
    """Filter expenses by time period"""
    now = datetime.now()
    
    if period == "today":
        target_date = now.strftime("%Y-%m-%d")
        return [e for e in expenses if e["date"] == target_date]
    
    elif period == "week":
        week_ago = now - timedelta(days=7)
        return [e for e in expenses if datetime.strptime(e["date"], "%Y-%m-%d") >= week_ago]
    
    elif period == "month":
        return [e for e in expenses if e["date"].startswith(now.strftime("%Y-%m"))]
    
    return expenses

def calculate_category_totals(expenses):
    """Calculate total spending by category"""
    totals = defaultdict(float)
    for expense in expenses:
        totals[expense["category"]] += expense["amount"]
    return dict(totals)

def get_budget_status(user_id):
    """Get budget status for user"""
    user_id = str(user_id)
    if user_id not in budgets_data:
        return None
    
    expenses = get_user_expenses(user_id)
    month_expenses = filter_expenses_by_period(expenses, "month")
    category_totals = calculate_category_totals(month_expenses)
    
    status = {}
    for category, budget in budgets_data[user_id].items():
        spent = category_totals.get(category, 0)
        remaining = budget - spent
        percentage = (spent / budget * 100) if budget > 0 else 0
        status[category] = {
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "percentage": percentage
        }
    
    return status

@client.event
async def on_ready():
    print(f'{client.user} is now online!')
    print(f'Expense Tracker Bot ready! Connected to {len(client.guilds)} server(s)')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content
    user_id = str(message.author.id)
    
    # Help command
    if msg.startswith('$help'):
        help_text = """
**💰 Expense Tracker Bot Commands:**

**Basic Commands:**
`$add <amount> <category> <description>` - Add an expense
Example: `$add 15.50 food Lunch at cafe`

`$list [today/week/month/all]` - View your expenses
Example: `$list week`

`$categories` - Show all available categories

`$summary [month]` - Monthly spending summary
Example: `$summary`

`$delete <id>` - Delete an expense by ID
Example: `$delete 5`

**Budget Commands:**
`$budget set <category> <amount>` - Set monthly budget
Example: `$budget set food 500`

`$budget status` - Check budget vs actual spending

`$budget clear` - Remove all budgets

**Categories:** food, transport, shopping, healthcare, entertainment, bills, education, housing, other
        """
        await message.channel.send(help_text)
        return
    
    # Add expense
    if msg.startswith('$add'):
        try:
            parts = msg.split(' ', 3)
            if len(parts) < 4:
                await message.channel.send("❌ Usage: `$add <amount> <category> <description>`")
                return
            
            amount = parts[1]
            category = parts[2].lower()
            description = parts[3]
            
            # Validate amount
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    await message.channel.send("❌ Amount must be greater than 0!")
                    return
            except ValueError:
                await message.channel.send("❌ Invalid amount! Please enter a number.")
                return
            
            # Validate category
            if category not in CATEGORIES:
                await message.channel.send(f"❌ Invalid category! Use `$categories` to see available options.")
                return
            
            # Add expense
            expense = add_expense(user_id, amount, category, description)
            
            # Check budget warning
            warning = ""
            if user_id in budgets_data and category in budgets_data[user_id]:
                expenses = get_user_expenses(user_id)
                month_expenses = filter_expenses_by_period(expenses, "month")
                category_total = sum(e["amount"] for e in month_expenses if e["category"] == category)
                budget = budgets_data[user_id][category]
                
                if category_total >= budget:
                    warning = f"\n⚠️ **Budget Alert:** You've exceeded your {CATEGORIES[category]} budget!"
                elif category_total >= budget * 0.8:
                    warning = f"\n⚠️ **Budget Alert:** You've used {category_total/budget*100:.0f}% of your {CATEGORIES[category]} budget!"
            
            await message.channel.send(
                f"✅ Expense added!\n"
                f"💵 ${amount_float:.2f} - {CATEGORIES[category]}\n"
                f"📝 {description}"
                f"{warning}"
            )
            return
            
        except Exception as e:
            await message.channel.send(f"❌ Error adding expense: {str(e)}")
            return
    
    # List expenses
    if msg.startswith('$list'):
        try:
            parts = msg.split(' ')
            period = parts[1] if len(parts) > 1 else "month"
            
            if period not in ["today", "week", "month", "all"]:
                await message.channel.send("❌ Invalid period! Use: today, week, month, or all")
                return
            
            expenses = get_user_expenses(user_id)
            filtered = filter_expenses_by_period(expenses, period)
            
            if not filtered:
                await message.author.send(f"📭 No expenses found for {period}.")
                await message.channel.send("✅ Check your DMs!")
                return
            
            # Sort by date (most recent first)
            filtered.sort(key=lambda x: (x["date"], x["timestamp"]), reverse=True)
            
            # Create response
            response = f"**💰 Your Expenses ({period.capitalize()}):**\n\n"
            total = 0
            
            for exp in filtered[-20:]:  # Show last 20
                total += exp["amount"]
                response += f"`ID:{exp['id']}` ${exp['amount']:.2f} - {CATEGORIES[exp['category']]} - {exp['description']} ({exp['date']})\n"
            
            response += f"\n**Total: ${total:.2f}**"
            
            await message.author.send(response)
            await message.channel.send("✅ Check your DMs!")
            return
            
        except Exception as e:
            await message.channel.send(f"❌ Error: {str(e)}")
            return
    
    # Show categories
    if msg.startswith('$categories'):
        cat_list = "**Available Categories:**\n\n"
        for key, value in CATEGORIES.items():
            cat_list += f"`{key}` - {value}\n"
        await message.channel.send(cat_list)
        return
    
    # Summary
    if msg.startswith('$summary'):
        try:
            expenses = get_user_expenses(user_id)
            month_expenses = filter_expenses_by_period(expenses, "month")
            
            if not month_expenses:
                await message.channel.send("📭 No expenses found for this month.")
                return
            
            category_totals = calculate_category_totals(month_expenses)
            total = sum(category_totals.values())
            
            response = f"**📊 Monthly Summary ({datetime.now().strftime('%B %Y')}):**\n\n"
            
            for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total * 100) if total > 0 else 0
                response += f"{CATEGORIES[category]}: ${amount:.2f} ({percentage:.1f}%)\n"
            
            response += f"\n**💵 Total: ${total:.2f}**"
            response += f"\n📝 Total Expenses: {len(month_expenses)}"
            
            await message.author.send(response)
            await message.channel.send("✅ Check your DMs!")
            return
            
        except Exception as e:
            await message.channel.send(f"❌ Error: {str(e)}")
            return
    
    # Delete expense
    if msg.startswith('$delete'):
        try:
            parts = msg.split(' ')
            if len(parts) < 2:
                await message.channel.send("❌ Usage: `$delete <expense_id>`")
                return
            
            expense_id = int(parts[1])
            expenses = get_user_expenses(user_id)
            
            # Find and remove expense
            found = False
            for i, exp in enumerate(expenses):
                if exp["id"] == expense_id:
                    removed = expenses.pop(i)
                    save_expenses(expenses_data)
                    await message.channel.send(
                        f"✅ Deleted: ${removed['amount']:.2f} - {CATEGORIES[removed['category']]} - {removed['description']}"
                    )
                    found = True
                    break
            
            if not found:
                await message.channel.send(f"❌ Expense ID {expense_id} not found!")
            
            return
            
        except ValueError:
            await message.channel.send("❌ Invalid expense ID!")
            return
        except Exception as e:
            await message.channel.send(f"❌ Error: {str(e)}")
            return
    
    # Budget commands
    if msg.startswith('$budget'):
        parts = msg.split(' ')
        
        if len(parts) < 2:
            await message.channel.send("❌ Usage: `$budget [set/status/clear]`")
            return
        
        action = parts[1].lower()
        
        # Set budget
        if action == "set":
            try:
                if len(parts) < 4:
                    await message.channel.send("❌ Usage: `$budget set <category> <amount>`")
                    return
                
                category = parts[2].lower()
                amount = float(parts[3])
                
                if category not in CATEGORIES:
                    await message.channel.send(f"❌ Invalid category! Use `$categories` to see options.")
                    return
                
                if amount <= 0:
                    await message.channel.send("❌ Budget amount must be greater than 0!")
                    return
                
                if user_id not in budgets_data:
                    budgets_data[user_id] = {}
                
                budgets_data[user_id][category] = amount
                save_budgets(budgets_data)
                
                await message.channel.send(
                    f"✅ Budget set: {CATEGORIES[category]} - ${amount:.2f}/month"
                )
                return
                
            except ValueError:
                await message.channel.send("❌ Invalid amount!")
                return
            except Exception as e:
                await message.channel.send(f"❌ Error: {str(e)}")
                return
        
        # Budget status
        elif action == "status":
            status = get_budget_status(user_id)
            
            if not status:
                await message.channel.send("📭 No budgets set! Use `$budget set <category> <amount>`")
                return
            
            response = f"**📊 Budget Status ({datetime.now().strftime('%B %Y')}):**\n\n"
            
            for category, data in status.items():
                emoji = "✅" if data["remaining"] >= 0 else "❌"
                bar_length = min(int(data["percentage"] / 10), 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                
                response += f"{emoji} {CATEGORIES[category]}\n"
                response += f"Budget: ${data['budget']:.2f} | Spent: ${data['spent']:.2f}\n"
                response += f"[{bar}] {data['percentage']:.1f}%\n"
                response += f"Remaining: ${data['remaining']:.2f}\n\n"
            
            await message.author.send(response)
            await message.channel.send("✅ Check your DMs!")
            return
        
        # Clear budgets
        elif action == "clear":
            if user_id in budgets_data:
                del budgets_data[user_id]
                save_budgets(budgets_data)
                await message.channel.send("✅ All budgets cleared!")
            else:
                await message.channel.send("📭 No budgets to clear!")
            return
        
        else:
            await message.channel.send("❌ Invalid action! Use: set, status, or clear")
            return

client.run(os.getenv('TOKEN'))

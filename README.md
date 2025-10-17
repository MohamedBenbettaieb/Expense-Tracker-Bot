# 💰 Expense Tracker Discord Bot

A practical Discord bot that helps you track your expenses, manage budgets, and gain insights into your spending habits. All your financial data is stored privately and persists between bot restarts.

## ✨ Features

- **📝 Expense Tracking**: Log expenses with amount, category, and description
- **📊 Spending Analysis**: View expenses by day, week, or month
- **💵 Budget Management**: Set monthly budgets per category with automatic alerts
- **🔔 Smart Alerts**: Get notified when you reach 80% or exceed your budget
- **📈 Visual Reports**: See spending breakdowns with percentages and progress bars
- **🔒 Privacy First**: All detailed financial data is sent via DM
- **💾 Persistent Storage**: All data is saved and survives bot restarts
- **👥 Multi-User**: Each user has their own separate expense tracking

## 📋 Prerequisites

- Python 3.8 or higher
- Discord Bot Token (from Discord Developer Portal)
- pip (Python package manager)

## 🚀 Installation

### 1. Clone or Download
Download this repository to your local machine.

### 2. Install Dependencies
```bash
pip install discord.py python-dotenv
```

### 3. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it (e.g., "Expense Tracker")
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - ✅ **Message Content Intent**
5. Click "Reset Token" and copy your bot token

### 4. Configure Environment Variables

Create a `.env` file in the project directory:
```env
TOKEN=your_bot_token_here
```

### 5. Invite Bot to Server

1. In Developer Portal, go to **OAuth2 → URL Generator**
2. Select scopes:
   - ✅ `bot`
3. Select bot permissions:
   - ✅ `Send Messages`
   - ✅ `Read Messages/View Channels`
   - ✅ `Send Messages in Threads` (optional)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

## 🎮 Usage

### Starting the Bot

```bash
python main.py
```

You should see:
```
<BotName> is now online!
Expense Tracker Bot ready! Connected to 1 server(s)
```

## 📖 Commands

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `$help` | Show all available commands | `$help` |
| `$add <amount> <category> <description>` | Add a new expense | `$add 15.50 food Lunch at cafe` |
| `$list [period]` | View expenses (today/week/month/all) | `$list week` |
| `$categories` | Show all available expense categories | `$categories` |
| `$summary` | Get monthly spending summary | `$summary` |
| `$delete <id>` | Delete an expense by its ID | `$delete 5` |

### Budget Commands

| Command | Description | Example |
|---------|-------------|---------|
| `$budget set <category> <amount>` | Set monthly budget for a category | `$budget set food 500` |
| `$budget status` | Check budget vs actual spending | `$budget status` |
| `$budget clear` | Remove all budget limits | `$budget clear` |

## 📂 Categories

The bot supports 9 expense categories:

| Command | Category | Emoji |
|---------|----------|-------|
| `food` | Food & Dining | 🍔 |
| `transport` | Transportation | 🚗 |
| `shopping` | Shopping | 🛍️ |
| `healthcare` | Healthcare | 💊 |
| `entertainment` | Entertainment | 🎮 |
| `bills` | Bills & Utilities | 💳 |
| `education` | Education | 🎓 |
| `housing` | Housing | 🏠 |
| `other` | Other | 💰 |

## 💡 Usage Examples

### Adding Expenses
```
$add 25.50 food Dinner at restaurant
$add 10 transport Bus fare
$add 150 bills Internet subscription
$add 45.99 entertainment Movie tickets
```

### Viewing Expenses
```
$list today          # Today's expenses
$list week           # Last 7 days
$list month          # Current month
$list all            # All expenses
```

### Setting Budgets
```
$budget set food 300
$budget set transport 150
$budget set entertainment 100
```

### Checking Budget Status
```
$budget status
```

Output example:
```
📊 Budget Status (October 2025):

✅ 🍔 Food & Dining
Budget: $300.00 | Spent: $125.50
[████░░░░░░] 41.8%
Remaining: $174.50

⚠️ 🚗 Transportation
Budget: $150.00 | Spent: $140.00
[█████████░] 93.3%
Remaining: $10.00
```

### Deleting Expenses
```
$delete 5            # Deletes expense with ID 5
```

## 📁 File Structure

```
ExpenseTrackerBot/
│
├── main.py                # Main bot code
├── .env                   # Environment variables (TOKEN)
├── expenses.json          # User expenses data (auto-generated)
├── budgets.json           # User budget settings (auto-generated)
├── README.md              # This file
└── .gitignore             # Git ignore file
```

## 💾 Data Storage

### expenses.json
Stores all user expenses:
```json
{
  "user_id": [
    {
      "id": 1,
      "amount": 15.50,
      "category": "food",
      "description": "Lunch at cafe",
      "date": "2025-10-18",
      "timestamp": "14:30:25"
    }
  ]
}
```

### budgets.json
Stores user budget limits:
```json
{
  "user_id": {
    "food": 300,
    "transport": 150,
    "entertainment": 100
  }
}
```

## 🔒 Privacy & Security

### Data Privacy
- All detailed expense reports are sent via **Direct Messages (DM)**
- Only confirmation messages appear in public channels
- Each user's data is completely isolated
- No user can see another user's expenses

### Security Best Practices
- **Never share your bot token**
- Keep your `.env` file private
- Add `.env` to `.gitignore`

### Recommended .gitignore
```
.env
*.json
__pycache__/
*.pyc
*.pyo
```

## 🎯 Budget Alerts

The bot provides smart budget warnings:

- **80% Warning**: "⚠️ You've used 80% of your Food & Dining budget!"
- **100% Alert**: "⚠️ You've exceeded your Food & Dining budget!"

These alerts appear automatically when you add expenses.

## 🐛 Troubleshooting

### Bot doesn't respond
- ✅ Verify "Message Content Intent" is enabled in Discord Developer Portal
- ✅ Check bot has proper permissions in your server
- ✅ Ensure bot is online (check terminal for "is now online!" message)

### "Module not found" error
```bash
pip install discord.py python-dotenv
```

### Token error
- ✅ Verify `.env` file exists in the same directory as `main.py`
- ✅ Check token is correct (no extra spaces or quotes)
- ✅ Regenerate token in Discord Developer Portal if needed

### Expenses not saving
- ✅ Check file permissions (bot needs write access)
- ✅ Verify `expenses.json` and `budgets.json` are not corrupted
- ✅ Try deleting JSON files and restarting (will reset data)

### DM not received
- ✅ Check your Discord privacy settings allow DMs from server members
- ✅ Ensure bot can send DMs (not blocked)

## 🔧 Customization

### Change Currency
Edit the currency symbol in `main.py`:
```python
# Find all instances of "$" and replace with your currency symbol
# Example: "€", "£", "TND", etc.
```

### Add Custom Categories
In `main.py`, modify the `CATEGORIES` dictionary:
```python
CATEGORIES = {
    "food": "🍔 Food & Dining",
    "transport": "🚗 Transportation",
    "custom_category": "🎨 Your Custom Category",  # Add here
    # ...
}
```

### Change Alert Thresholds
Modify budget alert percentages:
```python
# In the $add command section
if category_total >= budget * 0.8:  # Change 0.8 to your threshold
    warning = f"⚠️ Budget Alert!"
```

## 🚀 Future Features (Ideas)

- [ ] Export expenses to CSV/Excel
- [ ] Bill splitting with friends
- [ ] Recurring expenses (subscriptions)
- [ ] Multiple currency support
- [ ] Visual charts and graphs
- [ ] Income tracking
- [ ] Category customization per user
- [ ] Expense search and filtering
- [ ] Weekly/monthly email reports
- [ ] Integration with banking APIs

## 🤝 Contributing

Feel free to fork this project and add your own features! Some suggestions:
- Add more detailed analytics
- Implement data visualization
- Create web dashboard
- Add expense forecasting
- Multi-server support with different currencies

## 📝 License

This project is open source and available for personal and educational use.

## 💬 Support

If you encounter issues or have questions:
1. Check the Troubleshooting section
2. Verify your Discord bot settings
3. Ensure all dependencies are installed
4. Check Python version (3.8+)

## 🙏 Acknowledgments

- Built with [discord.py](https://discordpy.readthedocs.io/)
- Inspired by the need for simple, privacy-focused expense tracking

## 📊 Tips for Effective Usage

### Daily Habits
- Log expenses immediately after purchases
- Use descriptive names for better tracking
- Review your weekly spending every Sunday

### Monthly Routine
- Set budgets at the start of each month
- Review monthly summary before month ends
- Adjust budgets based on actual spending patterns

### Best Practices
- Be consistent with category selection
- Don't forget small purchases (they add up!)
- Set realistic budgets based on your income
- Use the `$list today` command before bed

---

**Made with 💰 to help you manage your finances better!**

*Version 1.0.0 - October 2025*

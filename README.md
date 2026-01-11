
This project automates the process of searching and applying for jobs on LinkedIn using Selenium.

## ⚠️ Important Warning
**Automating LinkedIn interactions is against their Terms of Service.** Using this bot may result in your account being restricted or banned. Use this tool at your own risk. It is recommended to use a secondary account for testing.

## Prerequisites
- Python 3.x
- Google Chrome browser installed

## Setup
1. Open `config.json` and update the following:
   - `email`: Your LinkedIn email.
   - `password`: Your LinkedIn password.
   - `keywords`: List of job titles/keywords to search for (e.g., "Python Developer").
   - `location`: Desired location (e.g., "New York").

2. (Optional) Adjust filters in `config.json`:
   - `avoid_unpaid`: Set to `true` to skip jobs with "unpaid" or "volunteer" in the description.

## Running the Bot
Run the following command in your terminal:
```bash
python main.py
```

## How it works
1. **Login**: Logs into your account using credentials in `config.json`.
2. **Search**: Iterates through your keywords.
3. **Filter**: Checks job descriptions for negative keywords (if `avoid_unpaid` is true).
4. **Apply**: Clicks "Easy Apply" and attempts to navigate the simplistic application form. 
   - *Note*: Complex forms requiring specific input (years of experience, phone number) may fail or be skipped.

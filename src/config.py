import yaml

config_path = "config-module/invest-app/config.yml"

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

DB_URL = config.get("db-url")
GROQ_API_KEY = config.get("groq-api-key")
LOGGING_LEVEL = config.get("logging-level")

NOTI_URLS = config.get("noti-urls")
FINANCE_REPORT_URL = NOTI_URLS.get("finance-report")
EXCEPTION_URL = NOTI_URLS.get("exception")
INVEST_APP_DEBUG_URL = NOTI_URLS.get("invest-app-debug")

SPREADSHEET_URL = config.get("google_sheet_url")

upbit = config.get("upbit")
UPBIT_ACCESS_KEY = upbit.get("access-key")
UPBIT_SECRET_KEY = upbit.get("secret-key")

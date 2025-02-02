import yaml

config_path = "config-module/invest-app/config.yml"

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

DB_URL = config.get("db-url")
GROQ_API_KEY = config.get("groq-api-key")
LOGGING_LEVEL = config.get("logging-level")

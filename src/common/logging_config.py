import logging

from config import LOGGING_LEVEL


def setup_logging():
    # 환경별로 다른 로깅 레벨 설정
    log_level = logging.DEBUG if LOGGING_LEVEL == "DEBUG" else logging.INFO
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)

    # 파일로도 로그 저장하기 (선택사항)
    # if os.getenv("LOG_TO_FILE"):
    #     file_handler = logging.FileHandler("app.log")
    #     file_handler.setFormatter(
    #         logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    #     )
    #     logger.addHandler(file_handler)

    logger.setLevel(log_level)

    # 기존 핸들러 제거 (중복 방지)
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger

logger = setup_logging()
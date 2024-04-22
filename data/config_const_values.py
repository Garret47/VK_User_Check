TABLES_DATABASE: list[str] = ['bot_settings']
TABLE_NAME_SETTING: str = 'bot_settings'
MAX_BYTE_TELEGRAM: int = 20447232
STANDARD_URL_TELEGRAM: str = 'https://api.telegram.org/file/bot'
TIMEOUT_READ_FILE: int = 30
DEFAULT_SETTINGS: dict = {'id': '', 'count': 100, 'mode': 'all', 'communities': '', 'people': ''}
STANDARD_URL_VK: str = 'https://api.vk.com/method/execute?code={0}&access_token={1}&v=5.199'
COUNT_TOKENS_IN_FILE: int = 100
COUNT_REQUEST_VK_THE_SAME: int = 3
STR_VK_CODE: str = '''API.{0}({{{1}}})'''
DEFAULT_VK_PEOPLE: list = ['first_name', 'last_name', 'id']
DEFAULT_VK_COMMUNITIES: list = ['name', 'screen_name', 'photo_200']
DEFAULT_VK_TIMEOUT: int = 30
MAX_LOAD_BYTES_FILE: int = 47185920

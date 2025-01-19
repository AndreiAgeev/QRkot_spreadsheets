# Validation error messages
BAD_NEW_DATA_ERROR = (
    'Нелья установить значение full_amount меньше уже вложенной суммы.'
)
CLOSED_PROJECT_ERROR = 'Проект закрыт. Не подлежит удалению/редактированию!'
ERROR_404 = 'Запрошенный проект отсутствует'
HAS_INVESTMENTS_ERROR = 'В проект были внесены средства, не подлежит удалению!'
NOT_UNIQUE_NAME_ERROR = 'Проект с таким именем уже существует!'


# Models and schemas constants
FULL_AMOUNT_EXAMPLE_VALUE = 100
FULL_AMOUNT_MIN = 1
INVESTED_AMOUNT_DEFAULT = 0
PROJECT_NAME_MAX_LENGTH = 100
PROJECT_NAME_MIN_LENGTH = 1
PROJECT_DESCRIPTION_MIN_LENGTH = 1


# Google API
COLUMN_COUNT = 3
DRIVE_API_VERSION = 'v3'
FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_COUNT = 100
SHEETS_API_VERSION = 'v4'
SHEETS_RANGE = 'A1:C100'

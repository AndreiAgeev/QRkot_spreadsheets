from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.extra.constants import (
    DRIVE_API_VERSION,
    FORMAT,
    SHEETS_API_VERSION,
    SHEETS_COLUMN_COUNT,
    SHEETS_RANGE,
    SHEETS_ROW_COUNT,
)
from app.extra.utils import get_timedelta


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    current_time = datetime.now().strftime(FORMAT)
    service = await wrapper_service.discover('sheets', SHEETS_API_VERSION)
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт от {current_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Текущие закрытые проекты',
                    'gridProperties': {
                        'rowCount': SHEETS_ROW_COUNT,
                        'columnCount': SHEETS_COLUMN_COUNT
                    }
                }
            }
        ]
    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: int,
        wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover('drive', DRIVE_API_VERSION)
    permission_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permission_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: int,
        projects_list: list,
        wrapper_service: Aiogoogle
) -> None:
    current_time = datetime.now().strftime(FORMAT)
    service = await wrapper_service.discover('sheets', SHEETS_API_VERSION)
    table_values = [
        ['Отчёт от', current_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects_list:
        table_values.append(
            [project['name'],
             get_timedelta(project['timedelta']),
             project['description']]
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=SHEETS_RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )

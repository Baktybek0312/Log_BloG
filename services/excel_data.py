import io
from io import BytesIO
from datetime import datetime

from sqlalchemy.orm import Session

import requests
import pandas as pd
import xlsxwriter

from models.table_posts import Post
from db.database import SessionLocal

db: Session = SessionLocal()


def get_data_report():
    """
    Функция выгрузка в excel файл постов
    """
    # from_date = datetime.strptime(show['from_date'], '%Y-%m-%d')
    # print(from_date)
    # posts = db.query(Post).all()
    # dt = []
    # for p in posts:
    #     dict_dt = {
    #         'id': p.id, 'title': p.title,
    #         'description': p.description, 'owner_id': p.owner_id,
    #         'username': p.owner_name, 'email': p.owner_email
    #     }
    #     dt.append(dict_dt)
    #
    # return dt

    posts = db.query(Post).all()
    dt = []
    for p in posts:
        dict_dt = {
            'id': p.id, 'title': p.title,
            'description': p.description, 'owner_id': p.owner_id,
            'username': p.owner_name, 'email': p.owner_email
        }
        dt.append(dict_dt)
    df = pd.DataFrame(dt)

    output = io.BytesIO()

    # Использовать объект BytesIO в качестве дескриптора файла.
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # Записать фрейм данных в объект BytesIO.
    df.to_excel(writer, sheet_name='record dataset', encoding='utf-8')
    writer.save()
    xlsx_data = output.getvalue()
    return xlsx_data

# def get_users_report(bag):
#     """
#     Функция возврощает Реестр по транзациям (по дням), в EXCEL файле.
#     Кнопка для формирования:
#     Взаиморасчеты -> Отчеты -> Реестр по транзациям (по дням).
#     """
#     from_date = datetime.strptime(bag['from_date'], '%Y-%m-%d')
#     to_date = datetime.strptime(bag['to_date'], '%Y-%m-%d')
#     to_date = to_date.replace(hour=23, minute=59, second=59, microsecond=999999)
#     total_active_count = 0
#     output = BytesIO()
#
#     with xlsxwriter.Workbook(output) as workbook:
#
#         merge_format = workbook.add_format({
#             'bold': 1,
#             'border': 1,
#             'align': 'center',
#             'valign': 'vcenter',
#             'color': 'grey'})
#
#         bold_left = workbook.add_format(
#             {'bold': True, 'align': 'left', 'border': 1})
#         border = workbook.add_format({'border': 1, 'align': 'left'})
#         table_head = workbook.add_format({'border': 1, 'bold': True})
#
#         # 1й лист
#         worksheet = workbook.add_worksheet('Пользователи')
#         worksheet.set_column('A:A', 6)
#         worksheet.set_column('B:B', 50)
#         worksheet.set_column('C:C', 65)
#         worksheet.set_column('D:D', 12)
#         worksheet.set_column('E:E', 50)
#         worksheet.set_column('F:F', 15)
#         worksheet.set_column('G:G', 50)
#
#         worksheet.write(
#             'B1:C1',
#             f'Количество пользователей ИБ/МБ (физ.лица) подключенных с '
#             f'{from_date.strftime("%d.%m.%Y")} по '
#             f'{to_date.strftime("%d.%m.%Y")} ', merge_format)
#
#         worksheet.set_row(0, 30)
#         worksheet.set_column('A:B', 20)
#
#         worksheet.write(2, 0, '№', table_head)
#         worksheet.write(2, 1, 'Филиал', table_head)
#         worksheet.write(2, 2, 'Сберкасса', table_head)
#         worksheet.write(2, 3, 'Код клиента', table_head)
#         worksheet.write(2, 4, 'ФИО клиента', table_head)
#         worksheet.write(2, 5, 'Дата создания', table_head)
#         worksheet.write(2, 6, 'Сотрудник', table_head)
#
#         query = db.session.query(Proposal).filter(Proposal.type == 'ACCESS').filter(and_(
#             Proposal.date_approve >= from_date, Proposal.date_approve <= to_date))
#
#         if bag.get('branch_id'):
#             query = query.filter(Proposal.branch_id == bag.get('branch_id'))
#
#         if bag.get('sub_branch_id'):
#             query = query.filter(Proposal.sub_branch_id == bag.get('sub_branch_id'))
#
#         if has_access('USERS_REPORT'):
#             proposals = query.order_by(Proposal.branch_id.asc(), Proposal.sub_branch_id.asc())
#         else:
#             manager = db.session.query(Manager).filter(Manager.id == get_current_manager_id()).first()
#             proposals = query.filter(manager.branch_id == Proposal.branch_id).order_by(Proposal.branch_id.asc(),
#                                                                                        Proposal.sub_branch_id.asc())
#         proposals = proposals.all()
#
#         for i, p in enumerate(proposals, start=3):
#             worksheet.write(i, 0, i - 2, border)
#             worksheet.write(i, 1, p.branch.name, border)
#             worksheet.write(i, 2, p.sub_branch.name, border)
#             worksheet.write(i, 3, p.client.client_id, border)
#             worksheet.write(i, 4, f'{p.client.surname or " "} {p.client.name or " "} {p.client.last_name or " "}',
#                             border)
#             worksheet.write(i, 5, p.date_approve.strftime("%d.%m.%Y"), border)
#             worksheet.write(i, 6, p.manager.name, border)
#
#     response = make_xls_file_response(output.getvalue())
#
#     return response

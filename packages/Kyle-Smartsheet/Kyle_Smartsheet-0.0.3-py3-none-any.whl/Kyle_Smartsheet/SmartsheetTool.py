import smartsheet
import logging
import smartsheet.models, smartsheet.sheets, smartsheet.search, smartsheet.attachments, smartsheet.folders, \
    smartsheet.workspaces
from smartsheet_dataframe import get_as_df, get_sheet_as_df
import warnings
import pandas as pd


class KSmartSheet():
    
    def __init__(self, token):
        KSmartSheet.smart = smartsheet.Smartsheet(token)
        KSmartSheet.smart.errors_as_exceptions(True)
        logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

    def get_way_add(self):
        s = '''
        sheet = KSheet(sheet_id,token)
        dictID_re = sheet.get_columnID()
        dic_value = sheet.convert_df_to_dict(df)
        lst_column_request = list(dic_value.keys())
        
        lst_row = []
        for i in range(df.shape[0]):
        
            lst_column=[]
        
            for j in range(len(lst_column_request)):
        
                cell1 = smart.models.Cell({
                    'column_id':dictID_re[lst_column_request[j]],
                    'object_value': dic_value[lst_column_request[j]][i]
                    })
        
                lst_column.append(cell1)
        
            row = smart.models.Row({
                'cells': lst_column
            })
        
            row.to_top=True
        
            lst_row.append(row)
        
        added_row = smart.Sheets.add_rows(
            sheet_id,  # sheet_id
            lst_row)
        '''
        return s

class KSheet():

    def __init__(self, SheetId, token):
        s = KSmartSheet(token)
        self.SheetId = SheetId
        self.smart = s.smart
        self.token = token

    def get_dataframe(self, include_row_id=True, include_parent_id=True):
        df = get_sheet_as_df(token=self.token,
                             sheet_id=self.SheetId,
                             include_row_id=include_row_id,
                             include_parent_id=include_parent_id
                             )
        return df

    def get_columnID(self):
        response = self.smart.Sheets.get_columns(
            self.SheetId,  # sheet_id
            include_all=True)
        columns_re = response.data
        cid_re = []
        cname_re = []
        for i in range(len(columns_re)):
            cname_re.append(str(columns_re[i].title))
            cid_re.append(columns_re[i].id)
        dictID_re = {}
        for i in range(len(columns_re)):
            dictID_re.update({cname_re[i]: cid_re[i]})
        return dictID_re

    def get_columnType(self):
        response = self.smart.Sheets.get_columns(
            self.SheetId,  # sheet_id
            include_all=True)
        columns_re = response.data
        cname_re = []
        type_re = []
        for i in range(len(columns_re)):
            cname_re.append(str(columns_re[i].title))
            type_re.append(columns_re[i].type_.value.name)
        dictType_re = {}
        for i in range(len(columns_re)):
            dictType_re.update({cname_re[i]: type_re[i]})
        return dictType_re
        
    def convert_df_to_dict(self, df):
        dic_value = {}
        for i in range(len(df.columns.tolist())):
            dic_value.update({df.columns.tolist()[i]: df[df.columns.tolist()[i]].tolist()})
        return dic_value

    def add_rows(self, df, parentID='parentID', siblingID ='siblingID'):

        dictID_re = self.get_columnID()
        dictType_re = self.get_columnType()
        dic_value = self.convert_df_to_dict(df)
        lst_column_request = list(dic_value.keys())

        # Update or Add rows

        lst_row = []

        for i in range(df.shape[0]):

            lst_column = []

            for j in range(len(lst_column_request)):
                if dictType_re[lst_column_request[j]] == 'DATE':
                    cell1 = self.smart.models.Cell({
                        'column_id': dictID_re[lst_column_request[j]],
                        'value': dic_value[lst_column_request[j]][i]
                    })
                else :
                    cell1 = self.smart.models.Cell({
                        'column_id': dictID_re[lst_column_request[j]],
                        'object_value': dic_value[lst_column_request[j]][i]
                    })

                lst_column.append(cell1)

            row = self.smart.models.Row({
                'cells': lst_column
            })

            if (parentID == 'parentID') & (siblingID == 'siblingID'):
                row.to_top = True
            elif (parentID != 'parentID') & (siblingID == 'siblingID'):
                row.parent_id = parentID
            elif (parentID == 'parentID') & (siblingID != 'siblingID'):
                row.sibling_id = siblingID

            # row.id = rowID
            lst_row.append(row)

        added_row = self.smart.Sheets.add_rows(
            self.SheetId,  # sheet_id
            lst_row)

    def update_rows(self, df, lstID):

        dictID_re = self.get_columnID()
        dictType_re = self.get_columnType()
        dic_value = self.convert_df_to_dict(df)
        lst_column_request = list(dic_value.keys())

        # Update or Add rows

        lst_row = []

        for i in range(df.shape[0]):

            lst_column = []

            for j in range(len(lst_column_request)):
                
                if dictType_re[lst_column_request[j]] == 'DATE':
                    cell1 = self.smart.models.Cell({
                        'column_id': dictID_re[lst_column_request[j]],
                        'value': dic_value[lst_column_request[j]][i]
                    })
                else:
                    cell1 = self.smart.models.Cell({
                        'column_id': dictID_re[lst_column_request[j]],
                        'object_value': dic_value[lst_column_request[j]][i]
                    })

                lst_column.append(cell1)

            row = self.smart.models.Row({
                'cells': lst_column
            })

            row.id_ = lstID[i]

            # row.id = rowID
            lst_row.append(row)

        updated = self.smart.Sheets.update_rows(
            self.SheetId,  # sheet_id
            lst_row)
        
    def delete_rows(self,lst_deleteID):
        deleted = self.smart.Sheets.delete_rows(
            self.SheetId,  # sheet_id
            lst_deleteID)  # row_ids



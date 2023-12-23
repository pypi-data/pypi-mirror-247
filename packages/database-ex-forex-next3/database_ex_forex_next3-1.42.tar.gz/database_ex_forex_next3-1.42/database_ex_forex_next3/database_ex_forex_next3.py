import sqlite3
from sqlite3 import Error


class Database:

        try:
            global con
            con = sqlite3.connect('Expert.db')
            cur = con.cursor()
        except:
            print("connect error DB") 
        
        def sql_connection():
             try:
               con = sqlite3.connect('Expert.db')
               return con
             except:
              print("connect error DB") 
        
        def sql_table(con):
             cursorobj = con.cursor()
             cursorobj.execute("CREATE TABLE Epizode(ID integer primary key AUTOINCREMENT , Patern_num text , Type text , point_Pattern json , point_5 text , point_5_time text , command text , candel_coler json , price_candel_open json , price_candel_close json , gap_point json , gap_amount json,gap_pip json,gap_word json , tension text , status text , chek text , time_start_search text , time_end_Pattern text , timestamp json , times json , ticket text , line_POS json , repetition_POS text , rep_patern_num text , Trust_patern text , Trust_patern_full text , Layout_patern text , Jump_patern text , News text , Jump_1mine text , Type_purchase text)")
             con.commit()
        
        def create_table():
             cone = Database.sql_connection()
             Database.sql_table(cone)    #create database
        
        def insert_table(value):
            # try: 
               cursorobj = con.cursor()
               cursorobj.execute('INSERT INTO Epizode (Patern_num , Type , point_Pattern , point_5 , point_5_time  , command , candel_coler , price_candel_open , price_candel_close , gap_point , gap_amount , gap_pip , gap_word , tension , status , chek , time_start_search , time_end_Pattern , timestamp , times , ticket , line_POS , repetition_POS , rep_patern_num , Trust_patern , Trust_patern_full , Layout_patern , Jump_patern , News , Jump_1mine , Type_purchase) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', value )
               con.commit()
               print("Record INSERT successfully")
               cursorobj.close()
            # except sqlite3.Error as error:
            #    print("Failed to INSERT reocord from a sqlite table", error)    

        def select_table_All():
            try: 
               cursorobj = con.cursor()
               sqlite_select_query = """SELECT * from Epizode  """
               cursorobj.execute(sqlite_select_query)
               record = cursorobj.fetchall()
               # print("Select_All reocord from a sqlite table")
               return record
            except sqlite3.Error as error:
               print("Failed to Select_All reocord from a sqlite table", error)    
 
        def select_table_One(patern_num):
            try: 
               cursorobj = con.cursor()
               sqlite_select_query = '''SELECT * from Epizode WHERE patern_num = ? '''
               cursorobj.execute(sqlite_select_query , (patern_num ,))
               record = cursorobj.fetchall()
               # print("Record Select successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to select_one reocord from a sqlite table", error)  

        def select_table_Two(patern_num , type):
            try: 
               cursorobj = con.cursor()
               sqlite_select_query = '''SELECT * from Epizode WHERE patern_num = ? and Type = ?'''
               cursorobj.execute(sqlite_select_query , (patern_num , type,))
               record = cursorobj.fetchall()
               # print("Record Select successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to select_one reocord from a sqlite table", error)   

        def delete_table(patern_num ):
            try:
               cursorobj = con.cursor()
               sqlite_select_query = '''DELETE  from Epizode WHERE patern_num = ?  '''
               cursorobj.execute(sqlite_select_query , (patern_num , ))
               record = con.commit()
               print("Record Delete successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to delete reocord from a sqlite table", error)  
               
        def delete_table_All():
            try:
               cursorobj = con.cursor()
               sqlite_select_query = '''DELETE from Epizode '''
               cursorobj.execute(sqlite_select_query )
               record = con.commit()
               print("Record Delete_All successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to delete reocord from a sqlite table", error)        
             
        def update_table_gap(gap_point , gap_amount , gap_pip , gap_word , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET gap_point = ? , gap_amount = ? , gap_pip = ? , gap_word = ?  where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (gap_point , gap_amount , gap_pip , gap_word , patern_num) )
               record = con.commit()
               # print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)   

        def update_table_status(status  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET status = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (status  , patern_num) )
               record = con.commit()
               # print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)

        def update_table_status_chek(chek  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET chek = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (chek  , patern_num) )
               record = con.commit()
               # print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)


        def update_table_repetition_pos(repetition_pos  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET repetition_pos = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (repetition_pos  , patern_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)

        def update_table_trust_patern(trust_patern  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET  Trust_patern = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (trust_patern , patern_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error) 

        def update_table_trust_patern_full(trust_patern_full  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET  Trust_patern_full = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (trust_patern_full , patern_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)           

        def update_table_Layout_patern(Layout_patern  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET Layout_patern = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (Layout_patern , patern_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)  

        def update_jump_patern(Jump_patern  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET Jump_patern = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (Jump_patern , patern_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)   

        async def update_Type_purchase(Type_purchase , ID):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET Type_purchase = ?   where  ID = ?"""
               cursorobj.execute(sqlite_update_query , (Type_purchase  , ID ) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)

        def update_jamp_1mine_manage(Jump_1mine  , patern_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET Jump_1mine = ?   where patern_num = ?"""
               cursorobj.execute(sqlite_update_query , (Jump_1mine , patern_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)                   

        async def update_table_chek(point_5 , point_5_time  , command , chek , ticket , line_POS , news , ID ):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET point_5 = ? , point_5_time =? , command = ? , chek = ? , ticket = ? , line_POS = ? , News = ? where ID = ?"""
               cursorobj.execute(sqlite_update_query , (point_5 , point_5_time , command , chek , ticket , line_POS , news , ID) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)                   

        
import MetaTrader5 as mt5
import json
import pandas as pd
import time
import collections

from line_ex_forex_next3 import LINE
from buy_sell_ex_forex_next3 import BUY_SELL
from database_ex_forex_next3 import Database
from decimal import Decimal
from common_pos_ex_forex_next3 import Pos_Common
from news_ex_forex_next3 import NEWS
from balance_mange_trade_ex_forex_next3 import Manage_balance_trade


from decimal import Decimal



class Pullback:
 
 def __init__(self , symbol_crypto , decimal_sambol ):
      
      fileObject = open("login.json", "r")
      jsonContent = fileObject.read()
      aList = json.loads(jsonContent)
      
      self.symbol_crypto = symbol_crypto
      self.decimal_sambol = decimal_sambol

      self.Time_news_effect = int(aList['Time_news_effect_minute'] )
      self.ratio_spread_pip_TP = (aList['ratio_spread_pip_TP'] )
      self.Min_Power_move = int (aList['Min_Power_move'] )

 def __str__(self):
      return f"({self.symbol_crypto },{self.decimal_sambol } , {self.Time_news_effect} , {self.ratio_spread_pip_TP})"

 def decimal(num , decimal_sambol):
        telo = '0.0'
        for i in range(decimal_sambol - 2):  
          telo = telo + "0"
        telo = telo + "1" 
        telo = float (telo)
        decimal_num = Decimal(str(num))
        rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
        return rounded_num  


 async def pullback_3_old (self , lot ):
               
    data_all = Database.select_table_All()
    #   print("data_all:" , data_all)

    select_all_len = len(data_all)
    print("select_all_len:" , select_all_len)
    input_patern = int(select_all_len / 2)

    if select_all_len > 0:

         
        data_patern = Database.select_table_One(input_patern)
        # print("data_patern:" , data_patern)
            
        for index in range(1) : 

            # print("indexs:" , index)
            lab = data_patern[0]
            # print("lab:" , lab)
            id = lab[0]
            patern_num = lab[1]
            type = lab[2]
            point_patern = lab[3]
            status = lab[15]
            chek = lab[16]
            time_start_search = lab[17]
            timepstamp = lab[19] 
            line_POS = lab[22]
            Trust_patern = lab[25]
            Trust_patern_full = lab[26]
            Layout_patern = lab [27]
            Jump_patern = lab [28]
            Type_purchase = lab[31]


            exit = 0
            line = []
            list_timpstamp_sec = []
            list_pullback3 = []
            Type_purchase_pos = []
            line_pullback = 0
            point_close_3 = 0
            status_patern_pos = True
            pos_buy = False
            pos_sell = False
            
          #   print("select_all_len:" , select_all_len)
            rec = data_all[select_all_len - 1]
            # print("rec:" , rec)

            time_start_search = int(time_start_search)
            time_end_search = int(time_start_search) - 60
            point_patern = json.loads(point_patern)
            timepstamp = json.loads(timepstamp)
            timepstamp_3 = json.loads(timepstamp[3])
            timepstamp_start = int(timepstamp_3) + 900
            line_POS = json.loads(line_POS)
 
            status_type = ''

            if type == "Two_TOP":
                status_type = 'T'

            elif type == "Two_Bottom":
                status_type = 'B'     

                   
            if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "false" :

                print("pullback_now 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")

                print("patern_num:" , patern_num )


                list_point = []
                list_point_left_right = []
                list_point_group = []
                list_lines = []

                list_line_pullback = []
                list_count_pullback_total = []
                list_num_pullback_puyesh = []
                list_num_pullback = []
                list_num_pullback_trade = []
                list_model_pullback = []
                list_shakhes_pullback = []
                list_time_shakhes_line = []
                
                
                inputs_candels = mt5.copy_rates_range(self.symbol_crypto, mt5.TIMEFRAME_M1, timepstamp_start , time_end_search)

                # print("inputs_candels:" , inputs_candels)
                # print("point_patern:" , point_patern)
                # print ("timestamp_pulback:" , timestamp_pulback) 
                
                def tp_max_buy(time_start_search_tp_max):  
                    inputs_candels_tp_max = mt5.copy_rates_range(self.symbol_crypto, mt5.TIMEFRAME_M1, time_start_search_tp_max, time_end_search)
                    list_max_candel = []
                    for i_max in inputs_candels_tp_max:
                        list_max_candel.append(i_max[2])
                    # print("list_max_candel:" , list_max_candel)    
                    price_max = max(list_max_candel)
                    price_max = Pullback.decimal(price_max , self.decimal_sambol)
                    price_max = float(price_max)
                    list_max_candel = []
                    return price_max

                def tp_min_sell(time_start_search_tp_min):
                    inputs_candels_tp_min = mt5.copy_rates_range(self.symbol_crypto, mt5.TIMEFRAME_M1, time_start_search_tp_min, time_end_search)
                    # print("inputs_candels_tp_min:", inputs_candels_tp_min)

                    list_min_candel = []
                    print(pd.to_datetime( time_start_search_tp_min , unit='s') )
                    for i_min in inputs_candels_tp_min:
                        list_min_candel.append(i_min[3])
                    # print("list_min_candel:" , list_min_candel)
                    price_min = min(list_min_candel)
                    price_min = Pullback.decimal(price_min , self.decimal_sambol)
                    price_min = float(price_min)
                    list_min_candel = []
                    return price_min


                for indexs , candel_recive in enumerate(inputs_candels): 
                  # if indexs == 9:
                    #  print("candel_recive:" , candel_recive)
                    #  print("indexs:" , indexs)

                    #  if indexs == 10 :
                    #       quit()
                     
            #    try:
                    
                    point_timepstamp =  candel_recive[0]
                    point_timepstamp = int (point_timepstamp)
                    # print("point_timepstamp:" , point_timepstamp)

                    utc_from = pd.to_datetime( point_timepstamp  , unit='s') 
                    utc_to = pd.to_datetime( point_timepstamp + 59 , unit='s')

                    # utc_from = pd.to_datetime( 1703173500  , unit='s') 
                    # utc_to = pd.to_datetime( 1703173500 + 59 , unit='s')
                        
                    ticks = mt5.copy_ticks_range(self.symbol_crypto , utc_from, utc_to , mt5.COPY_TICKS_ALL)
                    # print("ticks:" ,len(ticks) )

                    #  time.sleep(1)
    
                    for lists in ticks:
                         xx = Pullback.decimal(lists[1] , self.decimal_sambol)
                         xx = float(xx)
                         list_pullback3.append(xx)
                         list_timpstamp_sec.append(lists[0])
           

                    len_pullback = len(list_pullback3) 
                    len_pullback = len_pullback - 1
                    # print("Number_list_candel:" , len_pullback) 

                    
                    # print("list_pullback3:" , list_pullback3)  

                    # print("list_timpstamp_sec:" , list_timpstamp_sec) 
                    index_tick_time = point_timepstamp

                    # print("patern_num:" , patern_num)
                    # print("index_tick_time:" , index_tick_time)
                    print (pd.to_datetime( index_tick_time , unit='s'))
                    cal_line_rec =  LINE.line_run(patern_num , self.symbol_crypto , index_tick_time )
                    cal_line = cal_line_rec[0]
                    cal_list_line = cal_line_rec[1]
                    #  print("line_POS:" , line_POS)
                    # print("cal_line:" , cal_line)

                    # cal_line = [ 1.09996 ]
            
                    try:
                            
                        for index_line , index_point in enumerate(list_pullback3): 
                                
                                    index_point = float (index_point)
                                   
                                    if index_point in cal_line and index_line < len_pullback and index_line > 0:

                                            list_point_left_right.append(list_pullback3[index_line - 1])
                                            list_point_left_right.append(list_pullback3[index_line])
                                            list_point_left_right.append(list_pullback3[index_line + 1])
  
                                    if list_point_left_right != [] and len(list_point_left_right) == 3:
                                      
                                            list_point_group.append([list_point_left_right , list_timpstamp_sec[index_line]])
                                            # print("list_point_group:" , list_point_group) 
                                            list_point_left_right = []
                         
                    except:
                         print("error list_pullback3[indexs + 1]")
                   
                                 
                    if list_point_group != []:
                                         
                        # print("list_point_group:" , list_point_group)  

                        for index_lines , list_group in enumerate(list_point_group):
                            for i_line , index_line_pullback in enumerate(cal_line):
                                if index_line_pullback in list_group[0]:
                                    point_close_3 = list_group[0][1]
                                    left_candel = list_group[0][0]
                                    right_candel = list_group[0][2]
                                    line_pullback = i_line + 1
                                    if point_close_3 > left_candel and point_close_3 > right_candel:
                                        list_line_pullback.append([line_pullback , list_group , "M"])
                                        #  line_pullback_input(line_pullback , point_close_3)
                                    elif point_close_3 < left_candel and point_close_3 < right_candel:
                                        list_line_pullback.append([line_pullback , list_group , "H"]) 

           
                    # list_line_pullback = [[1, [[1.0894, 1.08939, 1.08941], 1703176622] , 'H'] , [2, [[1.0894, 1.08939, 1.08941], 1703176626] ,'M'], 
                    #                       [1, [[1.0894, 1.08939, 1.08941], 1703176642] ,'M'] , [2, [[1.0894, 1.08939, 1.08941], 1703176622] ,'H']]
                                          
                    # list_line_pullback: [[1, [[1.09961, 1.09962, 1.09961], 1703176622], 'H']]
                    # print("list_line_pullback:" , list_line_pullback)

                    # list_line_pullback = [[1, 1.09882, 1703175070, 'H'] , [1, 1.09882, 1703175071, 'H']]
                    

                    def duplicate(items):
                                unique = []
                                for item in items:
                                    if item not in unique:
                                        unique.append(item)
                                return unique
                        
                    if list_line_pullback:

                        len_call_line = len(cal_line)
                        # print("len_call_line:" , len_call_line)
                        for index_num , i_count in enumerate(list_line_pullback):
                            for ix in range(len_call_line + 1):
                                if ix == i_count[0]:
                                     list_count_pullback_total.append([i_count[0] , i_count[2]])  

                        list_count_pulback = duplicate(list_count_pullback_total)
                  
                        for ii in list_count_pulback:
                            list_num_pullback.append(ii[0])

                        for ic in list_num_pullback:
                            
                            xxx = list_count_pullback_total.count([ic, 'M'])  
                            if xxx:
                                list_num_pullback_puyesh.append([ic , 'M' ,[xxx]])

                            xxxx = list_count_pullback_total.count([ic, 'H'])    
                            if xxxx:
                                list_num_pullback_puyesh.append([ic , 'H' ,[xxxx]])             


                        # print("")
                        # print("list_count_pullback_total:" , list_count_pullback_total)


                        for indexx , i_puyesh in enumerate(list_line_pullback):
                       
                            list_lines.append([i_puyesh[0] , i_puyesh[1][0][1] , i_puyesh[1][1] , i_puyesh[2]])
                            list_time_shakhes_line.append(i_puyesh[1][1])
                         
                        # list_model_pullback = duplicate(list_model_pullback)

                        min_time_shakhes = min(list_time_shakhes_line)


                        list_trade_shakhes_1 = []
                        list_trade_shakhes_2 = []

                        for i_trade_shahes_1 in list_lines:
                            if min_time_shakhes == i_trade_shahes_1[2]:
                                list_trade_shakhes_1.append(i_trade_shahes_1)

                        list_trade_shakhes_1 = duplicate(list_trade_shakhes_1)

                        status_rep = ''
                       
                        if list_trade_shakhes_1:
                            for i_trade_shahes_2 in list_lines:
                                if list_trade_shakhes_1[0][3] == 'H':
                                    status_rep = 'M'
                                elif list_trade_shakhes_1[0][3] == 'M':
                                    status_rep = 'H'

                                for is1 in list_trade_shakhes_1 :   

                                    if is1[0] == i_trade_shahes_2[0] and i_trade_shahes_2[3] == status_rep :
                                        list_trade_shakhes_2.append(i_trade_shahes_2)


                        # print("list_num_pullback_puyesh:" , list_num_pullback_puyesh)            
                        # print("")  

                        # print("list_lines:" , list_lines)
                        print("")        
                        
                        print("list_trade_shakhes_1:" , list_trade_shakhes_1)
                        print("list_trade_shakhes_2:" , list_trade_shakhes_2)
                        print("")
                    
                        print("")

                        print("line_POS:" , line_POS)

                        if list_trade_shakhes_1:
                            for i_lts1 in list_trade_shakhes_1:
                                Type_purchase_pos.append(i_lts1[3])
                                list_shakhes_pullback.append(i_lts1[1])
                     
                        if list_trade_shakhes_2:
                            for i_lts2 in list_trade_shakhes_2:
                                Type_purchase_pos.append(i_lts2[3])
                                list_shakhes_pullback.append(i_lts2[1])

                        Type_purchase_pos = duplicate(Type_purchase_pos)
                        print("Type_purchase_pos:" , Type_purchase_pos)
                        print("list_shakhes_pullback:" , list_shakhes_pullback)

                        min_close_point = min(list_shakhes_pullback)
                        print("min_close_point:" , min_close_point)

                        max_close_point = max(list_shakhes_pullback)
                        print("max_close_point:" , max_close_point)

                                
                        list_num_pullback_pos = []

                        point5_buy = 0
                        point5_sell = 0
      
                        if line_POS:
                          
                            if line_POS[0] != 0:
                               
                                list_num_pullback_pos = line_POS  

                                if list_trade_shakhes_1:
                                    for ims1 in list_trade_shakhes_1:
                                        for ilp in line_POS:
                                            if ilp == ims1[0] and ims1[3] == 'H' and Type_purchase == 'H':
                                                pos_buy = True
                                                point5_buy = ims1[1]
                                            elif ilp == ims1[0] and ims1[3] == 'M' and Type_purchase == 'M':
                                                pos_sell = True   
                                                point5_buy = ims1[1]   

                                if list_trade_shakhes_2:
                                    for ims2 in list_trade_shakhes_2:
                                        for ilp in line_POS:
                                            if ilp == ims2[0] and ims2[3] == 'H' and Type_purchase == 'H':
                                                pos_buy = True
                                                point5_sell = ims2[1]
                                            elif ilp == ims2[0] and ims2[3] == 'M' and Type_purchase == 'M':
                                                pos_sell = True   
                                                point5_sell = ims2[1]

                            elif line_POS[0] == 0:   

                                for i_tp in Type_purchase_pos:
                                    if i_tp == 'H':
                                        pos_buy = True
                                        point5_buy = min_close_point
                                    elif i_tp == 'M':
                                        pos_sell = True  
                                        point5_sell = max_close_point  

                                for i_line_pos in list_trade_shakhes_1: 
                                    list_num_pullback_pos.append(i_line_pos[0])
                                

                        print("pos_buy:" , pos_buy)
                        print("pos_sell:" , pos_sell)

                        list_num_pullback_pos = duplicate(list_num_pullback_pos)
                                        
                        list_num_pullback_pos = json.dumps(list_num_pullback_pos)
                        print("list_num_pullback_pos:" , list_num_pullback_pos)

                        # ////////////////////////////// BUY //////////////////////////
                        # /////////////////////////////////////////////////////////////

                        if chek == "false" and pos_buy == True and point5_buy > 0:
                            
                            time_command = pd.to_datetime(index_tick_time , unit='s')
                            shakhes = LINE.line_shakhes(patern_num , self.symbol_crypto , self.decimal_sambol , point5_buy , "buy")
                            status_trade = shakhes[1]
                            print("status_trade:" , status_trade)
                            shakhes = int (shakhes[0])

                            ticket = 0
                            execution = ''
                            recive_time_news = ''
                            status_News = 'false'
                            time_news = ''
                            status_manage_balance = "false"

                            recive_time_news = NEWS.cal_time(self.Time_news_effect)
                            manage_balance =  Manage_balance_trade.balance_candel( lot , 'buy' , self.symbol_crypto)       
                            print("manage_balance:" , manage_balance)

                            if status_trade == True:
                                point = mt5.symbol_info(self.symbol_crypto).point
                                tp = point5_buy + (shakhes * point)
                                tp = BUY_SELL.decimal(tp , self.decimal_sambol)
                                tp_total = float(tp)
                                tp_max_buy_rec = tp_max_buy(point_timepstamp)
                                print("tp_max_buy_rec:" , tp_max_buy_rec)
                    
                                status_old_tp_buy = False

                                if tp_total > tp_max_buy_rec: 
                                    status_old_tp_buy = True

                                comment = f'{patern_num}' + "_" + f'{status_type}'+'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'+'O'
                               
                                if recive_time_news[0] == False and manage_balance == False and status_old_tp_buy == True:   
                                    status_News = 'false'  
                                    status_manage_balance = "false"  
                                    rec_pos = await BUY_SELL.pos_buy( tp_total , lot  , comment)   
                                    if rec_pos:
                                        execution = rec_pos.comment
                                        if execution == 'Request executed':
                                            ticket =  rec_pos.order                       
                                
                                else:
                                    ticket = 123456789

                            elif status_trade == False:
                                if shakhes >= self.Min_Power_move:
                                    ticket = 123456789
                                elif shakhes < self.Min_Power_move:
                                    ticket = 0    
                      
                            if recive_time_news[0] == True: 
                                status_News = 'true'   
                                time_news = recive_time_news[1]

                            if manage_balance == True:
                                status_manage_balance = 'true' 
                        
                            command = "(Patern:" + f'{patern_num})' + " _ " + "(position: BUY)" + " _ " + "(Line:" + f'{list_num_pullback_puyesh})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{3})'+ " _ " + "(Point5:" + f'{point5_buy})' + " _ " + "(Time:" + f'{time_command})'  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'+ " _ " + "(status_News:" + f'{status_News})'+ " _ " + "(time_news:" + f'{time_news})' + " _ " + "(status_manage_balance:" + f'{status_manage_balance})' 
                            status_chek = False
                            data_patern = Database.select_table_One(patern_num)
                            if data_patern: 
                                for index_patern , data_patern_num in enumerate(data_patern): 
                                        id = data_patern_num[0]
                                        Type_purchase = data_patern_num[31]
                                        if Type_purchase == 'H':
                                            await Database.update_table_chek(point5_buy , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)
                                            status_chek = True 
                                if status_chek == False:
                                    for index_patern , data_patern_num in enumerate(data_patern): 
                                        id = data_patern_num[0]
                                        await Database.update_table_chek(point5_buy , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)

                        #/////////////////////////////// SELL /////////////////////////
                        #//////////////////////////////////////////////////////////////
                                            
                        if chek == "false" and pos_sell == True and point5_sell > 0:
                            time_command = pd.to_datetime(index_tick_time , unit='s')
                            shakhes = LINE.line_shakhes(patern_num , self.symbol_crypto , self.decimal_sambol , point5_sell , "sell")
                            status_trade = shakhes[1]
                            print("status_trade:" , status_trade)
                            shakhes = int (shakhes[0])

                            ticket = 0
                            execution = ''
                            recive_time_news = ''
                            status_News = 'false'
                            time_news = ''
                            status_manage_balance = "false"

                            recive_time_news = NEWS.cal_time(self.Time_news_effect)

                            manage_balance =  Manage_balance_trade.balance_candel( lot , 'sell' , self.symbol_crypto)       
                            print("manage_balance:" , manage_balance)

                            if status_trade == True:
                                point = mt5.symbol_info(self.symbol_crypto).point
                                tp = point5_sell - (shakhes * point)
                                tp = BUY_SELL.decimal(tp , self.decimal_sambol)
                                tp_total = float(tp) 
                                print("tp_total:" , tp_total)

                                tp_min_sell_rec = tp_min_sell(point_timepstamp)
                                print("tp_min_sell_rec:" , tp_min_sell_rec)
                    
                                status_old_tp_sell = False

                                if tp_total < tp_min_sell_rec: 
                                    status_old_tp_sell = True

                                comment = f'{patern_num}' + "_" + f'{status_type}'+'M' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'+'O'
                               
                                if recive_time_news[0] == False and manage_balance == False and status_old_tp_sell == True:   
                                    status_News = 'false'  
                                    status_manage_balance = "false"  
                                    rec_pos = await BUY_SELL.pos_sell( tp_total , lot  , comment)   
                                    if rec_pos:
                                        execution = rec_pos.comment
                                        if execution == 'Request executed':
                                            ticket =  rec_pos.order                       
                                
                                else:
                                    ticket = 123456789

                            elif status_trade == False:
                                
                                if shakhes >= self.Min_Power_move:
                                    ticket = 123456789
                              
                                elif shakhes < self.Min_Power_move:
                                    ticket = 0 
                      
                            if recive_time_news[0] == True: 
                                status_News = 'true'   
                                time_news = recive_time_news[1]

                            if manage_balance == True:
                                status_manage_balance = 'true' 
                        
                            command = "(Patern:" + f'{patern_num})' + " _ " + "(position: SELL)" + " _ " + "(Line:" + f'{list_num_pullback_puyesh})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{3})'+ " _ " + "(Point5:" + f'{point5_sell})' + " _ " + "(Time:" + f'{time_command})'  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'+ " _ " + "(status_News:" + f'{status_News})'+ " _ " + "(time_news:" + f'{time_news})' + " _ " + "(status_manage_balance:" + f'{status_manage_balance})' 
                            status_chek = False
                            data_patern = Database.select_table_One(patern_num)
                            if data_patern: 
                                for index_patern , data_patern_num in enumerate(data_patern): 
                                    id = data_patern_num[0]
                                    Type_purchase = data_patern_num[31]
                                    if Type_purchase == 'M':
                                        await Database.update_table_chek(point5_sell , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)
                                        status_chek = True
                                if status_chek == False:
                                    for index_patern , data_patern_num in enumerate(data_patern): 
                                        id = data_patern_num[0]
                                        await Database.update_table_chek(point5_sell , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)


                    if pos_buy == True or pos_sell == True:
                        break

                    list_pullback3 = []
                    Type_purchase_pos = []
                    list_lines = []
                    list_trade_shakhes_1 = []
                    list_trade_shakhes_2 = []
                    list_point_group = []
                    list_line_pullback = []
                    list_num_pullback_pos = []
                    list_num_pullback = []
                    list_shakhes_pullback = []


 async def pullback_3_now (self , timestamp_pulback , lot , status_end):
               
      data_all = Database.select_table_All()
    #   print("data_all:" , data_all)

      select_all_len = len(data_all)
      print("select_all_len:" , select_all_len)

      if select_all_len > 0:
               
         for index in range(select_all_len):
                          
            # print("indexs:" , index)
            lab = data_all[index]
            # print("lab:" , lab)
            id = lab[0]
            patern_num = lab[1]
            type = lab[2]
            point_patern = lab[3]
            status = lab[15]
            chek = lab[16]
            time_start_search = lab[17]
            timepstamp = lab[19] 
            line_POS = lab[22]
            Trust_patern = lab[25]
            Trust_patern_full = lab[26]
            Layout_patern = lab [27]
            Jump_patern = lab [28]
            Type_purchase = lab[31]


            exit = 0
            line = []
            list_timpstamp_sec = []
            list_pullback3 = []
            line_pullback = 0
            point_close_3 = 0
            status_patern_pos = True
            pos_buy = False
            pos_sell = False
            
          #   print("select_all_len:" , select_all_len)
            rec = data_all[select_all_len - 1]
            # print("rec:" , rec)

            time_start_search = int(time_start_search)
            point_patern = json.loads(point_patern)
            timepstamp = json.loads(timepstamp)
            timepstamp_3 = json.loads(timepstamp[3])
            line_POS = json.loads(line_POS)
 
            status_type = ''

            if type == "Two_TOP":
                status_type = 'T'

            elif type == "Two_Bottom":
                status_type = 'B'     

            if status_end == True:
                data_patern = Database.select_table_One(patern_num)
                if data_patern:
                    # print("data_patern:" , data_patern)
                    for index_db in data_patern:
                        chek = index_db[16]
                        
                        if chek == "true":
                            Database.update_table_status_chek("true" , patern_num)
                   
            if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "false" and status_end == False:

                print("pullback_now 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")

                print("patern_num:" , patern_num )


            
                list_point_left_right = []
                list_point_group = []
                list_lines = []

                list_line_pullback = []
                list_count_pullback_total = []
                list_num_pullback_puyesh = []
                list_num_pullback = []
                list_num_pullback_trade = []
                list_model_pullback = []
                list_shakhes_pullback = []
                list_time_shakhes_line = []
                
                
                inputs_candels = mt5.copy_rates_from(self.symbol_crypto, mt5.TIMEFRAME_M1,  timestamp_pulback , 1)

                # print("inputs_candels:" , inputs_candels)
                # print("point_patern:" , point_patern)
                # print ("timestamp_pulback:" , timestamp_pulback) 

                for indexs , candel_recive in enumerate(inputs_candels): 
                  # if indexs == 9:
                    #  print("candel_recive:" , candel_recive)
                    #  print("indexs:" , indexs)

                    #  if indexs == 10 :
                    #       quit()
                     
            #    try:
                    
                    point_timepstamp =  candel_recive[0]
                    point_timepstamp = int (point_timepstamp)
                    #  print("point_timepstamp:" , point_timepstamp)

                    utc_from = pd.to_datetime( point_timepstamp , unit='s') 
                    utc_to = pd.to_datetime( point_timepstamp + 59 , unit='s')
                        
                    ticks = mt5.copy_ticks_range(self.symbol_crypto , utc_from, utc_to , mt5.COPY_TICKS_ALL)
                    # print("ticks:" ,len(ticks) )

                    #  time.sleep(1)
    
                    for lists in ticks:
                         xx = Pullback.decimal(lists[1] , self.decimal_sambol)
                         xx = float(xx)
                         list_pullback3.append(xx)
                         list_timpstamp_sec.append(lists[0])


                    len_pullback = len(list_pullback3) 
                    len_pullback = len_pullback - 1
                    # print("Number_list_candel:" , len_pullback) 

                    
                    # print("list_pullback3:" , list_pullback3)  

                    # print("list_timpstamp_sec:" , list_timpstamp_sec) 

                    index_tick_time = int(list_timpstamp_sec[0])
                    # print("patern_num:" , patern_num)
                    # print("index_tick_time:" , index_tick_time)
                    print (pd.to_datetime( index_tick_time , unit='s'))
                    cal_line_rec =  LINE.line_run(patern_num , self.symbol_crypto , index_tick_time )
                    cal_line = cal_line_rec[0]
                    cal_list_line = cal_line_rec[1]
                    #  print("line_POS:" , line_POS)
                    print("cal_line:" , cal_line)

                    # cal_line = [ 1.09996 ]
            
                    try:
                            
                        for index_line , index_point in enumerate(list_pullback3): 
                                    # print ("index_line:" , index_line ) 
                                    index_point = float (index_point)
                                    # print("index_point:" , index_point) 

                                    if index_point in cal_line and index_line < len_pullback and index_line > 0:
                                            
                                            # print("111111111111111")
                                            # print("index_line:" , index_line)
                                            # print("index_point:" , index_point) 

                                            #  list_point.append(index_point_close)
                                            list_point_left_right.append(list_pullback3[index_line - 1])
                                            list_point_left_right.append(list_pullback3[index_line])
                                            list_point_left_right.append(list_pullback3[index_line + 1])
                                            # print("list_point_left_right:" , list_point_left_right)

                                    if list_point_left_right != [] and len(list_point_left_right) == 3:
                                #    if list_point_left_right != [] :         
                                            list_point_group.append([list_point_left_right , list_timpstamp_sec[index_line]])
                                            # print("list_point_group:" , list_point_group) 
                                            list_point_left_right = []
                         
                    except:
                         print("error list_pullback3[indexs + 1]")
                   
                                 
                    if list_point_group != []:
                                         
                        # print("list_point_group:" , list_point_group)  

                        for index_lines , list_group in enumerate(list_point_group):
                            for i_line , index_line_pullback in enumerate(cal_line):
                                if index_line_pullback in list_group[0]:
                                    point_close_3 = list_group[0][1]
                                    left_candel = list_group[0][0]
                                    right_candel = list_group[0][2]
                                    line_pullback = i_line + 1
                                    if point_close_3 > left_candel and point_close_3 > right_candel:
                                        list_line_pullback.append([line_pullback , list_group , "M"])
                                        #  line_pullback_input(line_pullback , point_close_3)
                                    elif point_close_3 < left_candel and point_close_3 < right_candel:
                                        list_line_pullback.append([line_pullback , list_group , "H"]) 

                    print("")
                    # list_line_pullback = [[1, [[1.0894, 1.08939, 1.08941], 1703176622] , 'H'] , [2, [[1.0894, 1.08939, 1.08941], 1703176626] ,'H'], 
                    #                       [1, [[1.0894, 1.08939, 1.08941], 1703176642] ,'H'] , [2, [[1.0894, 1.08939, 1.08941], 1703176626] ,'M']]
                                          
                    # list_line_pullback: [[1, [[1.09961, 1.09962, 1.09961], 1703176622], 'H']]
                    # print("list_line_pullback:" , list_line_pullback)

                    # list_line_pullback = [[1, 1.09882, 1703175070, 'H'] , [1, 1.09882, 1703175071, 'H']]
                    

                    def duplicate(items):
                                unique = []
                                for item in items:
                                    if item not in unique:
                                        unique.append(item)
                                return unique
                        
                    if list_line_pullback:

                        len_call_line = len(cal_line)
                        # print("len_call_line:" , len_call_line)
                        for index_num , i_count in enumerate(list_line_pullback):
                            for ix in range(len_call_line + 1):
                                if ix == i_count[0]:
                                     list_count_pullback_total.append([i_count[0] , i_count[2]])  

                        list_count_pulback = duplicate(list_count_pullback_total)
                  
                        for ii in list_count_pulback:
                            list_num_pullback.append(ii[0])

                        for ic in list_num_pullback:
                            
                            xxx = list_count_pullback_total.count([ic, 'M'])  
                            if xxx:
                                list_num_pullback_puyesh.append([ic , 'M' ,[xxx]])

                            xxxx = list_count_pullback_total.count([ic, 'H'])    
                            if xxxx:
                                list_num_pullback_puyesh.append([ic , 'H' ,[xxxx]])             


                        # print("")
                        # print("list_count_pullback_total:" , list_count_pullback_total)

                        print("")
                                  

                        for indexx , i_puyesh in enumerate(list_line_pullback):
                       
                            list_lines.append([i_puyesh[0] , i_puyesh[1][0][1] , i_puyesh[1][1] , i_puyesh[2]])
                            list_time_shakhes_line.append(i_puyesh[1][1])
                         
                        # list_model_pullback = duplicate(list_model_pullback)

                        min_time_shakhes = min(list_time_shakhes_line)


                        list_trade_shakhes_1 = []
                        list_trade_shakhes_2 = []

                        for i_trade_shahes_1 in list_lines:
                            if min_time_shakhes == i_trade_shahes_1[2]:
                                list_trade_shakhes_1.append(i_trade_shahes_1)

                        list_trade_shakhes_1 = duplicate(list_trade_shakhes_1)

                        status_rep = ''
                        if list_trade_shakhes_1:
                            for i_trade_shahes_2 in list_lines:
                                if list_trade_shakhes_1[0][3] == 'H':
                                    status_rep = 'M'
                                elif list_trade_shakhes_1[0][3] == 'M':
                                    status_rep = 'H'
                                for is1 in list_trade_shakhes_1 :   
                                    if is1[0] == i_trade_shahes_2[0] and i_trade_shahes_2[3] == status_rep :
                                        list_trade_shakhes_2.append(i_trade_shahes_2)


                        print("list_num_pullback_puyesh:" , list_num_pullback_puyesh)            
                        print("")  

                        print("list_lines:" , list_lines)
                        print("")        
                        
                        print("list_trade_shakhes_1:" , list_trade_shakhes_1)
                        print("list_trade_shakhes_2:" , list_trade_shakhes_2)
                        print("")
                    
                        print("")

                        # min_close_point = min(list_shakhes_pullback)
                        # print("min_close_point:" , min_close_point)


                        print("line_POS:" , line_POS)

                        print("Type_purchase:" , Type_purchase)
                                
                        list_num_pullback_pos = []
                        list_model_pullback_pos = []

                        point5 = 0
      
                        if line_POS:
                          
                            if line_POS[0] != 0:
                               
                                list_num_pullback_pos = line_POS  

                                if list_trade_shakhes_1:
                                    for ims1 in list_trade_shakhes_1:
                                        for ilp in line_POS:
                                            if ilp == ims1[0] and ims1[3] == 'H' and Type_purchase == 'H':
                                                pos_buy = True
                                                point5 = ims1[1]
                                            elif ilp == ims1[0] and ims1[3] == 'M' and Type_purchase == 'M':
                                                pos_sell = True   
                                                point5 = ims1[1]   

                                if list_trade_shakhes_2:
                                    for ims2 in list_trade_shakhes_2:
                                        for ilp in line_POS:
                                            if ilp == ims2[0] and ims2[3] == 'H' and Type_purchase == 'H':
                                                pos_buy = True
                                                point5 = ims2[1]
                                            elif ilp == ims2[0] and ims2[3] == 'M' and Type_purchase == 'M':
                                                pos_sell = True   
                                                point5 = ims2[1]


                            elif line_POS[0] == 0:   

                                if list_trade_shakhes_1:
                                    for ims1 in list_trade_shakhes_1:
                                        if ims1[3] == 'H' and Type_purchase == 'H':
                                            pos_buy = True
                                            point5 = ims1[1]
                                        elif ims1[3] == 'M' and Type_purchase == 'M':
                                            pos_sell = True   
                                            point5 = ims1[1]

                                if list_trade_shakhes_2:
                                    for ims2 in list_trade_shakhes_2:
                                        if ims2[3] == 'H' and Type_purchase == 'H':
                                            pos_buy = True
                                            point5 = ims2[1]
                                        elif ims2[3] == 'M' and Type_purchase == 'M':
                                            pos_sell = True  
                                            point5 = ims2[1]
                                
                                for i_line_pos in list_trade_shakhes_1: 
                                    list_num_pullback_pos.append(i_line_pos[0])
                                

                        print("pos_buy:" , pos_buy)
                        print("pos_sell:" , pos_sell)

                        list_num_pullback_pos = duplicate(list_num_pullback_pos)         
                        list_num_pullback_pos = json.dumps(list_num_pullback_pos)
                        print("list_num_pullback_pos:" , list_num_pullback_pos)


                        if chek == "false" and pos_buy == True and point5 > 0:
                            
                            time_command = pd.to_datetime(index_tick_time , unit='s')
                            shakhes = LINE.line_shakhes(patern_num , self.symbol_crypto , self.decimal_sambol , point5 , "buy")
                            status_trade = shakhes[1]
                            print("status_trade:" , status_trade)
                            shakhes = int (shakhes[0])

                            ticket = 0
                            execution = ''
                            recive_time_news = ''
                            status_News = 'false'
                            time_news = ''
                            status_manage_balance = "false"

                            recive_time_news = NEWS.cal_time(self.Time_news_effect)

                            manage_balance =  Manage_balance_trade.balance_candel( lot , 'buy' , self.symbol_crypto)       
                            print("manage_balance:" , manage_balance)

                            if status_trade == True:
                                point = mt5.symbol_info(self.symbol_crypto).point
                                tp = point5 + (shakhes * point)
                                tp = BUY_SELL.decimal(tp , self.decimal_sambol)
                                tp_total = float(tp) 

                                comment = f'{patern_num}' + "_" + f'{status_type}'+'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'+'N'
                               
                                if recive_time_news[0] == False and manage_balance == False:   
                                        status_News = 'false'  
                                        status_manage_balance = "false"  
                                        rec_pos = await BUY_SELL.pos_buy( tp_total , lot  , comment)   
                                        if rec_pos:
                                            execution = rec_pos.comment
                                            if execution == 'Request executed':
                                                ticket =  rec_pos.order                       
                                
                      
                            if recive_time_news[0] == True: 
                                status_News = 'true'   
                                time_news = recive_time_news[1]

                            if manage_balance == True:
                                status_manage_balance = 'true' 
                        
                            command = "(Patern:" + f'{patern_num})' + " _ " + "(position: BUY)" + " _ " + "(Line:" + f'{list_num_pullback_puyesh})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{3})'+ " _ " + "(Point5:" + f'{point5})' + " _ " + "(Time:" + f'{time_command})'  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'+ " _ " + "(status_News:" + f'{status_News})'+ " _ " + "(time_news:" + f'{time_news})' + " _ " + "(status_manage_balance:" + f'{status_manage_balance})' 
                            
                            status_chek = False
                            data_patern = Database.select_table_One(patern_num)
                            if data_patern: 
                                for index_patern , data_patern_num in enumerate(data_patern): 
                                        id = data_patern_num[0]
                                        Type_purchase = data_patern_num[31]
                                        if Type_purchase == 'H':
                                            await Database.update_table_chek(point5 , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)
                                            status_chek = True
                                if status_chek == False:
                                    for index_patern , data_patern_num in enumerate(data_patern): 
                                        id = data_patern_num[0]
                                        await Database.update_table_chek(point5 , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)


                        if chek == "false" and pos_sell == True and point5 > 0:
                            time_command = pd.to_datetime(index_tick_time , unit='s')
                            shakhes = LINE.line_shakhes(patern_num , self.symbol_crypto , self.decimal_sambol , point5 , "sell")
                            status_trade = shakhes[1]
                            print("status_trade:" , status_trade)
                            shakhes = int (shakhes[0])

                            ticket = 0
                            execution = ''
                            recive_time_news = ''
                            status_News = 'false'
                            time_news = ''
                            status_manage_balance = "false"

                            recive_time_news = NEWS.cal_time(self.Time_news_effect)

                            manage_balance =  Manage_balance_trade.balance_candel( lot , 'sell' , self.symbol_crypto)       
                            print("manage_balance:" , manage_balance)

                            if status_trade == True:
                                point = mt5.symbol_info(self.symbol_crypto).point
                                tp = point5 - (shakhes * point)
                                tp = BUY_SELL.decimal(tp , self.decimal_sambol)
                                tp_total = float(tp) 

                                comment = f'{patern_num}' + "_" + f'{status_type}'+'M' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'+'N'
                               
                                if recive_time_news[0] == False and manage_balance == False:   
                                        status_News = 'false'  
                                        status_manage_balance = "false"  
                                        rec_pos = await BUY_SELL.pos_sell( tp_total , lot  , comment)   
                                        if rec_pos:
                                            execution = rec_pos.comment
                                            if execution == 'Request executed':
                                                ticket =  rec_pos.order                       
                                
                      
                            if recive_time_news[0] == True: 
                                status_News = 'true'   
                                time_news = recive_time_news[1]

                            if manage_balance == True:
                                status_manage_balance = 'true' 
                        
                            command = "(Patern:" + f'{patern_num})' + " _ " + "(position: SELL)" + " _ " + "(Line:" + f'{list_num_pullback_puyesh})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{3})'+ " _ " + "(Point5:" + f'{point5})' + " _ " + "(Time:" + f'{time_command})'  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'+ " _ " + "(status_News:" + f'{status_News})'+ " _ " + "(time_news:" + f'{time_news})' + " _ " + "(status_manage_balance:" + f'{status_manage_balance})' 
                            
                            status_chek = False
                            data_patern = Database.select_table_One(patern_num)
                            if data_patern: 
                                for index_patern , data_patern_num in enumerate(data_patern): 
                                        id = data_patern_num[0]
                                        Type_purchase = data_patern_num[31]
                                        if Type_purchase == 'M':
                                           await Database.update_table_chek(point5 , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)
                                           status_chek = True
                                if status_chek == False:
                                    for index_patern , data_patern_num in enumerate(data_patern): 
                                        id = data_patern_num[0]
                                        await Database.update_table_chek(point5 , index_tick_time , command , "true" , ticket , list_num_pullback_pos , status_News , id)

                    if pos_buy == True or pos_sell == True:
                        break
                    
                    list_pullback3 = []
                    list_pullback3 = []
                    Type_purchase = []
                    list_lines = []
                    list_trade_shakhes_1 = []
                    list_trade_shakhes_2 = []
                    list_point_group = []
                    list_line_pullback = []
                    list_num_pullback_pos = []
                    list_num_pullback = []





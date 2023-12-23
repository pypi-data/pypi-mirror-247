import MetaTrader5 as mt5
import pandas as pd
import json


from database_ex_forex_next3 import Database
from decimal import Decimal
from line_ex_forex_next3 import LINE

class REP_POS:
   
   
   def __init__(self):
       fileObject = open("login.json", "r")
       jsonContent = fileObject.read()
       aList = json.loads(jsonContent)
       
       self.login = int (aList['login'])
       self.Server = aList['Server'] 
       self.Password = aList['Password'] 
       self.symbol_crypto = aList['symbol_crypto'] 
       self.decimal_sambol = int (aList['decimal_sambol'] )
       self.repetition_index = int (aList['repetition_index'] )

   def decimal(num , decimal_sambol):
        telo = '0.0'
        for i in range(decimal_sambol - 2):  
          telo = telo + "0"
        telo = telo + "1" 
        telo = float (telo)
        decimal_num = Decimal(str(num))
        rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
        return rounded_num  

   def repetition_pos(status_rep):
     
   #   print("status_rep:" , status_rep)
        
      if status_rep == "true":   

         data_all = Database.select_table_All()
         select_all_len = len(data_all)
         print("select_all_len:" , select_all_len)
 
         if select_all_len > 0:
               
             
               positions = mt5.positions_get(symbol = REP_POS().symbol_crypto)
             
               if positions == None:
                  print("No positions on EURUSD, error code={}".format(mt5.last_error()))
               elif len(positions) > 0:
                  print("Total positions on EURUSD =", len(positions))
                   
               len_positions = len(positions)
                 
             
               list_ticket_POS = []
            
               for position in positions:
                   
                   list_ticket_POS.append(position[0])
                   
               list_ticket_DB = []
               list_rep_patern = []
  
               for i in range(select_all_len):
                                    
                       data_one_DB = data_all[i]
                       repetition_candel = data_one_DB[24]
                       if repetition_candel:
                          list_rep_patern.append(repetition_candel)
  
  
               from collections import Counter
              #  print("list_rep_patern:" , list_rep_patern)
               freq_dict = Counter(list_rep_patern)
               sorted_freq = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
   
               # Print the sorted frequency
              #  print("sorted_freq:" , sorted_freq)
  
               list_rep_sorted = []
               for index_rep in sorted_freq:
                    # print("index_rep:" , index_rep)
                    if index_rep[1] >= REP_POS().repetition_index:
                         list_rep_sorted.append(index_rep[0])
                         
              #  print("list_rep_sorted:" , list_rep_sorted)
               for index , index_patern in enumerate(data_all): 
                                  
                #    print("index_patern:" , index_patern)
                   patern_num = index_patern[1]
                   status = index_patern[15]
                   chek = index_patern[16]
                   ticket = index_patern[21]
                   repetition_pos = index_patern[23]
                   repetion_patern_num = index_patern[24]
                   Trust_patern_full = index_patern[26]
                   Layout_patern = index_patern [27]

                   chek_ticket = None
                   
                   if ticket:
                       ticket = int(ticket)
                     #   list_ticket_DB.append(ticket)
        
                #    print("patern_num:" , patern_num)
                #    print("chek:" , chek)
                #    print("status:" , status)
                  #  print("ticket:" , ticket)
                  #  print("repetition_pos:" , repetition_pos)
                  #  print("list_ticket_POS:" , list_ticket_POS)



                   for ticket_pos in list_ticket_POS:
                        #   print("ticket_pos:" , ticket_pos)
   
                          ticket_pos = int (ticket_pos)
                          ticket = int (ticket)
                          
                          if ticket == ticket_pos:
                               chek_ticket = True

                   if chek_ticket == True:
                        chek_ticket = True
                
                   else:
                        chek_ticket = False   

                  #  print("chek:" , chek)
                  #  print("status:" , status)
                  #  print("ticket:" , ticket)
                  #  print("repetition_pos:" , repetition_pos)
                  #  print("Trust_patern:" , Trust_patern)
                  #  print("Layout_patern:" , Layout_patern)    
                  #  print("chek_ticket:" , chek_ticket)   

                   chek_rep = False
                  #  print("repetion_patern_num:" , repetion_patern_num) 
                   for index_search_rep in list_rep_sorted:
                        if repetion_patern_num == index_search_rep:
                           #   print("11111111111111333333333333")
                             chek_rep = True

                  #  print("chek_rep:" , chek_rep)          

                   if chek_ticket == False  and chek == "true" and status =="true" and repetition_pos == "false" and ticket != 0 and Trust_patern_full == "true" and Layout_patern == "true" and chek_rep == False:
                           print("11111111111111111111111111111111111111111111111111111")
                           patern_num_rep = index_patern[1]
                           type = index_patern[2]
                           point_patern = index_patern[3]
                           point_5 = index_patern[4]
                           point_5_time = index_patern[5]
                           command = index_patern[6]
                           candel_color = index_patern[7]
                           price_candel_open = index_patern[8]
                           price_candel_close = index_patern[9]
                           gap_point = index_patern[10]
                           gap_amount = index_patern[11]
                           gap_pip = index_patern[12]
                           gap_word = index_patern[13]
                           tension = index_patern[14]
                           status = index_patern[15]
                           chek = index_patern[16]
                           time_start_search = index_patern[17]
                           time_end_patern = index_patern[18]
                           timepstamp = index_patern[19] 
                           times = index_patern[20]
                           ticket = index_patern[21]
                           line_POS = index_patern[22]
                           repetition_pos = index_patern[23]
                           rep_patern_num = index_patern[24]
                           Trust_patern = index_patern[25]
                           Trust_patern_full = index_patern[26]
                           Layout_patern = index_patern [27]
                           Jump_patern = index_patern [28]
                           news = index_patern [29]
                           jump_1mine = index_patern [30]
                           Type_purchase = index_patern[31]
                           
                       
                        #    print("repetition_pos:" , repetition_pos)

                           rep_patern_num_algo = 0

                           if rep_patern_num:
                               rep_patern_num_algo = rep_patern_num
                            #    print("111111111111111")
        
                           else:
                               rep_patern_num_algo =  patern_num_rep 
                            #    print("222222222222222")

                           # print("ticket:" , ticket)
                          
                            
                           point_5_time = int(point_5_time)
                           timecandel = mt5.copy_rates_from_pos(REP_POS().symbol_crypto , mt5.TIMEFRAME_M1 , 0 , 1)
                           time_now = int( timecandel[0][0])
                               
                           def tp_max_buy():  
                              inputs_candels_tp_max = mt5.copy_rates_range(REP_POS().symbol_crypto, mt5.TIMEFRAME_M1, point_5_time, time_now)
                              list_max_candel = []
                              print("point_5_time:" , pd.to_datetime( point_5_time , unit='s') )
                              for i_max in inputs_candels_tp_max:
                                  list_max_candel.append(i_max[2])
                              # print("list_max_candel:" , list_max_candel)    
                              price_max = max(list_max_candel)
                              price_max = REP_POS.decimal(price_max , REP_POS().decimal_sambol)
                              price_max = float(price_max)
                              list_max_candel = []
                              return price_max
          
                           def tp_min_sell():
                              inputs_candels_tp_min = mt5.copy_rates_range(REP_POS().symbol_crypto, mt5.TIMEFRAME_M1, point_5_time, time_now)
                                        # print("inputs_candels_tp_min:", inputs_candels_tp_min)
                              list_min_candel = []
                              print("point_5_time:" , pd.to_datetime( point_5_time , unit='s') )
                              for i_min in inputs_candels_tp_min:
                                 list_min_candel.append(i_min[3])
                                        # print("list_min_candel:" , list_min_candel)
                              price_min = min(list_min_candel)
                              price_min = REP_POS.decimal(price_min , REP_POS().decimal_sambol)
                              price_min = float(price_min)
                              list_min_candel = []
                              return price_min
                           

                           ticket = int(ticket)

                           status_old_tp = False

                           if ticket == 123456789 and point_5:
                              print("1111111111111111111111111111111")  
                              x = 1
                              for i in range(REP_POS().decimal_sambol):
                                 x = x * 10

                              point5 = float(point_5)   

                              point_close = json.loads(price_candel_close)
                              timepstamp = json.loads(timepstamp)
                              timepstamp_3 = int (timepstamp[3]) + 840
                              price_close_3 = float(point_close[3])    
   

                              line_point = LINE.cal_point_line(patern_num , timepstamp_3)
                              line_point = float(line_point)
                              amount_shakhes = abs (price_close_3 - line_point)
                              amount_shakhes = amount_shakhes * x
                              amount_shakhes = int(amount_shakhes)
   
                              point = mt5.symbol_info(REP_POS().symbol_crypto).point
                              point_shakhes = amount_shakhes * point  
                              
                              

                              if Type_purchase == 'H':
                                 tp_buy = (point5 + point_shakhes) 
                                 tp_buy = LINE.decimal(tp_buy , LINE().decimal_sambol)
                                 tp_buy = float(tp_buy)

                                 tp_max_buy_rec = tp_max_buy()
                                 print("tp_max_buy_rec:" , tp_max_buy_rec)
                                 if tp_max_buy_rec > tp_buy:
                                    status_old_tp = True
                                    print("111111111")

                              elif Type_purchase == 'M':
                                 tp_sell = (point5 - point_shakhes) 
                                 tp_sell = LINE.decimal(tp_sell , LINE().decimal_sambol)
                                 tp_sell = float(tp_sell)

                                 tp_min_sell_rec = tp_min_sell()
                                 print("tp_min_sell_rec:" , tp_min_sell_rec)
                                 if tp_min_sell_rec < tp_sell: 
                                    status_old_tp = True
                                    print("222222222")
                                   
                              point_close = json.dumps(price_candel_close)
                              timepstamp = json.dumps(timepstamp)

                           print("status_old_tp:" , status_old_tp)
                           print("rep_patern_num_algo:" , rep_patern_num_algo)

                           status_patern_pos = True

                           positions = mt5.positions_get(symbol = REP_POS().symbol_crypto)
                           if positions:
                               for position in positions:
                                   command = position.comment
                                   if command:
                                       patern_num_pos = command.split('_')
                                       status_command = patern_num_pos[0].isnumeric()
                                       if status_command == True:
                                           patern_num_pos = int (patern_num_pos[0])
                                           patern_num_rep = int(patern_num_rep)
                                           if patern_num_pos == patern_num_rep:
                                               status_patern_pos = False
                                               
                           print("status_patern_pos:" , status_patern_pos)                    

                           if status_old_tp == True or ticket != 123456789 and status_patern_pos == True :
                                 data_all = Database.select_table_All()
                                 select_all_len = len(data_all)
                                 # print("select_all_len:" , select_all_len)
                                 rec = data_all[select_all_len - 1]
                                 # print("select_all:" , rec)
                                 patern_num = int (rec[1])
                                 # print("rec:" , rec)
                                 patern_num = patern_num + 1
                                 # print("patern_num:" , patern_num)
                                 Database.update_table_repetition_pos("true" , patern_num_rep ) 

                                 value = (patern_num , type , point_patern , "" , "" , ""  , candel_color , price_candel_open , price_candel_close , gap_point , gap_amount , gap_pip ,gap_word , tension, status , "false" , time_start_search , time_end_patern , timepstamp , times , 0 , line_POS , "false" , rep_patern_num_algo , Trust_patern , Trust_patern_full , Layout_patern , Jump_patern , news , jump_1mine , "H")
                                 Database.insert_table(value)

                                 value = (patern_num , type , point_patern , "" , "" , ""  , candel_color , price_candel_open , price_candel_close , gap_point , gap_amount , gap_pip ,gap_word , tension, status , "false" , time_start_search , time_end_patern , timepstamp , times , 0 , line_POS , "false" , rep_patern_num_algo , Trust_patern , Trust_patern_full , Layout_patern , Jump_patern , news , jump_1mine , "M")
                                 Database.insert_table(value)
                                 
      
                                 break
 
      elif status_rep == "false":
          
          print("status_rep: False")
   
from itertools import groupby
import datetime
import ipaddress

def TO_check(group,key,N):
    TO_clock = 0 #故障した時間
    Recov_clock = 0 #復旧した時間
    TO_time = 0 #故障期間
    TO_state = False #タイムアウトしているか
    TO_counter = 0 #連続TO数
    for member in group:
        if TO_state == False:
            if member[2]=='-': #タイムアウトしていない状態で応答が無い場合
                TO_state = True
                TO_counter = 1
                #yymmddhhmmssを年-月-日時:分:秒に変換
                TO_clock = datetime.datetime.strptime(member[0],'%Y%m%d%H%M%S')
        else:
            if member[2]!='-': #タイムアウトしている状態で応答が来た場合
                TO_state = False
                if TO_counter >= N: # N回以上連続でタイムアウトした場合
                    #yymmddhhmmssを年-月-日時:分:秒に変換
                    Recov_clock = datetime.datetime.strptime(member[0],'%Y%m%d%H%M%S')
                    TO_time = Recov_clock - TO_clock
                    #アドレスと故障期間を表示
                    print('address:'+key,' failure period:',TO_time)
                TO_clock = 0

            else:#連続でタイムアウトした場合
                TO_counter += 1
    if TO_state == True: #タイムアウト状態の場合
        if TO_counter >= N: # N回以上連続でタイムアウトした場合
            #アドレスと故障中と出力
            print('address:'+key,' In failure')  
        

def TO_check_sub(group,key,N):
    host_count = 0
    host_num = {}
    group_sorted = sorted(group,key=lambda elem:elem[1])
    for key2, group2 in groupby(group_sorted, key=lambda m: m[1]):
        host_num[key2] = host_count
        host_count += 1
    TO_clock = 0 #サブネットが故障した時間
    Recov_clock = 0 #サブネットが復旧した時間
    TO_time = 0 #サブネットの故障期間
    TO_state = [False] * host_count #ホストごとにタイムアウトしているか
    TO_counter = [0] * host_count #ホストごとの連続TO数
    group_sorted = sorted(group_sorted,key=lambda elem:elem[0])
    for member in group_sorted:
        if  all(TO_state)== True:
            if member[2]!='-': #サブネットがタイムアウトしている状態で応答が来た場合
               TO_state[host_num[member[1]]] = False
               Recov_clock = datetime.datetime.strptime(member[0],'%Y%m%d%H%M%S')
               TO_time = Recov_clock - TO_clock
               print('subnet address:'+str(member[3]),' failure period:',TO_time)
               TO_clock = 0
               TO_counter[host_num[member[1]]] = 0

        else:
            if member[2]!='-': #サブネットがタイムアウトしていない状態で応答が来た場合
                TO_state[host_num[member[1]]] = False
                TO_counter[host_num[member[1]]] = 0
            else: #サブネットがタイムアウトしていない状態で応答が来ない場合
                TO_counter[host_num[member[1]]] += 1
                if TO_counter[host_num[member[1]]] >= N:
                    TO_state[host_num[member[1]]] = True
                    if  all(TO_state) == True: #サブネット内の全てのホストが故障している場合
                        TO_clock = datetime.datetime.strptime(member[0],'%Y%m%d%H%M%S')
    if all(TO_state)== True: #サブネットが故障中の場合
        print('subnet address:'+str(member[3]),' failure period:',TO_time)

#連続タイムアウト数
N = 2
#ログファイルの読み込み(文字列)
with open('log4.txt','r') as f:
    content = f.read()    
#行ごとに分割
contents = content.split("\n")
elements = [] 
#入力を要素ごとに分割したタプルをリストelementsに格納する
for cont in contents:
    #要素ごとに分割
    element = cont.split(',')
    #ネットワークアドレスを取得
    address = ipaddress.ip_network(element[1],strict=False)
    tupple = (element[0],element[1],element[2],address)
    elements.append(tupple)
    #elements[n] = (確認日時,サーバアドレス,応答結果,サーバのネットワークアドレス)
#リストをネットワークアドレスでソート
elements_sorted = sorted(elements,key=lambda elem:elem[3])
#リストをネットワークアドレスでグループ分けしてグループごとに処理を行う
for key, group in groupby(elements_sorted, key=lambda m: m[3]):
    TO_check_sub(group,key,N)
elements_sorted = sorted(elements,key=lambda elem:elem[1])
for key, group in groupby(elements_sorted, key=lambda m: m[1]):
    TO_check(group,key,N)
    
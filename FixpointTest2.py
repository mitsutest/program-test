from itertools import groupby
import datetime
#連続タイムアウト数
N = 2
#ログファイルの読み込み(文字列)
with open('log2.txt','r') as f:
    content = f.read()    
#行ごとに分割
contents = content.split("\n")
elements = [] 
#入力を要素ごとに分割したタプルをリストelementsに格納する
for cont in contents:
    #要素ごとに分割
    element = cont.split(',')
    tupple = (element[0],element[1],element[2])
    elements.append(tupple)
    #elements[n] = (確認日時,アドレス,応答結果)
#リストをアドレスでソート
elements_sorted = sorted(elements,key=lambda elem:elem[1])
#リストをアドレスでグループ分けしてグループごとに処理を行う
for key, group in groupby(elements_sorted, key=lambda m: m[1]):
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
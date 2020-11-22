from itertools import groupby
import datetime

#平均応答時間を計算する関数
def delay_ave(c,m):
    sum = 0
    num = 0
    if len(c) > m:
        for i in range(1,m+1):
            if c[-i] != '-':
                sum += int(c[-i])
                num += 1
    else:
        for i in range(1,len(c)+1):
            if c[-i] != '-':
                sum += int(c[-i])
                num += 1
    if num == 0:
        num = 1
    ave = sum / num
    return ave

def delay_check(group,m,t,key):
    OL_clock = 0 #過負荷になった時間
    Recov_clock = 0 #過負荷から復旧した時間
    OL_time = 0 #過負荷期間
    ave_res = 0 #平均応答時間
    OL_state = False #過負荷しているか
    check = []
    for member in group:
        check.append(member[2])
        ave_res = delay_ave(check,m)
        if OL_state == False:
            if ave_res > t: #過負荷していない状態で過負荷となった場合
                OL_state = True
                #yymmddhhmmssを年-月-日時:分:秒に変換
                OL_clock = datetime.datetime.strptime(member[0],'%Y%m%d%H%M%S')
        else:
            if ave_res <= t: #過負荷している状態で過負荷から復旧した場合
                OL_state = False
                #yymmddhhmmssを年-月-日時:分:秒に変換
                Recov_clock = datetime.datetime.strptime(member[0],'%Y%m%d%H%M%S')
                OL_time = Recov_clock - OL_clock
                #アドレスと故障期間を表示
                print('address:'+key,' overload period:',OL_time)
    if OL_state == True: #過負荷状態の場合
        #アドレスと故障中と出力
        print('address:'+key,' overload')   

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

N = 2 #連続タイムアウト数
m = 3 #参照応答回数
t = 100 #過負荷の閾値
#ログファイルの読み込み(文字列)
with open('log3.txt','r') as f:
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
    TO_check(group,key,N)
for key, group in groupby(elements_sorted, key=lambda m: m[1]):
    delay_check(group,m,t,key)
    
    
 
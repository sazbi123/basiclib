import matplotlib.pyplot as plt

def get_data_with_offset(data_list:list,offset:int,size:int)->list:
    # バイトごとに分けられたデータに対してオフセットと取得するデータを指定して返す関数
    return data_list[offset:offset+size]

def get_bits_num(bits:list,little_or_big:int)->int:
    # バイトごとに分けられたデータの値を求め返す関数
    # リトルエンディアンかビッグエンディアンかを第2引数で指定する必要あり
    # little_or_big: 0: little, 1: big
    return_num=0

    if little_or_big==0:
        # little endian
        for i in range(len(bits)):
            # print(bits[i])
            return_num+=bits[i]<<i*8
        
        # print(return_num)
        # print()
        return return_num
    elif little_or_big==1:
        # big endian
        for i in range(len(bits)):
            # print(bits[len(bits)-i-1])
            return_num+=bits[len(bits)-i-1]<<i*8
        
        # print(return_num)
        # print()
        return return_num
    else:
        print("第2引数は0または1です")
        exit()

def byte_num_and_prefix(byte_num:int,SI_or_IEC:int):
    # 単位がバイトのものを適切な接頭語と値に返る関数
    # SI接頭語（キロとか）かIEC（キビとか）を指定する必要がある
    # SI_or_IEC: 0:SI, 1:IEC
    return_byte_num=byte_num
    prefix_SI=["","K","M","G","T"]
    prefix_IEC=["","Ki","Mi","Gi","Ti"]
    prefix_count=0
    if SI_or_IEC==0:
        while True:
            if return_byte_num//1000!=0:
                return_byte_num/=1000
                prefix_count+=1
            else:
                break
        
        try:
            return [return_byte_num,prefix_SI[prefix_count]]
        except IndexError:
            return [return_byte_num,f"10^{prefix_count*3}"]
    elif SI_or_IEC==1:
        while True:
            if return_byte_num//1024!=0:
                return_byte_num/=1024
                prefix_count+=1
            else:
                break
        
        try:
            return [return_byte_num,prefix_IEC[prefix_count]]
        except IndexError:
            return [return_byte_num,f"2^{10*prefix_count}"]
        
def charcode_to_str(char_code:list,little_or_big:int)->str:
    # 文字コードデータリストから文字列を生成する
    # リトルエンディアンかビッグエンディアンかを第2引数で指定する必要あり
    # エンディアンというよりは逆順にするかどうか見たいなこと
    # little_or_big: 0: little, 1: big
    return_str=""

    if little_or_big==0:
        # little endian
        for i in range(len(char_code)):
            return_str+=chr(char_code[len(char_code)-i-1])
    elif little_or_big==1:
        # big endian
        for i in range(len(char_code)):
            return_str+=chr(char_code[i])
    
    return return_str

def EscapeSequence():
    # Pythonのprint()でのエスケープシーケンスを確認する関数
    for i in range(10):
        for j in range(10):
            v = i * 10 + j
            print("\033[{}m{}\033[0m ".format(str(v), str(v).zfill(3)), end="")
        print()

def TextRawDataList2TextFile(filename:str,data:list):
    # エクスポートしたrawデータの形式でファイルに書き込む関数
    # リストの要素はタブ文字で区切られる必要がある
    with open(f"{filename}.txt","w",encoding="utf8") as f1:
        for i in data:
            f1.write(f"{i}\n")

def GetColumn(data:list,index:int,sep:str)->list:
    # 指定した区切り文字で区切り，指定した列のインデックス番号を返す関数
    # 改行文字は無視
    return_data=[]

    for i in data:
        return_data.append(i.replace("\n","").split(sep)[index])
    
    return return_data

def ElementStr2Float(data:list)->list:
    return [float(i) for i in data]

def TextRawDataSaveImg(file_name:str,text_raw_data:list,save_index:list):
    # TextRawDataViewImgを使っているときはこれを使わない
    # グラフを画像データで保存する関数
    # file_nameは拡張子を省略しない
    # text_raw_dataは前処理必要ない
    # 区切り文字がタブ文字前提になっている
    column_num=len(text_raw_data[0].split("\t"))
    x=ElementStr2Float(GetColumn(text_raw_data,0,"\t")[1:])

    for i in range(column_num-1):
        if len(save_index)==0:
            y=ElementStr2Float(GetColumn(text_raw_data,i+1,"\t")[1:])
            plt.plot(x, y)
        elif i+1 in save_index:
            y=ElementStr2Float(GetColumn(text_raw_data,i+1,"\t")[1:])
            plt.plot(x, y)
    
    plt.grid()
    plt.savefig(file_name)

def TextRawDataViewImg(text_raw_data:list,save_index:list):
    # TextRawDataSaveImgを使っているときはこれを使わない
    # グラフをウィンドウに描画する関数
    # file_nameは拡張子を省略しない
    # text_raw_dataは前処理必要ない
    # 区切り文字がタブ文字前提になっている
    column_num=len(text_raw_data[0].split("\t"))
    x=ElementStr2Float(GetColumn(text_raw_data,0,"\t")[1:])

    if len(save_index)==0:
        for i in range(column_num-1):
            y=ElementStr2Float(GetColumn(text_raw_data,i+1,"\t")[1:])
            plt.plot(x,y)
        
        plt.legend(text_raw_data[0].replace("\n","").split("\t")[1:])
    else:
        for i in range(len(save_index)):
            for j in range(column_num-1):
                if save_index[i]==GetColumn(text_raw_data,j+1,"\t")[0]:
                    y=ElementStr2Float(GetColumn(text_raw_data,j+1,"\t")[1:])
                    plt.plot(x,y)
        
        plt.legend(save_index)
    
    plt.grid()
    plt.show()

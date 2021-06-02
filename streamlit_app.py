import csv
import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import plotly_express as px
import base64
import datetime
#import time

#from module3 import excute

st.title("超温保护数据解析程序")


#上传文件
uploaded_file=st.file_uploader("Choose a txt file",type="txt")

if(st.button('点击开始上传')):
    if uploaded_file is not None:
        name=["date","temp1","temp2","Other"]
        data=pd.read_csv(uploaded_file,sep=' ',names=name,encoding='gb18030')#,,encoding='gb18030',names=name,
    
        data.to_csv('sourcedata.txt',index=False,encoding='gb18030') #sep='',

        st.success('上传完成.')
    else:
        st.error('未选择文件!')


#st.date_input - 显示日期输入框
d1 = st.date_input(
    "Select begin date:",
    datetime.date(2020, 7, 1))

date_begin=d1.__str__()[2:4]+d1.__str__()[5:7]+d1.__str__()[8:10]
st.write('Your selection is:', d1)



d2 = st.date_input(
    "Select end date:",
    datetime.date(2020, 7, 6))
date_end=d2.__str__()[2:4]+d2.__str__()[5:7]+d2.__str__()[8:10]
st.write('Your selection is:', d2)



#@st.cache
#打开文件
def my_func(fin,fout,date_begin,date_end):
    fp=open(fout,"w",newline='')
    #fp.write("这是个测试！")
    f_csv = csv.writer(fp)
    headers = ['Date','Tmp1','Tmp2']
    f_csv.writerow(headers)
    
    #ymdStart="200120"
    #ymdEnd="211020"
    ymdStart=date_begin
    ymdEnd=date_end
    
    maxTemp1=-50
    maxTemp2=-50

    with open(fin, 'r',encoding='gb18030') as f:#utf-8,gb18030
        for line in f.readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            #print(line)
            if("T" in line or "∞" in line):#如果包含T则跳过，∞鈭灺癈
                continue
            if (line[0:6]>=ymdStart and line[0:6] <= ymdEnd):
                #print('Y')
                #st.write(line)
                idC1=line.find("C")#第一次出现的位置
                #line.partition("C")
                idC2=line.rfind("C");#最后一次出现的位置
                id_1=line.find(",");
                id_2=line.rfind(",");
                date=line[0:12]#
                date='20'+(date)
                #转换成日期格式
                #date=pd.to_datetime(date)
                Temp1=line[13:idC1-id_1-3+13+1]
                Temp2=line[idC1+2:idC2-idC1-3+idC1+1+1]
                
                #st.write('temp:',Temp1,Temp2)

                if(int(Temp1) >= int(maxTemp1)):
                    maxTemp1=Temp1#T1最高温度
                    mxdate1=date#最高温度时间
                    #print(maxTemp1,mxdate1)
                if(int(Temp2) >= int(maxTemp2)):
                    maxTemp2=Temp2#T1最高温度
                    mxdate2=date#最高温度时间
                    #print(maxTemp2,mxdate2)

                rows = [[date,Temp1,Temp2]]
                f_csv.writerows(rows)

    
    f.close()
    fp.close()
    print("Result")
    print(maxTemp1,mxdate1)
    print(maxTemp2,mxdate2)
    #st.write("Max1:",maxTemp1,mxdate1)
    #st.write("Max2:",maxTemp2,mxdate2)

    return (maxTemp1,mxdate1,maxTemp2,mxdate2)


#文件目录输入
filepath_in=st.text_input("Enter the txt file path:")
st.write('The entered path is:',filepath_in)
fin='C:/Users/Administrator/source/repos/WebProject1/WebProject1/20.08.06.10.18.50 Temp1 3车1位.txt'
fin=filepath_in

filepath_out=st.text_input("Enter the output file path:")
st.write('The entered path is:',filepath_out)
fo='C:/Users/Administrator/source/repos/WebProject1/WebProject1/output.csv'
fo=filepath_out

@st.cache
#文件下载
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">点击下载 {file_label}</a>'
    return href


#点击按钮开始执行
if(st.button("点击开始执行")):
    
    #st.info("Program start")
    if(fin!='' and fo!=''):
        #添加占位符
        my_placeholder = st.empty()
        # Now replace the placeholder with some text:
        my_placeholder.text("Program start.")
        
        (maxTemp1,mxdate1,maxTemp2,mxdate2)=my_func(fin,fo,date_begin,date_end)
        #st.success("Program end")
        my_placeholder.text("Program end.")
        st.write("Max temp1:",maxTemp1,",",mxdate1)
        st.write("Max temp2:",maxTemp2,",",mxdate2)

        #st.balloons - 显示庆祝气球
        st.balloons()

        file_path =filepath_out
        file_label = '结果文件'
        st.markdown(get_binary_file_downloader_html(file_path, file_label),
                unsafe_allow_html=True)
        #st.balloons - 显示庆祝气球
        st.balloons()
    else:
        st.error("目录不能为空!")



#
def getTemp(arrLike,input):
    output=arrLike[input]

    set_start=200622090900
    set_end=200724090900
    temp_high1=-50
    temp_high2=-50

    csv_date=arrLike['date']
    csv_temp1=arrLike['temp1']
    csv_temp2=arrLike['temp2']

    if set_start<(csv_date) and set_end>(csv_date):#日期在范围内

            data_temp1=csv_temp1.rstrip("°C")
            data_temp2=csv_temp2.rstrip("°C")
            #temp_str=data_temp1+data_temp2
            if("T" not in data_temp1 and "∞" not in data_temp1):#如果不包含T ∞
                if("T" not in data_temp2 and "∞" not in data_temp2):
                    
                    st.write('---out---',csv_date, data_temp1, data_temp2)
                    return [csv_date,int(data_temp1),int(data_temp2)]


    




if(st.button("点击开始解析")):
    (maxTemp1,maxdate1,maxTemp2,maxdate2)=my_func('sourcedata.txt','resultdata.csv',date_begin,date_end)
    st.write(maxTemp1,maxdate1,maxTemp2,maxdate2)
    #st.balloons - 显示庆祝气球
    st.balloons()


if(st.button("点击显示下载链接")):
    file_path ='resultdata.csv'
    file_label = '结果文件'
    st.markdown(get_binary_file_downloader_html(file_path, file_label),
            unsafe_allow_html=True)
    

if(st.button("点击开始绘图")):
    result=pd.read_csv('resultdata.csv',sep=',',encoding='gb18030')
    #st.write(result)
    #st.line_chart(result[['Tmp1','Tmp2']])

    
    #base=datetime.datetime(2020,7,1)
    #dates=[base+datetime.timedelta(seconds=(10*i))for i in range(64069)]
    ##st.write(dates)
    #plt.plot(dates)
    #st.pyplot()
    #方法1：先创建窗口，再创建子图
    fig=plt.figure()
    lims=[np.datetime64('2020-07-01'),np.datetime64('2020-07-06')]
    axes1=fig.add_subplot(2,1,1)
    axes2=fig.add_subplot(2,1,2)
    axes1.plot(result['Date'],result['Tmp1'],c='c')
    axes2.plot(result['Date'],result['Tmp2'])
    #axes2.set_xlim(lims)
    #rotate labels
    for label in axes2.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    #st.pyplot(fig)

    #方法2：一次性创建窗口和多个子图
    fig, axarr = plt.subplots()#打开新窗口，并创建子图
    ax1=axarr#通过子图数组获取一个子图
    ax1.plot(result[['Tmp1','Tmp2']])
    ax1.set_title("Temprature")
    ax1.set_xlabel("N")
    ax1.set_ylabel("T")
    st.pyplot(fig)




if(st.button("Test")):
    fig, ax1 = plt.subplots()
    ax1.scatter([1, 2, 3], [1, 2, 3])
    st.pyplot(fig)

    set_start=200622090900
    set_end=200724090900
    temp_high1=-50
    temp_high2=-50

    #rr=data.apply(getTemp,axis=1,input=('date'))
    st.write('write :',rr)
    rr.to_csv('result.csv',sep=',',index=False) 
    #创建一个空的DataFrame
    result=pd.DataFrame(columns=('date','t1','t2'))

    #st.write("行名",data.index)
    #st.write("列名",data.columns)
    for indexs in data.index:
        #st.write(data.loc[indexs])#写一行
       
        data_date=data.at[indexs,'date']
        if set_start<(data_date) and set_end>(data_date):#日期在范围内

            data_temp1=data.at[indexs,"Temp1"].rstrip("°C")
            

            data_temp2=data.at[indexs,"Temp2"].rstrip("°C")
            #temp_str=data_temp1+data_temp2
            if("T" in data_temp1 or "∞" in data_temp1):#如果包含T ∞则跳过
                if("T" in data_temp2 or "∞" in data_temp2):
                    continue
            #st.write(data_date,int(data_temp1),int(data_temp2))   #xieru

            #st.write(int(data_temp1))
            #将结果逐行插入result
            dat={
                'date':[int(data_date)],
                't1':[int(data_temp1)],
                't2':[int(data_temp2)]}
            result=result.append(pd.DataFrame(dat),ignore_index=True)

            #查找最大值
            if int(data_temp1) > int(temp_high1):
                date_Max1=data_date
                temp_high1=data_temp1
            if int(data_temp2) > int(temp_high2):
                date_Max2=data_date
                temp_high2=data_temp2

    st.write("---output max---")
    st.write(date_Max1,int(temp_high1))
    st.write(date_Max2,int(temp_high2))
    #st.write(result)
    
    
    #将创建的数据写成csv文件中
    st.line_chart(result[['t1','t2']])
    result.to_csv('result.csv',sep=',',index=False) 
    

    chart_data=pd.DataFrame(np.random.randn(20,1),columns=['A'])
    st.write(chart_data)
    st.line_chart(chart_data)


    #st.write(data.loc[indexs].values[2:3])#values[0:1]
    
    with open(uploaded_file.__str__(), 'r',encoding='gb18030') as f:
        for line in uploaded_file.readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            print(line)

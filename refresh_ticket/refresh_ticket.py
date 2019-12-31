# -*- coding:utf-8 -*-
import threading
import requests
import time
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *


class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('12306查票系统')
        self.master.geometry('795x351')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()
        self.bum = self.winfo_toplevel()
        frame = Frame()

        frame.place(x=20, y=60, width=750, height=259)
        self.style = Style()

        self.style.configure('Label1.TLabel', anchor='w', font=('宋体', 9, 'bold'))
        self.Label1 = Label(self.top, text='出发地:', style='Label1.TLabel')
        self.Label1.place(relx=0.03, rely=0.068, relwidth=0.072, relheight=0.048)

        self.Text1Var = StringVar(value='')
        self.Text1 = Entry(self.top, textvariable=self.Text1Var, font=('宋体', 9))
        self.Text1.place(relx=0.091, rely=0.046, relwidth=0.142, relheight=0.094)

        self.style.configure('Label1.TLabel', anchor='w', font=('宋体', 9, 'bold'))
        self.Label1 = Label(self.top, text='目的地:', style='Label1.TLabel')
        self.Label1.place(relx=0.262, rely=0.068, relwidth=0.072, relheight=0.048)

        self.Text2Var = StringVar(value='')
        self.Text2 = Entry(self.top, textvariable=self.Text2Var, font=('宋体', 9))
        self.Text2.place(relx=0.322, rely=0.046, relwidth=0.142, relheight=0.094)

        self.style.configure('Command1.TButton', font=('宋体', 9, 'bold'))
        self.Command1 = Button(self.top, text='查      询', command=self.Command2, style='Command1.TButton')
        self.Command1.place(relx=0.785, rely=0.046, relwidth=0.172, relheight=0.094)

        self.style.configure('Label1.TLabel', anchor='w', font=('宋体', 9, 'bold'))
        self.Label2 = Label(self.top, text='出发日期：', style='Label2.TLabel')
        self.Label2.place(relx=0.493, rely=0.058, relwidth=0.092, relheight=0.048)
        self.number = StringVar()
        numberChosen = Combobox(self.top, textvariable=self.number)
        numberChosen.place(relx=0.574, rely=0.049, relwidth=0.142, relheight=0.074)
        numberChosen['values'] = (1, 2, 4, 42, 100)  # 设置下拉列表的值
        values = []
        y = int(time.strftime("%Y", time.localtime()))
        m = int(time.strftime("%m", time.localtime()))
        d = int(time.strftime("%d", time.localtime()))
        i = 0
        yy = y
        mm = m
        dd = d
        while i < 30:  # 30天数据
            if m in (1, 3, 5, 7, 8, 10, 12):
                if d + i > 31:
                    dd = d + i - 31
                    mm = m + 1
                    if mm > 12:
                        yy = y + 1
                        mm = mm - 12
                else:
                    dd = d + i
            elif m in (4, 6, 9, 11):
                if d + i > 30:
                    dd = d + i - 30
                    mm = m + 1
                    if mm > 12:
                        yy = y + 1
                        mm = mm - 12
                else:
                    dd = d + i
            else:
                if (m % 400 == 0) or ((m % 4 == 0) and (m % 100 != 0)):
                    if d + i > 29:
                        dd = d + i - 29
                        mm = m + 1
                        if mm > 12:
                            yy = y + 1
                            mm = mm - 12
                    else:
                        dd = d + i
                else:
                    if d + i > 28:
                        dd = d + i - 28
                        mm = m + 1
                        if mm > 12:
                            yy = y + 1
                            mm = mm - 12
                    else:
                        dd = d + i
            s = '%d-%02d-%02d' % (yy, mm, dd)
            values.append(s)
            i += 1
        numberChosen['values'] = tuple(values)
        numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        scrollBar = Scrollbar(frame)
        scrollBar.pack(side=RIGHT, fill=Y)
        self.tree = Treeview(frame, height=259,
                             columns=("车次", "出发站名", "到达站名", "出发时间", "到达时间", "一等座", "二等座", "硬卧", "软卧", "硬座", "无座"),
                             show="headings", yscrollcommand=scrollBar.set)
        scrollBar.configure(command=self.tree.yview)
        self.tree.column('车次', width=50, anchor='center')
        self.tree.column('出发站名', width=80, anchor='center')
        self.tree.column('到达站名', width=80, anchor='center')
        self.tree.column('出发时间', width=80, anchor='center')
        self.tree.column('到达时间', width=80, anchor='center')
        self.tree.column('一等座', width=60, anchor='center')
        self.tree.column('二等座', width=60, anchor='center')
        self.tree.column('硬卧', width=60, anchor='center')
        self.tree.column('软卧', width=60, anchor='center')
        self.tree.column('硬座', width=60, anchor='center')
        self.tree.column('无座', width=60, anchor='center')
        self.tree.heading('车次', text='车次')
        self.tree.heading('出发站名', text='出发站名')
        self.tree.heading('到达站名', text='到达站名')
        self.tree.heading('出发时间', text='出发时间')
        self.tree.heading('到达时间', text='到达时间')
        self.tree.heading('一等座', text='一等座')
        self.tree.heading('二等座', text='二等座')
        self.tree.heading('硬卧', text='硬卧')
        self.tree.heading('软卧', text='软卧')
        self.tree.heading('硬座', text='硬座')
        self.tree.heading('无座', text='无座')
        self.tree.pack()


class Application(Application_ui):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
        # 获取各个城市的编号
        city_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9077"
        rep = requests.get(city_url, headers=header)
        self.areatocode = {}
        # 把内容以{城市名:对应的编号}存入字典
        for i in rep.content.decode().split("@")[1:]:
            if i:
                tmp = i.split("|")
                self.areatocode[tmp[1]] = tmp[2]

    def Command2(self):
        """点击查询按钮触发的逻辑"""
        start1 = self.Text1.get()
        to1 = self.Text2.get()
        date = self.number.get()
        # 这里日期判断不够严格   自己可以附加
        now_data = time.strftime('%Y.%m.%d', time.localtime(time.time()))
        if not start1:
            showerror(title='警告', message='出发地不能为空')
        elif start1 not in self.areatocode:
            showerror(title='警告', message='输入错误,没有找到该城市')
        elif not to1:
            showerror(title='警告', message='目的地不能为空')
        elif to1 not in self.areatocode:
            showerror(title='警告', message='输入错误,没有找到该城市')
        elif not date:
            showerror(title='警告', message='输入错误,没有找到该日期')
        elif int(date.replace('-', '')) < int(now_data.replace('.', '')):
            showerror(title='警告', message='日期不能小于当期日期')
        elif start1 and to1 and date:
            if self.Command1['text'] == '查      询':
                self.Command1['text'] = '正 在 查 询'
            # 每次点击查询按钮后将按钮设置为不可用  防止多次发送请求
            self.Command1.config(state=DISABLED)
            # 启动一个线程防止程序在查询期间被卡主  出现未响应的情况
            t = threading.Thread(target=self.Command1_Cmd, args=(start1, to1, date))
            t.start()

    def Command1_Cmd(self, start1, to1, date):
        try:
            start = self.areatocode[start1]
            to = self.areatocode[to1]
            # 这里有学生和成人之分   默认直接写成成人了
            student = "ADULT"
            url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + start + "&leftTicketDTO.to_station=" + to + "&purpose_codes=" + student
            rep = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
            patrst01 = '"result":\[(.*?)\]'
            # 正则提取查票的结果
            rst0 = re.compile(patrst01).findall(rep.content.decode())
            checimap_pat = '"map":({.*?})'
            checimap = eval(re.compile(checimap_pat).findall(rep.content.decode())[0])
            if rst0[0] == '':
                showinfo(title='警告', message='没有找到该车次的信息')
            rst01 = rst0[0]
            allcheci = rst01.split(",")
            # 点击查询按钮 先把内容清空
            x = self.tree.get_children()
            for item in x:
                self.tree.delete(item)

            for i in range(0, len(allcheci)):
                this_checi = allcheci[i].split("|")
                code = this_checi[3]
                from_name = this_checi[6]
                from_name = checimap[from_name]
                # [7]---toname
                toname = this_checi[7]
                toname = checimap[toname]
                # [8]---stime
                stime = this_checi[8]
                # [9]---atime
                atime = this_checi[9]
                # [28]---一等座
                yz = this_checi[31] if str(this_checi[31]) != '' else "-"
                # [29]---二等座
                wz = this_checi[30] if str(this_checi[30]) != '' else "-"
                # [30]---硬座
                ze = this_checi[29] if str(this_checi[29]) != '' else "-"
                # [31]---无座
                zy = this_checi[26] if str(this_checi[26]) != '' else "-"
                # 硬卧
                xx = this_checi[28] if str(this_checi[28]) != '' else "-"
                # 软卧
                yy = this_checi[23] if str(this_checi[23]) != '' else "-"
                # 将数据回显到软件中
                self.tree.insert('', i, values=(
                    code, from_name, toname, stime, atime, str(yz), str(wz), str(xx), str(yy), str(ze), str(zy)))
            # 查询完毕将按钮变为正常
            self.Command1.config(state=NORMAL)
            self.Command1['text'] = '查      询'
        except:
            self.Command1.config(state=NORMAL)
            self.Command1['text'] = '查      询'


if __name__ == "__main__":
    top = Tk()
    top.resizable(width=False, height=False)
    Application(top).mainloop()
    try:
        top.destroy()
    finally:
        print('except')
        pass

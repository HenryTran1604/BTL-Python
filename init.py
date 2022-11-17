import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from shopeeFunctions import *
from ImageFunctions import *
import threading
class Window(tk.Tk):
    def __init__(self, productList):
        self.productList = productList
        tk.Tk.__init__(self)
        self.title('TEAM 16 - Python scraping')
        self.geometry(getPosition(self, 800, 500))
        self.resizable(False, False)

    def accessToGithub(self):
        webbrowser.open("https://github.com/Team-16-Python-Scraping/final-python-scraping.git")

    def intro(self):
        intro = tk.Tk()
        intro.title('Welcome')
        intro.geometry(getPosition(intro))
        intro.after(3000, lambda: intro.destroy())
        intro.mainloop()
 
    def initPage(self):
        # Insert picture as background
        labelWidth = 800
        labelHeight = 500
        maxsize = (labelWidth, labelHeight)
        img = Image.open('Img/r.jpg')
        img = img.resize(maxsize)
        bg = ImageTk.PhotoImage(img)
        rootImg = tk.Label(self, image=bg)
        rootImg.place(in_=self, x=0, y=0)

        # Button about us for more infor
        btn_aboutUs = tk.Button(self, text='ABOUT US', bg='black',
                               fg='white', width=9, height=2,
                               font=('Inter', 10, 'bold'),command=self.accessToGithub)
        btn_aboutUs.pack(pady=2, anchor='e')

        #Create personal style
        style = ttk.Style()
        style.theme_create("Tab", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 4], "background": '#d2ffd2'},
                "map": {"background": [("selected", '#FF8C00')],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        style.theme_use("Tab")

        myfont = ('Inter', '11', 'bold')

        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        s = ttk.Style()
        s.configure('TNotebook.Tab', font=myfont)

        tabControl.add(tab1, text='Get product from shopee')
        tabControl.add(tab2, text='Get image from URL', )
        tabControl.pack(expand=1, fill="both")

        ttk.Label(tab1)  # root for shopee
        lbSearch = tk.Label(tab1, text='Nhập tên sản phẩm: ', font=myfont)
        eSearch = tk.Entry(tab1, width=70, font=myfont)
        frame = tk.LabelFrame(tab1, text='Danh sách thuộc tính cần lấy về', width=500, height=200)

        lbSearch.place(x=10, y=10)
        eSearch.focus()
        eSearch.place(x=180, y=10)
        frame.place(x=10, y=50)

        checkVar = tk.IntVar(value=1)
        ckbName = ttk.Checkbutton(frame, text='Tên sản phẩm', state=tk.DISABLED, variable=checkVar)
        ckbMinPrice = ttk.Checkbutton(frame, text='Giá nhỏ nhất', state=tk.DISABLED, variable=checkVar)
        ckbMaxPrice = ttk.Checkbutton(frame, text='Giá lớn nhất', state=tk.DISABLED, variable=checkVar)
        ckbRating = ttk.Checkbutton(frame, text='Đánh giá (sao)', state=tk.DISABLED, variable=checkVar)
        ckbLink = ttk.Checkbutton(frame, text='Link sản phẩm', state=tk.DISABLED, variable=checkVar)

        ckbName.place(x=15, y=10)
        ckbMinPrice.place(x=15, y=45)
        ckbMaxPrice.place(x=15, y=80)
        ckbRating.place(x=15, y=115)
        ckbLink.place(x=15, y=150)

        lbNumberOfPage = tk.Label(tab1, text='Số trang muốn lấy dữ liệu: ')
        eNumberOfPage = tk.Entry(tab1, width=20, textvariable=tk.IntVar(value=1))
        lbNumberOfPage.place(x=10, y=265)
        eNumberOfPage.place(x=170, y=265)

        imgLogo = ImageTk.PhotoImage(Image.open('Img/logoshopee.png').resize((205, 205)))
        lbLogo = tk.Label(tab1, image=imgLogo)

        lbLogo.place(x=550, y=45)

        btnSearch = tk.Button(tab1, text='TRA CỨU!', font=myfont, command= lambda: threading.Thread(target=accessToShopee, args=(tab1, eNumberOfPage.get(), eSearch.get(), self)).start())
        lbCopyRight = tk.Label(tab1, text='@2022 - team 16 PTIT',
                               height=2, bg='black', fg='white',
                               font=myfont, relief=tk.SUNKEN, width=self.winfo_screenwidth(), anchor=tk.W)
        btnSearch.place(x=550, y=270)
        lbCopyRight.pack(side='bottom', fill='y')

        ttk.Label(tab2)

        lbUrl = tk.Label(tab2, text='Nhập url bạn muốn lấy ảnh: ', font=myfont)
        lbLimit = tk.Label(tab2, text='Nhập số lượng tối đa ảnh: \n(Bỏ trống nếu muốn lấy tất cả)')
        eLimit = tk.Entry(tab2, width=20, font=myfont)
        eUrl = tk.Entry(tab2, width=65, font=myfont)
        btnSearch2 = tk.Button(tab2, text='Lấy ảnh!', font=myfont, command=lambda :threading.Thread(target=getImage_run, args=(tab2, eUrl.get(), r'C:\team16\images', eLimit.get())).start())

        lbUrl.place(x=10, y=10)
        lbLimit.place(x=10, y=50)
        eUrl.focus_set()
        eUrl.place(x=220, y = 10)
        eLimit.place(x=220, y=50)
        btnSearch2.place(x=650, y = 80)

        

        lbCopyRight = tk.Label(tab2, text='@2022 - team 16 PTIT',
                               height=2, bg='black', fg='white',
                               font=myfont, relief=tk.SUNKEN, width=self.winfo_screenwidth(), anchor=tk.W)

        lbCopyRight.pack(side='bottom', fill='y')
        self.mainloop()

    def run(self):
        self.initPage()

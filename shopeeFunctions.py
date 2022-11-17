import threading
from concurrent.futures import ThreadPoolExecutor
import tkinter
from tkinter import messagebox
from tkinter import ttk
from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser
import time
import csv
from Product import Product
import tkinter as tk
from tkinter import CENTER, Toplevel, ttk
import webbrowser
import os
# link to chromedriver app in your pc
PATH = r'C:\Program Files (x86)\Chromedriver\chromedriver.exe'


def getPosition(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    return f'{window_width}x{window_height}+{position_right}+{position_top}'


def generateLinks(numberOfPage, searched_product):
    urlList = []
    for i in range(numberOfPage):
        search = searched_product.lower().replace(' ', '%20')
        url = "https://shopee.vn/search?keyword={}&page={}".format(search, i)
        urlList.append(url)
    return urlList


def getHtml(url):  # get source code of web
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=PATH, options=options)
        driver.get(url)
        time.sleep(3)
        for i in range(15):
            driver.execute_script("window.scrollBy(0, 450)")
            time.sleep(0.1)

        html = driver.page_source
        driver.close()
        soup = BeautifulSoup(html, 'lxml')
        return soup
    except :
        return None


# productList = []  # use global var for fill the table and export to csv file
win, pb = None, None

def showProgressBar(root):
    global win, pb
    win = Toplevel()
    win.title('Đang xử lý...')
    win.attributes("-topmost", True)
    win.geometry(getPosition(root, 300, 120))
    win.resizable(False, False)
    pb = ttk.Progressbar(
        win,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )
    pb.grid(row=0, column=0, columnspan=2, padx=10, pady=20)
    cancel_button = ttk.Button(
        win,
        text='Cancel',
        command=win.destroy
    )
    cancel_button.grid(column=0, row=1, padx=10, pady=10, sticky=tkinter.E)
    pb.start()


def endProgressBar():
    global win, pb
    pb.destroy()
    win.destroy()

def fillProductList(url, App, root):
    soup = getHtml(url)
    if soup == None:
        endProgressBar()
        return

    items = soup.find_all(
        'div', class_='col-xs-2-4 shopee-search-item-result__item')
    for item in items:

        # name
        nameItem = item.find('div', class_='ie3A+n bM+7UW Cve6sh').text
        price = item.findAll('span', class_='ZEgDH9')

        minPrice, maxPrice = 0, 0
        if len(price) > 1:
            minPrice, maxPrice = [int(x.text.replace('.', '')) for x in price]
        else:
            minPrice = maxPrice = int(price[0].text.replace('.', ''))

        # rating
        stars = item.findAll('div', class_='shopee-rating-stars__lit')
        rating = 0
        if stars != None:
            for star in stars:
                rating += float(star['style'].split()[1][:-2]) / 100

        quantity, sales = item.find('div', class_='r6HknA uEPGHT'), '0'
        if quantity != None:
            sales = quantity.text.split(
            )[-1].replace(',', '').replace('k', '000')

        # link
        linkItem = 'https://shopee.vn' + item.find('a')['href']
        p = Product(nameItem, minPrice, maxPrice, rating, sales, linkItem)
        App.productList.append(p)
def run(root, numberOfPage, searched_product, App):
    App.productList.clear()
    urls = generateLinks(numberOfPage, searched_product)
    showProgressBar(root)
    with ThreadPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
        for url in urls:
            executor.submit(fillProductList, *[url, App, root])
    if len(App.productList) != 0:
        showProducts(App)
    else:
        messagebox.showerror('Error', 'Có lỗi xảy ra\nVui lòng kiểm tra lại')

    endProgressBar()


def writeToFile(name, App):
    if len(name) == 0:
        messagebox.showerror("Error", "Bạn chưa nhập tên file")
    else:
        path = r'C:\team16\Data'
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        csvFile = open(f'{path}\{name}.csv', 'w+',
                       encoding='utf-16', newline='')
        try:
            writer = csv.writer(csvFile, delimiter='\t')
            writer.writerow(
                ('Tên sản phẩm', 'Giá nhỏ nhất', 'Giá lớn nhất', 'Đánh giá sản phẩm', 'Doanh số', 'Link sản phẩm'))
            writer.writerows(App.productList)
        except:
            messagebox.showerror('ERROR', 'Đã có lỗi xảy ra!')
        finally:
            csvFile.close()
            messagebox.showinfo(
                "Sucessfully!", 'Đã lưu vào file vào thư mục C:\\team16\\Data')


def clearTreeView(productTree):
    for i in productTree.get_children():
        productTree.delete(i)


def fillTreeView(productTree, App):
    contacts = []
    for i in range(0, len(App.productList)):
        contacts.append((i+1, App.productList[i].name, App.productList[i].minPrice, App.productList[i].maxPrice,
                        App.productList[i].sales, '%.1f' % App.productList[i].rating, App.productList[i].link))
    productTree.tag_configure('oddrow', background="#7DE5ED")
    productTree.tag_configure('evenrow', background="white")
    count = 0
    for contact in contacts:
        if (count % 2 == 0):
            productTree.insert('', tk.END, values=contact, tags="oddrow")
        else:
            productTree.insert('', tk.END, values=contact, tags="evenrow")
        count += 1


def showProducts(App):  # ProductTable
    table = Toplevel()
    # table.attributes('-topmost', True)
    table.title('Danh sách sản phẩm')
    table.geometry("1200x424")
    table.resizable(False, False)
    # Construct Treeview
    columns = ['S_T_T', 'Tên_sản_phẩm', 'Giá_nhỏ_nhất',
               'Giá_lớn_nhất', 'Đã_bán', 'Sao_đánh_giá', 'Link_sản_phẩm']
    productTree = ttk.Treeview(
        table, columns=columns, show='headings', cursor="hand2 orange")

    def columnConstructor(cl, text, w):
        productTree.heading(cl, text=text)
        productTree.column(cl, width=w, anchor=CENTER)
    columnConstructor('S_T_T', 'STT', 50)
    columnConstructor('Tên_sản_phẩm', 'Tên sản phẩm', 210)
    columnConstructor('Giá_nhỏ_nhất', 'Giá nhỏ nhất', 100)
    columnConstructor('Giá_lớn_nhất', 'Giá lớn nhất', 100)
    columnConstructor('Đã_bán', 'Đã bán', 80)
    columnConstructor('Sao_đánh_giá', 'Sao đánh giá', 100)
    columnConstructor('Link_sản_phẩm', 'Link sản phẩm', 300)
    contacts = []
    for i in range(0, len(App.productList)):
        contacts.append((i+1, App.productList[i].name, App.productList[i].minPrice, App.productList[i].maxPrice,
                        App.productList[i].sales, '%.1f' % App.productList[i].rating, App.productList[i].link))
    productTree.tag_configure('oddrow', background="#7DE5ED")
    productTree.tag_configure('evenrow', background="white")
    count = 0
    for contact in contacts:
        if (count % 2 == 0):
            productTree.insert('', tk.END, values=contact, tags="oddrow")
        else:
            productTree.insert('', tk.END, values=contact, tags="evenrow")
        count += 1
    s2 = ttk.Style()
    s2.theme_use("default")
    s2.configure('Treeview.Heading', background="orange", bd=1)
    s2.configure('Treeview', rowheight=40, border=1)
    s2.map('Treeview', background=[('selected', 'orange')],)
    # Access to link of selected product

    def goLink(event):
        input_id = productTree.selection()
        input_item = productTree.set(input_id, column="Link_sản_phẩm")
        webbrowser.open('{}'.format(input_item))
    productTree.bind("<Double-1>", goLink)
    productTree.grid(row=0, column=0, sticky='nsew')
    # Scrollbar
    scrollbar = ttk.Scrollbar(
        table, orient=tk.VERTICAL, command=productTree.yview)
    productTree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    def sortByPrice():
        clearTreeView(productTree)
        App.productList.sort(key=lambda x: (x.minPrice, x.maxPrice, -x.rating, -int(x.sales)))
        fillTreeView(productTree, App)

    def sortByRating():
        clearTreeView(productTree)
        App.productList.sort(key=lambda x: (-x.rating, -int(x.sales), x.minPrice ,x.maxPrice))
        fillTreeView(productTree, App)

    def sortBySales():
        clearTreeView(productTree)
        App.productList.sort(key=lambda x: (-int(x.sales), -x.rating, x.minPrice, x.maxPrice))
        fillTreeView(productTree, App)


    # Set Selections
    selections = tk.Frame(table, relief="solid")
    selections.place(x=980, y=60, height=350, width=200)
    btn_sortPrice = tk.Button(selections, text="Sắp xếp theo giá tăng dần",
                              pady=10, fg="white", bg="black", cursor="hand2", command=sortByPrice)
    btn_sortSales = tk.Button(selections, text="Sắp xếp theo doanh số giảm dần",
                                     pady=10, fg="white", bg="black", cursor="hand2", command=sortBySales)
    btn_sortRate = tk.Button(selections, text="Sắp xếp theo đánh giá giảm dần",
                             pady=10, fg="white", bg="black", cursor="hand2", command=sortByRating)
    lb_exportToFile = tk.Label(selections, text='Nhập tên file: ')
    e_exportToFile = tk.Entry(selections, width=40)
    btn_exportToFile = tk.Button(selections, text='Lưu vào file csv!', pady=10,
                                 fg='white', bg='green', command=lambda: writeToFile(e_exportToFile.get(),App))
    btn_sortPrice.pack(pady=10)
    btn_sortSales.pack(pady=10)
    btn_sortRate.pack(pady=10)
    lb_exportToFile.pack(pady=10)
    e_exportToFile.pack(pady=5)
    btn_exportToFile.pack(pady=10)


def accessToShopee(root, numberOfPage, searchedProduct, App):
    if len(searchedProduct) == 0:
        messagebox.showerror("Warning", "Bạn chưa nhập tên sản phẩm")
    else:
        try:
            n = int(numberOfPage)
            if n > 10:
                messagebox.showwarning("Error", 'Số lượng trang quá lớn\nVui lòng thử lại')
            else:
                threading.Thread(target=run, args=(
                    root, n, searchedProduct, App)).start()

        except:
            messagebox.showerror("Error", "Mời bạn nhập đúng định dạng!")

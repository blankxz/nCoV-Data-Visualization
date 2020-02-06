from pyecharts import options as opts
from pyecharts.charts import Map, Page
from pyecharts.faker import Collector, Faker
import csv

province = {}
date = '1月11日'
date_data = {}
foreign = ['泰国','日本','韩国','美国','越南','新加坡','尼泊尔','法国','澳大利亚','马来西亚','加拿大','斯里兰卡','柬埔寨','德国','阿联酋','印度','菲律宾','芬兰','意大利']
with open('Updates_NC.csv',encoding='GBK') as f:
    f_csv = list(csv.reader(f))
    f_csv.pop(0)
    f_csv.reverse()
    flag = 0
    for row in f_csv:
        if row[0] != date:
            date_data[date] = province.copy()
            date = row[0]
        if row[1] not in province:
            if row[1] not in foreign:
                province[row[1]] = int(row[3])
        else:
            province[row[1]] += int(row[3])
    date_data[date] = province.copy()

data = {}
for i in date_data:
    ll = []
    for j in date_data[i]:
        l = []
        l.append(j)
        l.append(str(date_data[i][j]))
        ll.append(l)
    data[i] = ll

# print(data)

C = Collector()



@C.funcs
def map_visualmap(data,title) -> Map:
    c = (
        Map(init_opts=opts.InitOpts(width='1500px',height='700px'))
        .add("", data, "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(max_=300),
        )
    )
    return c

# @C.funcs
# def map_visualmap_piecewise(data) -> Map:
#     c = (
#         Map()
#         .add("", data, "china")
#         .set_global_opts(
#             title_opts=opts.TitleOpts(title="Map-VisualMap（分段型）"),
#             visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
#         )
#     )
#     return c

for i in data:
    dd = sorted(data[i], key=lambda h: int(h[1]),reverse=True)
    print(dd)
    num = 0
    for j in dd:
        num += int(j[1])
    title = i+'，全国共感染 ' + str(num) + ' 人，其中\n\n'
    for j in dd:
        if dd.index(j) % 4 == 0 and dd.index(j) != 0:
            title += j[0] + ':' + j[1] + '人 \n\n'
        else:
            title += j[0] + ':' + j[1] + '人 '
    Page().add(*[fn(dd,title) for fn, _ in C.charts]).render(i+'.html')
    
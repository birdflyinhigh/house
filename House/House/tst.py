base_url_bj = 'http://esf.house.163.com/bj/search/{}-0-0-0-1.html'
for i in range(1, 19):
    bj_url = base_url_bj.format(i)
    print(bj_url)
from requests import get
from re import findall
from time import sleep
root_url = "https://blog.reimu.net/"
classes = ["3D", "anime", "collection", "picture", "wallpaper", "android", "game", "comic", "indie", "music", "ALL"]


def get_total_pages(type):
    type_root = "https://blog.reimu.net/archives/category/"
    url = type_root + type
    print("[*]Getting total pages of %s..."%type)
    res = get(url)
    r = findall("%s/page/(\d+).*?\">"%url, res.text)
    ans = int(r[-1])
    print("[*]Success! %d pages in total!"%ans)
    return ans

def get_magnets_in_certain_page(links, ff):
    curr = 1
    tot = len(links)

    for i in links:
        if curr%50==0:
            print("[*]Sleep 8s for every 50 step!")
            sleep(8)

        try:
            res = get(i)
        except Exception as err:
            # sleep 10s, then try again
            sleep(10)
            try:
                res = get(i)
            except Exception as e:
                # skip it
                print(e)
                continue

        title = findall("<h1 class=\"entry-title\">(.*?)</h1>", res.text)
        magnets = findall("(magnet:\?xt=urn:btih:[0-9a-fA-F]{40})", res.text)
        mega_links = findall("(https://mega.nz/.*?)\"", res.text)
        baidupan_links = findall("\"(https://pan.baidu.com/s/.*?)\"", res.text)
        baidupan_passes = findall("提取码.*?[0-9A-Za-z]{4}", res.text)
        # zip_password = findall("([解][压][密]*[码].{5})", res.text)

        if len(title)==0:
            # skip
            curr+=1
            continue
        else:
            print("(%d, %d) %s  (original: %s)" % (curr, tot, title[0], i))
            ff.write(title[0] + "  (%s)\n"%i)

        if len(magnets)==0 and (len(baidupan_links)==0 or len(baidupan_passes)==0) and len(mega_links)==0:
            ff.write("\t" + "No baidu pan links, mega links or magnets found, please visit the original page\n")

        if len(magnets)!=0:
            for each in magnets:
                ff.write("\t" + "磁力链: " + each +"\n")

        if len(mega_links)!=0:
            for each in mega_links:
                ff.write("\t" + "mega网盘: " + each + "\n")


        if len(baidupan_links)!=0 and len(baidupan_passes)!=0:
            for i in range(min(len(baidupan_links), len(baidupan_passes))):
                ff.write("\t" + "baidu网盘: " + baidupan_links[i] + "  " + baidupan_passes[i] + "\n")


        # if len(zip_password)!=0:
        #     for each in zip_password:
        #         ff.write("\t" + each + "\n")

        ff.write("\n")
        curr+=1
        sleep(2)

def get_links_in_one_page(url_of_page):
    rsp = get(url_of_page).text
    res = findall("href=\"(https://blog.reimu.net/archives/\d+)\"", rsp)

    return res
def start(typ):
    f = open("%s.txt"%typ, "w", encoding="utf-8")
    pages = get_total_pages(typ)
    links_vec = []
    for pg in range(1, pages+1):
        print("[*](%d, %d)Sleep for 3s" % (pg, pages))
        sleep(3)
        links_vec.append(get_links_in_one_page("https://blog.reimu.net/archives/category/%s/page/%d" % (typ, pg)))

    # remove the repeated one
    st = set()
    for i in links_vec:
        for j in i:
            st.add(j)
    print("[*]Saving for %s, please wait!"%typ)
    get_magnets_in_certain_page(st, f)


def main():
    class_num = len(classes)-1
    # get user's order
    for i in range(0, class_num+1):
       print("%d: %s" % (i, classes[i]))
    op = int(input("Choose a number to start: "))

    if classes[op] != 'ALL':
        start(classes[op])
    else:
        for i in range(0, class_num):
            start(classes[i])


            print("[*]Sleep for 10s before next class", end='\n\n')
            sleep(10)


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(err)
        print("[!]Failed, please try again.")
        exit(-1)
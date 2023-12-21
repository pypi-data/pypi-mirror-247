from remote_run_everything import Conf, Local, ByHttp


def test():
    c = Conf(
        host="127.0.0.1",
        user="root",
        pwd='123456',
        remote_root="/mnt/myrust/ssl",
        local_root="D://mygit/remote_run_everything",
    )
    # r = Remote(c)
    l = Local(c)

    # step1:代码文件同步：这个命令会把local_root下的子文件夹递归复制到remote_root对应的子文件夹,虚拟机共享文件夹不需要本步骤
    l.upload(c.local_root, exclude=["node_modules"])

    # step2: 命令行：这个命令会在远程环境remot_root文件夹中执行cargo run，并把输出结果打印在屏幕。多个命令以列表形式传递
    # r.cmd(['cargo run'])

    # step3：代码智能补全文件下载： 这个命令会把remote_root的子文件夹复制到local_root对应子文件夹,虚拟机共享文件夹不需要本步骤，这一步的意义在于ide智能补全（编译代码在虚拟机，本地没有）。实际中，执行此步骤需要根据语言变更子文件夹,以rust为例，复制target即可

    # l.download(c.remote_root+"/target")

    # print (l.upload_scripts())


import requests


def pull_example():
    bh = ByHttp("localhost", "D://", "D://wq", "D://temp")
    url = "http://127.0.0.1:8080/deploy/iterdir"
    req = requests.post(url, json={"root": "D://temp"}).json()
    for i in bh.pull_list(req['message']):
        print(i)
        pull = bh.will_pull(i['lpath'], i['time'])
        print (pull)
        if pull:
            url = "http://127.0.0.1:8080/deploy/readfileb64"
            req = requests.post(url, json={'path': i['rpath']}).json()
            b64 = req['message']
            bh.writeb64(i['lpath'], b64)


pull_example()


def push_example():
    bh = ByHttp("localhost", "D://", "D://temp", "D://wq")
    push_url = "http://127.0.0.1:8080/wmsApi/deploy/upmycode"
    for i in bh.push_list():
        print(i['rpath'])
        pay = {"b64": i['b64'], "path": i['rpath']}
        print(bh.will_push(i['lpath']))
        req = requests.post(push_url, json=pay)

        print(req.json())

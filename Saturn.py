import requests
from threading import Thread
from random import randint,choice
from time import sleep
from tkinter import *
from tkinter import messagebox
from io import BytesIO
from PIL import Image, ImageTk
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyperclip import copy

window = Tk()
window.title("Saturn | Total Groups Found : 0")
window.geometry("548x866")
window.maxsize(548, 866)
window.minsize(548, 866)
window.iconbitmap("assets/mylogo.ico")
backg = PhotoImage(file='assets/background.png')
backg2 = PhotoImage(file='assets/background2.png')
blankbu = PhotoImage(file='assets/blank.png')
fullbu = PhotoImage(file='assets/full.png')
finding = PhotoImage(file='assets/finding.png')
notrunning = PhotoImage(file='assets/notrunning.png')
online0 = PhotoImage(file='assets/online0.png')
online1 = PhotoImage(file='assets/online1.png')
online2 = PhotoImage(file='assets/online2.png')
online3 = PhotoImage(file='assets/online3.png')
online4 = PhotoImage(file='assets/online4.png')
stopped = PhotoImage(file='assets/stopped.png')
blankthumb = PhotoImage(file='assets/blankthumb.png')
claim = PhotoImage(file='assets/claim.png')

class Saturn:

    def __init__(self):
        self._IsRunning = False
        self._429_counts = 0
        self._ValidsCount = 0
        self._Triies = 0
        self.RetryID = ""
        self.ScannedIDs = []
        self.ValidIDs = []
        self.Proxies = []
        self._isproxy = False
        self._LoadProxies()
        self.RateLimitTime = 1
        Thread(target=self._Saturn).start()

    def _LoadProxies(self,path="proxies/proxies.txt"):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if "ip:port" in line:
                    continue
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) == 2:
                    ip, port = parts
                    proxy = f"http://{ip}:{port}"
                elif len(parts) == 4:
                    ip, port, user, pwd = parts
                    proxy = f"http://{user}:{pwd}@{ip}:{port}"
                else:
                    continue
                self.Proxies.append(proxy)
                self._isproxy = True
        return self.Proxies

    def _GetRandomProx(self):
        bomba = choice(self.Proxies)
        bomba = str(bomba).strip()
        return {
            "http": bomba,
            "https": bomba
        }

    def _AddGroupToListBox(self,grp):
        self.GroupList.insert(END, grp)
        window.title(f"Saturn | Total Groups Found : {self._ValidsCount}")

    def _StartScan(self):
        Thread(target=self._UpdateLogs, args=("[+] Process Started, Finding Available Groups..\n",)).start()
        session = requests.Session()
        self.concurrent_requests = 20
        self.min_batch = 5
        self.max_batch = 50
        self.RetryQueue = []

        def scan_v1(ID):
            try:
                resp = session.get(f"https://groups.roblox.com/v1/groups/{ID}", timeout=10, proxies=self._GetRandomProx() if self._isproxy else None)
                if resp.status_code == 429:
                    return "429", ID
                if resp.status_code != 200:
                    return "skip", ID
                data = resp.json()
                if data.get('memberCount', 0) == 0 or not data.get('publicEntryAllowed', False):
                    return "skip", ID
                if data.get('isLocked', False):
                    return "skip", ID
                if data.get('owner') is None:
                    return "valid", f"{ID} - {data.get('name')} - {data.get('memberCount')} members"
            except:
                return "skip", ID
            return "skip", ID

        while self._IsRunning:
            batch_ids = []
            while self.RetryQueue and len(batch_ids) < self.concurrent_requests:
                batch_ids.append(self.RetryQueue.pop(0))
            while len(batch_ids) < self.concurrent_requests:
                batch_ids.append(randint(1000, 1_500_000))
            try:
                v2_url = "https://groups.roblox.com/v2/groups?groupIds=" + ",".join(str(i) for i in batch_ids)
                self._Triies += len(batch_ids)
                v2_resp = session.get(v2_url, timeout=10,proxies=self._GetRandomProx() if self._isproxy else None)
                if v2_resp.status_code == 429:
                    self.RetryQueue.extend(batch_ids)
                    self.concurrent_requests = max(self.min_batch, self.concurrent_requests - 5)
                    Thread(target=self._UpdateLogs,args=(f"[429] v2 Rate Limited, decreasing batch to {self.concurrent_requests}\n",)).start()
                    sleep(randint(1000, 3000)/1000)
                    continue
                elif v2_resp.status_code != 200:
                    for ID in batch_ids:
                        self.ScannedIDs.append(ID)
                    continue
                data = v2_resp.json().get("data", [])
                candidate_ids = [grp["id"] for grp in data if grp.get("owner") is None]
                if not candidate_ids:
                    continue
            except:
                candidate_ids = batch_ids
            futures = {}
            executor = ThreadPoolExecutor(max_workers=len(candidate_ids))
            for ID in candidate_ids:
                futures[executor.submit(scan_v1, ID)] = ID
            for fut in as_completed(futures):
                status, result = fut.result()
                if status == "valid":
                    self.ValidIDs.append(result.split(" - ")[0])
                    self._ValidsCount += 1
                    Thread(target=self._UpdateLogs, args=("[+] Found Valid Group\n",)).start()
                    window.after(0, lambda r=result: self._AddGroupToListBox(r))
                elif status == "429":
                    self._429_counts +=1
                    self.RetryQueue.append(result)
                    self.concurrent_requests = max(self.min_batch, self.concurrent_requests - 5)
                    Thread(target=self._UpdateLogs,
                        args=(f"[429] v1 Rate Limited, decreasing batch to {self.concurrent_requests}\n",)).start()
                    sleep(randint(1000, 3000)/1000)
                else:
                    self.ScannedIDs.append(result)
            batch_success_count = sum(1 for fut in futures if fut.result()[0] == "valid")
            batch_total = len(futures)
            if batch_total > 0:
                success_rate = batch_success_count / batch_total
                if success_rate > 0.3:
                    self.concurrent_requests = min(self.max_batch, self.concurrent_requests + 2)
                elif success_rate < 0.05:
                    self.concurrent_requests = max(self.min_batch, self.concurrent_requests - 2)
            if self._429_counts >= 5:
                Thread(target=self._UpdateLogs,args=(f"[429] Too many rate limits, sleeping 10s\n",)).start()
                sleep(randint(9000, 12000)/1000)
                self._429_counts = 0
            else:
                sleep(randint(500, 1500) / 1000)
            if self._Triies % 100 == 0:
                Thread(target=self._UpdateLogs,args=(f"[+] Currently at : {self._Triies} tries\n",)).start()
        Thread(target=self._UpdateLogs, args=("\n[+] Process Stopped\n",)).start()

    def _UpdateLogs(self,msg):
        try:
            self.Logs.insert("end", msg)
        except:
            pass

    def _StateGIF(self):
        while self._IsRunning:
            self.state_a.config(image=online1)
            sleep(0.06)
            self.state_a.config(image=online2)
            sleep(0.06)
            self.state_a.config(image=online3)
            sleep(0.06)
            self.state_a.config(image=online4)
            sleep(0.06)
            self.state_a.config(image=online3)
            sleep(0.06)
            self.state_a.config(image=online2)
            sleep(0.06)
            self.state_a.config(image=online1)
            sleep(0.06)
            self.state_a.config(image=online0)
            sleep(0.8)
        self.state_a.config(image=notrunning)

    def _OnOffSaturn(self):
        if self._IsRunning:
            self._IsRunning = False
            self.Start_Finder.config(image=blankbu)
            self.State_text.config(image=stopped)
        else:
            self._IsRunning = True
            self.Start_Finder.config(image=fullbu)
            self.State_text.config(image=finding)
            Thread(target=self._StateGIF).start()
            Thread(target=self._StartScan).start()

    def _ThumbNail(self,url):
        response = requests.get(url)
        image_data = response.content
        pil_image = Image.open(BytesIO(image_data))
        tk_image = ImageTk.PhotoImage(pil_image)
        self.ThumbnailLabel.configure(image=tk_image)
        self.ThumbnailLabel.image = tk_image 

    def _CopyGroupLink(self):
        copy(self.temp_grplink)
        messagebox.showinfo("Saturn","Link copied ! Paste it on your browser join & claim your group !")

    def _GUIGrpInfo(self,info):
        self.temp_grplink = f"https://www.roblox.com/communities/{info[0]}"
        self.grpinfogui = Toplevel(window)
        self.grpinfogui.title("Saturn Unowned Group Information")
        self.grpinfogui.geometry("548x391")
        self.grpinfogui.maxsize(548, 391)
        self.grpinfogui.minsize(548, 391)
        self.grpinfogui.iconbitmap("assets/mylogo.ico")
        Bg = Label(self.grpinfogui, image=backg2,borderwidth=0)
        Bg.place(x=0, y=0)
        self.ThumbnailLabel = Label(self.grpinfogui, image=blankthumb,borderwidth=0,bg='#111111')
        self.ThumbnailLabel.place(x=45,y=156)
        claimgroup = Button(self.grpinfogui, image=claim,bg='#111111',borderwidth=0, activebackground="#111111",command=self._CopyGroupLink)
        claimgroup.place(x=34,y=322)
        grpID = Label(self.grpinfogui, text=f"{info[0]}",font=("Inter",13),bg="#111111",fg="#FFFFFF")
        grpID.place(x=295,y=153)
        mmberc = Label(self.grpinfogui, text=f"{info[3]}",font=("Inter",13),bg="#111111",fg="#FFFFFF")
        mmberc.place(x=299,y=185)
        grpname = Label(self.grpinfogui, text=f"{str(info[1]).split(' -')[0]}",font=("Inter",13),bg="#111111",fg="#FFFFFF")
        grpname.place(x=273,y=217)
        Thread(target=self._ThumbNail,args=(info[2],)).start()

    def _GrpInformation(self,ID_grp):
        info_html = requests.get(f"https://www.roblox.com/groups/group.aspx?gid={ID_grp}",timeout=10,proxies=self._GetRandomProx() if self._isproxy else None)
        if info_html.status_code == 200:
            infol = []
            info = info_html.text
            name = info.split('<title>')[1].split("</title>")[0]
            thumb = info.split('https://tr.rbxcdn.com/')[1].split("noFilter")[0]
            fullthumb = f"https://tr.rbxcdn.com/{thumb}noFilter"
            members = info.split(' members.')[0].split('with ')[1]
            infol.append(ID_grp);infol.append(name);infol.append(fullthumb);infol.append(members)
            Thread(target=self._GUIGrpInfo,args=(infol,)).start()
        elif info_html.status_code == 429:
            messagebox.showerror("Saturn","429 Error, too many requests.\nIf saturn is finding groups, stop it, wait a few seconds (4,8s) and try again")

    def _OpenGroup(self,event):
        selected_index = self.GroupList.curselection()
        if selected_index:
            selected_item = self.GroupList.get(selected_index[0])
            ID_grp = str(selected_item).split(" -")[0]
            Thread(target=self._GrpInformation,args=(ID_grp,)).start()

    def _Saturn(self):
        Bg = Label(window, image=backg,borderwidth=0)
        Bg.place(x=0, y=0)
        self.Start_Finder = Button(window, image=blankbu,bg='#111111',borderwidth=0, activebackground="#111111",command=self._OnOffSaturn)
        self.Start_Finder.place(x=346,y=196)
        self.State_text = Label(window, image=stopped,bg='#111111',borderwidth=0, activebackground="#111111")
        self.State_text.place(x=80,y=152)
        self.state_a = Label(window, image=notrunning,bg='#111111',borderwidth=0, activebackground="#111111")
        self.state_a.place(x=31,y=145)
        self.GroupList = Listbox(window, bg="#0A0A0A", fg="#FFFFFF", width=78, height=20, borderwidth=0)
        self.GroupList.place(x=42,y=285)
        self.Logs = Text(window, bg="#0B0B0B", fg="#FFFFFF",wrap="none",width=59, height=8, borderwidth=0)
        self.Logs.place(x=37,y=686)
        self.GroupList.bind("<<ListboxSelect>>", self._OpenGroup)

Saturn()
window.mainloop()
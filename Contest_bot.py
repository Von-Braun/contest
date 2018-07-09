import praw,string,os
from random import choice
from Tkinter import *

printable = set(string.printable)

user_agent = ("contest_automaton/v0.1 (by /u/Anatoly_Korenchkin)")
account_file=open('account_file.txt','r')
REDDIT_USERNAME = account_file.readline().strip('\n')
REDDIT_PASS = account_file.readline().strip('\n')
REDDIT_CLIENT_ID = account_file.readline().strip('\n')
REDDIT_CLIENT_SECRET = account_file.readline().strip('\n')

r = praw.Reddit(user_agent = user_agent,client_id=REDDIT_CLIENT_ID,client_secret=REDDIT_CLIENT_SECRET,username=REDDIT_USERNAME,password=REDDIT_PASS)
root = Tk() #create the window
root.wm_title("Contest_bot") #name the window
root.resizable(0,0)
root.geometry('{}x{}'.format(400, 50))
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

directory=os.getcwd()+'/Excel Contest Records'
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)

def paste():
    root.wm_title("Contest_bot - Processing...") #name the window
    text = root.selection_get(selection='CLIPBOARD')
    entry.delete(0, END)
    entry.insert(0, text)

    submission = r.submission(url=text)
    #print 'Prepare for PAIN!'
    submission.comments.replace_more(limit=None, threshold=1)
    commentlist= submission.comments#.list()

    root_comments=[]
    comment_authors=[]
    comment_bodys=[]
    for comment in commentlist:
        root_comments.append(comment)
    root_comments.sort(key=lambda comment: comment.created_utc, reverse=True)
    for comment in root_comments:
        if comment.author not in comment_authors:
            comment_authors.append(comment.author)
            comment_bodys.append(comment.body)
    print 'Collected '+str(len(root_comments))+' root comments. Removed '+str(len(root_comments)-len(comment_authors))+' duplicates.'

    save_file=open('Contest_'+submission.id+'.csv','w')
    save_file.write('#,Name,Comment\n')

    winner = choice(comment_authors)
    user_entry_text.set(winner)
    entry_text.set(submission.id)

    for count,comment in enumerate(comment_authors):
        if comment==winner:
            tag='WINNER'
        else:
            tag=''
        text=filter(lambda x: x in printable, comment_bodys[count])
        save_file.write(tag+str(count+1)+','+str(comment)+','+str(text).replace('\n',' ').replace(',','')+'\n')
        


    root.wm_title("Contest_bot - Done") #name the window



entry_text=StringVar() #create the variables where the input to the entry boxes is stored
entry = Entry(root, width=67, textvariable=entry_text) #create the entry boxes


user_entry_text=StringVar() #create the variables where the input to the entry boxes is stored
user_entry = Entry(root, width=67, textvariable=user_entry_text) #create the entry boxes

v1 = StringVar()
bot_url = Label(textvariable=v1)
v1.set('URL: ')

v2 = StringVar()
bot_select = Label(textvariable=v2)
v2.set('I have selected: ')

button_1=Button(root, text='Paste URL', command=paste, width=17) #create buttons
button_1.grid(row=0, column=2) #place a button in the window
bot_url.grid(row=0, column=0,sticky=W) #place a button in the window
entry.grid(row=0, column=1,sticky=W)
bot_select.grid(row=1, column=0,sticky=W) #place a button in the window
user_entry.grid(row=1, column=1,sticky=W) 

root.mainloop() #stop the window from closing

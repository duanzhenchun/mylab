"""
by lucida (lucida@users.sf.net/acura@smth.org)
Version 2.2
A script to post files @SMTH BBS(www.smth.org)
Require curl and pygtk>=2.0
"""

#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys, os, string, codecs, urllib, re, gtk
import qterm
from sgmllib import SGMLParser
from gtk import *  # Generally advertised as safe


lp = long(sys.argv[0])
# user settings

# program path
CURL = '/usr/bin/curl'
ICONV = '/usr/bin/iconv'

# parameters for curl
myid = 'this is my id'
mypass = 'this is my password'

# signature settings
usesignature = '1'

# temp. files
tmpfile = '/tmp/.qterm.tmp1234'
cookie = '/tmp/.qterm.cookie'

# smth files.
smth_url = 'http://proxy.smth.org/'

userAgent = ' "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)" '

phplogin = 'bbslogin.php'
phpupload = 'bbsupload.php'
phplogout = 'bbslogout.php'
phppost = 'bbspst.php'
phpsend = 'bbssnd.php'
phpdoc = 'bbsdoc.php'

class TextExtracter(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.text = 0
        self.input = 0
        self.textarea = ''
        self.title = ''
        
    def start_textarea(self, attrs):
        self.text = 1

    def handle_data(self, data):
        if self.text == 1 and data:
            self.textarea = data
            
    def end_textarea(self):
        self.text = 0

    def start_input(self, attrs):
        mytitle = [v for k, v in attrs if k == 'value']
        if mytitle and self.input == 0:
            self.title = mytitle
            self.input = 1
            
class QPostIt:
    def delete_event(self, widget, event, data=None):
        if self.logined:
            self.logout()
        self.window.hide()
        gtk.main_quit()
        return gtk.FALSE

    def login(self):
# login and set cookie        
        if self.logined == 1:
            return

        print "login..."
        self.runcmd = CURL + ' -A ' + userAgent \
                        + ' -F "id=' + myid + '" -F "passwd=' + mypass \
                        + '" -F "kick_multi=0" ' + smth_url + phplogin \
                        + ' -c ' + cookie
# print self.runcmd
        p = os.popen(self.runcmd)
        p.close()
        self.logined = 1

    def logout(self):
        print 'logout...'
# logout and delete cookie
        self.runcmd = CURL + ' -A ' + userAgent \
            + smth_url + phplogout \
            + ' -b ' + cookie
# print self.runcmd
        p = os.popen(self.runcmd)
        p.close()
        self.logined = 0
        
    def getindex(self):

# fetch the url            
        self.strboard = self.entryBoard.get_text().lower()
        self.strindex = self.entryIndex.get_text()
        
        if self.strboard and self.strindex.isdigit():
            strurl = smth_url + phpdoc + '?board=' + self.strboard + '&start=' + self.strindex
            fh = urllib.urlopen(strurl)
            str = fh.read()
            fh.close()
            str = str.lower()
            restr1 = '<td class="t3">' + self.strindex + '</td>'
            restr2 = 'board=' + self.strboard + '&id=\d+'
            p1 = re.compile('<td class="t3">\d+</td>')
            p2 = re.compile(restr2)
            list1 = p1.findall(str)
            list2 = p2.findall(str)
            if list2:
# split it and get the index
                try:
                    self.numindex = list2[list1.index(restr1)].split('=')[2]
                except: 
                    self.numindex = ''
        
    def update_cb(self, widget, data=None):
        self.getindex()
        self.login()
        
# fetch the URL
        print self.numindex
        if self.numindex and self.strboard:
# http://proxy.smth.org/bbspst.php?board=LinuxApp&reid=129508        
            self.runcmd = CURL + ' -A ' + userAgent \
                + ' "' + smth_url + phppost + '?board=' + self.entryBoard.get_text() \
                + '&reid=' + self.numindex + '" ' \
                + ' -b ' + cookie
            p = os.popen(self.runcmd)
            rawdata = p.read()
            p.flush()
            p.close()
            parser = TextExtracter()
            parser.feed(rawdata)
            parser.close()
            
# convert them to utf8 in a stupid way            
            fh = open(tmpfile, 'w')
            if fh:
                fh.write(parser.textarea)
                fh.close()
                self.runcmd = 'cat ' + tmpfile + ' | ' + ICONV + ' -f gbk -t utf8'
                p = os.popen(self.runcmd)
                self.replytext = p.read()
                p.close()
# update the GUI                
                self.textbuffer.insert_at_cursor(self.replytext)
                
            fh = open(tmpfile, 'w')
            if fh:
                fh.write(parser.title[0])
                fh.close()
                self.runcmd = 'cat ' + tmpfile + ' | ' + ICONV + ' -f gbk -t utf8'
                p = os.popen(self.runcmd)
                self.titletext = p.read()
                p.close()
# update the GUI
                self.entryTitle.set_text(self.titletext)
            
            
    def send_cb(self, widget, data=None):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        mystr = self.textbuffer.get_text(start, end, gtk.TRUE)
        mytitle = self.entryTitle.get_text()
        myboard = self.entryBoard.get_text()
        tmpfileu = tmpfile + '.utf8'
        tmpfilet = tmpfile + '.title'
        myindex = self.entryIndex.get_text()

        if mytitle and myboard and mystr:
            self.fh = open(tmpfileu, 'w')
            if self.fh:
                self.fh.write(mystr)
                self.fh.flush()
                self.fh.close()
                self.runcmd = ICONV + ' -f utf8 -t gbk < ' + tmpfileu + ' >' + tmpfile
                p = os.popen(self.runcmd)
                p.close()

            self.fh = open(tmpfileu, 'w')
            if self.fh:
                self.fh.write(mytitle)
                self.fh.flush()
                self.fh.close()
                self.runcmd = ICONV + ' -f utf8 -t gbk < ' + tmpfileu + ' >' + tmpfilet
                p = os.popen(self.runcmd)
                p.close()
                
# login  
            self.login()    

# upload the files
            s = self.filename.get_text().split(';')
            i = 0
            while s[i] != '' :
                if os.path.isfile(s[i]):
                    self.runcmd = CURL + ' -A ' + userAgent \
                        + ' -F ' + '"attachfile=@' + s[i] + ';type=application/binary" ' \
                        + ' "' + smth_url + phpupload + '?act=add"' \
                        + ' -b ' + cookie
#                    print self.runcmd
                    p = os.popen(self.runcmd)
#                    print p.read()
                    p.close()
                i += 1
            
# post article
            mysig = ''
            if usesignature:
                mysig = ' -F "signature=' + usesignature + '" '
#            print mysig
            
            print myindex
            print self.numindex
            if myindex.isdigit() and not self.numindex:
                self.getindex()
#                print self.numindex
#            else:
#                print "no update..."
#                print self.numindex

            if self.numindex and myindex.isdigit():
                self.runcmd = CURL + ' -A ' + userAgent \
                    + ' -F "title=<' + tmpfilet + '" ' \
                    + ' -F "text=<' + tmpfile + '" ' \
                    + mysig + ' "' + smth_url + phpsend + '?board=' + myboard \
                    + '&reid=' + self.numindex + '" ' \
                    + ' -b ' + cookie
            else:            
                self.runcmd = CURL + ' -A ' + userAgent \
                    + ' -F "title=<' + tmpfilet + '" ' \
                    + ' -F "text=<' + tmpfile + '" ' \
                    + mysig + smth_url + phpsend + '?board=' + myboard \
                    + ' -b ' + cookie
                    
#            print self.runcmd
            p = os.popen(self.runcmd)
            p.close()
# logout
        self.logout()
        
        self.window.hide()
        gtk.main_quit()
        return gtk.FALSE

    def cancel_cb(self, widget, data=None):
        if self.logined:
            self.logout()
        self.window.hide()
        gtk.main_quit()

    def file_cb(self, widget, data=None):
        self.filesel = gtk.FileSelection("Select A File...")
        self.filesel.connect("destroy", self.destroy)
        self.filesel.ok_button.connect("clicked", self.file_ok_sel)
        self.filesel.cancel_button.connect_object("clicked",
                                self.destroy, self.filesel)
        self.filesel.show()
    
    def destroy(self, w):
        self.filesel.hide()

    def msg_ok(self, w, data=None):
        return

    def file_ok_sel(self, w):
        filename = self.filesel.get_filename()
        self.filesel.hide()
        list = self.filename.get_text()
        list = list + filename + ";"
        self.filename.set_text(list)

    def __init__(self):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(gtk.FALSE)

        self.window.connect("delete_event", self.delete_event)
        self.window.set_title("SMTH Post It!")
        self.window.set_border_width(0)
        self.window.set_default_size(500, 300)
        self.window.set_position(1)
        self.window.grab_focus()
        self.window.set_border_width(5)
        self.vbox = gtk.VBox(gtk.FALSE, 0)
        self.window.add(self.vbox)
        self.vbox.show()
        self.table = gtk.Table(10, 8, gtk.TRUE)

        self.label1 = gtk.Label("æ ‡é¢˜")
        self.label2 = gtk.Label("è®¨è®ºåŒº")
        self.table.attach(self.label1, 0, 1, 0, 1)
        self.entryTitle = gtk.Entry()
        self.table.attach(self.entryTitle, 1, 5, 0, 1)
        self.entryTitle.show()
        self.entryBoard = gtk.Entry()
        self.table.attach(self.label2, 5, 6, 0, 1)
        self.table.attach(self.entryBoard, 6, 8, 0, 1)
        self.label1.show()
        self.label2.show()
        boardname = qterm.getText(lp, 0)
        if boardname:
            s1 = boardname.split('[')
            if s1[0] != boardname and s1[1]:
                s2 = s1[1].split(']')
                self.entryBoard.set_text(s2[0])
       
        self.entryBoard.show()
        self.vbox.pack_start(self.table, gtk.TRUE, gtk.TRUE, 0)
                
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.sw.add(self.textview)

        self.table.attach(self.sw, 0, 8, 1, 8)

        self.sw.show()
        self.textview.show()
        self.table.show()
        
        self.filedialog = gtk.Button("Open", gtk.STOCK_OPEN)
        self.senddata = gtk.Button("Send", gtk.STOCK_PASTE)
        self.cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        self.label10 = gtk.Label("æ–‡ç« å·")
        self.updatecontent = gtk.Button("æ›´æ–°å¼•è¨€_U")
        self.entryIndex = gtk.Entry()
        self.filename = gtk.Entry()
        self.table.attach(self.filename, 0, 7, 8, 9)
        self.table.attach(self.filedialog, 7, 8, 8, 9)
        
        self.table.attach(self.label10, 0, 1, 9, 10)
        self.table.attach(self.entryIndex, 1, 3, 9, 10)
        self.table.attach(self.updatecontent, 3, 4, 9, 10)
        self.table.attach(self.senddata, 7, 8, 9, 10)
        self.table.set_row_spacing(8, 3)
        self.table.attach(self.cancel, 6, 7, 9, 10)
        self.filename.show()
        self.filedialog.show()
        self.senddata.show()
        self.cancel.show()

        
        self.logined = 0
        self.numindex = ''
        modestr = qterm.getText(lp, 1)
        p = re.compile('\[Ctrl-P\]')
        p1 = re.compile('Ò»°ãÄ£Ê½')
        modestr1 = qterm.getText(lp, 2)
        
        self.mode = gtk.RESPONSE_YES
#        print modestr
        if p.findall(modestr) and p1.findall(modestr1):
            self.msg = gtk.Dialog('é€‰æ‹©å‘æ–‡æ¨¡å¼', self.window, gtk.DIALOG_DESTROY_WITH_PARENT, ('å‘è¡¨æ–‡ç« (_P)', gtk.RESPONSE_YES, 'å›žå¤æ–‡ç« (_R)', gtk.RESPONSE_NO))
            self.mode = self.msg.run()
            self.msg.destroy()
            
        if self.mode == gtk.RESPONSE_NO:
            self.label10.show()
            self.entryIndex.show()
            self.updatecontent.show()

# reply mode, try to fetch the id and title        
#            print 'reply article'
            line = qterm.caretY(lp)
            mystr = ''
            if line:
                modestr = qterm.getText(lp, line)
                p1 = re.compile('\d+\.\@')
                i = 0
                list = modestr.split(None, 3)
                if len(list[2]) == 1:
                    i = 1
                if not p1.findall(modestr):
                    mystr = modestr.split(None, 6 + i)[6 + i]
                else:                                
                    mystr = modestr.split(None, 5 + i)[5 + i]
                
                if list[1].isdigit() and mystr:
                    self.entryIndex.set_text(list[1])
                    self.fh = open(tmpfile, 'w')
                    if self.fh:
                        self.fh.write(mystr)
                        self.fh.flush()
                        self.fh.close()
                        self.runcmd = 'cat ' + tmpfile + ' | iconv -f gbk -t utf8'
                        self.stdout = os.popen(self.runcmd)
                        self.title = self.stdout.read()
                        if self.title:
                            self.entryTitle.set_text("Re: %s" % self.title.rstrip())
        self.window.show()

        self.filedialog.connect("clicked", self.file_cb, None)
        self.cancel.connect("clicked", self.cancel_cb, None)
        self.senddata.connect("clicked", self.send_cb, None)
        self.updatecontent.connect("clicked", self.update_cb, None)

def builtin():
    # And of course, our main loop.
    gtk.main()
    # Control returns here when main_quit() is called
    return 0
    
# if __name__ == "__main__":
if __name__ == "__builtin__":
    QPostIt()
    builtin()

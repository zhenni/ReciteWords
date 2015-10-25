import  xml.dom.minidom
import xml
from xml.dom import minidom
import codecs
import time
import os
import random

# constant
DOCNAME = 'GRE3000_learning.xml'
LOGFILE = "log/"+DOCNAME+"_"+ time.strftime('%Y-%m-%d_%H:%M:%S') +".log";
log = os.open(LOGFILE, os.O_CREAT);
is_modified = False


def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    writer.write(indent+"<" + self.tagName)
    
    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()
    
    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
            and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s"%(newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer,indent+addindent,addindent,newl)
        writer.write("%s</%s>%s" % (indent,self.tagName,newl))
    else:
        writer.write("/>%s"%(newl))

minidom.Element.writexml = fixed_writexml

def display(x, i):
    i = norm(i);
    
    os.system("clear");
    word_node = x[i].getElementsByTagName("word")[0].childNodes[0];
    phonetic_node = x[i].getElementsByTagName("phonetic")[0].childNodes[0];
    trans = x[i].getElementsByTagName("trans")[0].childNodes[0];
        
    word=word_node.nodeValue;
    phonetic=phonetic_node.wholeText;
    trans=trans.wholeText;
    
    print '\033[1;40;40m'
    print word
    print '\033[0m'
    print phonetic
    print "".join(trans.split("<br />"));
    return i;

def norm(i):
    if i < 0:
        i = x.length-1
    if i > x.length-1:
        i = 0
    return i;

def is_learned(x, i):
    if i < 0 or i > x.length-1:
        return False;
    
    learned_node = x[i].getElementsByTagName("learned")[0].childNodes[0];
    if learned_node.nodeValue == '1':
        return True;
    else:
        return False;

def set_learned(x, i):
    if i < 0 or i > x.length-1:
        return False;
    
    is_modified = True;
    learned_node = x[i].getElementsByTagName("learned")[0].childNodes[0];
    learned_node.nodeValue = '1';
    word_node = x[i].getElementsByTagName("word")[0].childNodes[0];
    log.write(word_node.nodeValue + "\t\t"+ i + "\t\t learned 0 1\n")
    return True;

def show_status(x):
    count = 0;
    for i in range(x.length):
        if is_learned(x, i) == True:
            count = count+1;
    print "#################### STATUS ######################"
    print "Learned:", count, "/", x.length, "words";
    print "Finish about ", (count/x.length*100) , "%";
    print "##################################################"

def show_help():
    os.system("clear");
    print "Hello! Welcome to Recite Words!"
    print "Author: Zhen Wei 94hazelnut@gmail.com"
    print "##################################################"
    print "q       quit or back"
    print "h       help"
    print "a or w  prev word"
    print "s or s  next word"
    print "l       delete the words that have been known well"

def save_xml():
    f = codecs.open(DOCNAME,'w','utf-8')
    dom.writexml(f,addindent='  ',newl='\n',encoding = 'utf-8')
    f.close();

def recite(x):
    for i in range (x.length):
        if is_learned(x, i) == True:
            continue;
        else:
            i = display(x, i);
            break;
    if i == x.length-1:
        print "Finished"
        return;

    cmd = getch().upper();
    while cmd != "Q":
        if cmd == "A" or cmd == "W": # recites
            i = norm(i-1);
            while is_learned(x, i) == True:
                i = norm(i-1);
            i = display(x, i)
        elif cmd == "S"or cmd == "D":
            i = norm(i+1);
            while is_learned(x, i) == True:
                i = norm(i+1);
            i = display(x, i)
        elif cmd == "L":
            if is_learned(x, i) == "0":
                set_learned(x, i);
            else:
                print "The word has arreaady been in the finished file."
        cmd = getch().upper();
    show_help();

############################ MAIN ####################################

# Parse and get the items
dom = xml.dom.minidom.parse(DOCNAME)

root = dom.documentElement
x = root.getElementsByTagName('item');

show_help();
show_status(x);

cmd = getch().upper();
while cmd != "Q":
    if cmd == "R": # recites
        recite(x);
    else:
        show_help();
    cmd = getch().upper();

# No modification remove the log
if is_modified == False:
    os.remove(LOGFILE);
else:
    save_xml()

# # add node "learned"
#    learned = dom.createElement('learned');
#    value = '0'
#   learned_value = dom.createTextNode(value)
#   learned.appendChild(learned_value)
#   x[i].appendChild(learned)

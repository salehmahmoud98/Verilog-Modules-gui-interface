# import tkinter module
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

names = []
tests = []
widths = []
types = []


verilog_reserved_words = [
        'always', 'and', 'assign', 'automatic', 'before', 'begin', 'buf', 'bufif0', 'bufif1',
        'case', 'casex', 'casez', 'cmos', 'deassign', 'default', 'defparam', 'disable', 'edge',
        'else', 'end', 'endcase', 'endfunction', 'endmodule', 'endprimitive', 'endspecify', 'endtable',
        'endtask', 'event', 'for', 'force', 'forever', 'fork', 'function', 'highz0', 'highz1',
        'if', 'ifnone', 'initial', 'inout', 'input', 'integer', 'join', 'large', 'localparam',
        'macromodule', 'medium', 'module', 'nand', 'negedge', 'nmos', 'nor', 'not', 'notif0',
        'notif1', 'or', 'output', 'parameter', 'pmos', 'posedge', 'primitive', 'pull0', 'pull1',
        'pulldown', 'pullup', 'rcmos', 'real', 'realtime', 'reg', 'release', 'repeat', 'rnmos',
        'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared', 'small', 'specify', 'specparam',
        'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time', 'tran', 'tranif0',
        'tranif1', 'tri', 'tri0', 'tri1', 'triand', 'trior', 'trireg', 'vectored', 'wait',
        'wand', 'wor', 'while', 'wire', 'wor', 'xnor', 'xor']


def valid_name(List):
    x = ord(List[0])
    
    if( (x < 65 or (x > 90 and x < 97) or x > 122) and (x != 95) ):
        return False
    
    for i in List:
        n = ord(i)
        if( (n < 65 or (n > 90 and n < 97) or n > 122) and (n != 95) and (n < 48 or n > 57)):
            return False
        
    return True

def findname(List, Searched_Name):
    for i in range(len(List)):
        if (List[i] == Searched_Name):
            return i
    return -1

def isbin(Str):
 
    p = set(Str)
 
    s = {'0', '1'}
 
    if s == p or p == {'0'} or p == {'1'}:
        return True
    else:
        return False


def going():
	name = ee1.get().strip()
	Type = ee2.get()
	clk_type = ee3.get()
	syn_type = ee4.get()

	if(len(name) > 0 and valid_name(name) and (name not in verilog_reserved_words) ):
		global module_name
		module_name = name
		global type_
		type_ = "1" if (Type == "combinational") else "2"
		global edge_type
		edge_type = "1" if (clk_type == "pos edge") else "2"
		global reset
		reset = "0" if(syn_type == "no reset") else "1" if(syn_type == "Asynchronous positive") else "2" if(syn_type == "Asynchronous negative") else "3" if(syn_type == "Synchronous positive") else "4"
		if(type_ == "2"):
			names.append("clk")
			widths.append(1)
			types.append("input")
		else:
			reset = "5"
			edge_type = "3"
		if(reset == "1" or reset == "3"):
			names.append("rst")
			widths.append(1)
			types.append("input")
		elif(reset == "2" or reset == "4"):
			names.append("rst_n")
			widths.append(1)
			types.append("input")
		print("reset : ", reset, "clock: ", edge_type)
		root.deiconify()
		root0.destroy()

	else:
		messagebox.showerror(title = "Error", message = "Invalid module name")


def Add_clicked():
	name = e2.get().strip()
	Type = e1.get()
	wd = e3.get().strip()

	if(len(name) > 0 and valid_name(name) and (name not in names) and (name not in verilog_reserved_words) and wd.isdigit() and (int(wd) > 0) ):
		names.append(name)
		types.append(Type)
		widths.append(int(wd))
		tree.insert('', END, values = (name, Type, int(wd)))
	else:
		messagebox.showerror(title = "Error", message = "Invalid port name or Invalid width")


def delete_selected():
	val = tree.item(tree.selection())
	record = val['values']
	if(len(record) > 0):
		name_ = record[0]
		index = names.index(name_)
		names.pop(index)
		widths.pop(index)
		types.pop(index)
		tree.delete(tree.selection())
		print("\nDeleted successfuly!")

def create():

	filename = module_name + ".v"

	f = open(filename, "w")

	text = "module " + module_name + "(\n"

	l = len(names)

	for i in range(l - 1):
		if(widths[i] != 1):
			m = "\t" + types[i] + " " + "[" + str(widths[i] -1) + ":0] " + names[i] + ",\n"
		else:
			m = "\t" + types[i] + " " + names[i] + ",\n"
		text += m

	if(widths[l-1] != 1):
		m = "\t" + types[l-1] + " " + "[" + str(widths[l-1] -1) + ":0] " + names[l-1] + ");\n\n\n"
	else:
		m = "\t" + types[l-1] + " " + names[l-1] + ");\n\n\n"

	text += m

	if(type_ == "1"):
		m = "\talways @(*) begin\n\n\t\t//your code goes here\n\n\tend\n\nendmodule"
		text += m

	else:

		edge       = "posedge"  if(edge_type == "1")  else "negedge"
		reset_edge = "posedge " if(reset == "1")      else "negedge "

		if(reset =="0"):
			m = "\talways @(" + edge + " clk) begin\n\n\t\t//your code goes here\n\n\tend\n\nendmodule"
			text += m

		else: 
			if(reset == "1" or reset == "2"):
				m = "\talways @(" + edge + " clk or " + reset_edge + names[1] + ") begin\n\n"
			else:
				m = "\talways @(" + edge + " clk) begin\n\n"
		    
			text += m

			if(reset == "1" or reset == "3"):
				rst = "\n\t\tif(" + names[1] + ") begin\n\n\t\t\t//Reset condition\n\n\t\tend\n\t\telse begin\n\n\t\t\t//Non-reset condition\n\n\t\tend\n\tend\n\nendmodule"
			else:
				rst = "\n\t\tif(!" + names[1] + ") begin\n\n\t\t\t//Reset condition\n\n\t\tend\n\t\telse begin\n\n\t\t\t//Non-reset condition\n\n\t\tend\n\tend\n\nendmodule"
			text += rst

	f.write(text)
	f.close()

	print("Done implementing!")           


# creating main tkinter window/toplevel
root0 = Tk()

root0.title("Configure Module")

# chaning window icon
#root0.iconbitmap("icon.ico")

#message = Tk()

# this will create a label widget
ll0 = Label(root0, text = "Choose module Name and properties : ", font = "Times 16")
ll1 = Label(root0, text = "Name:")
ll2 = Label(root0, text = "com or seq:")
ll3 = Label(root0, text = "clk type:")
ll4 = Label(root0, text = "reset type:")

# grid method to arrange labels in respective
# rows and columns as specified
ll0.grid(row = 0, column = 0, sticky = W, pady = 2)
ll1.grid(row = 1, column = 0, sticky = W, pady = 2)
ll2.grid(row = 2, column = 0, sticky = W, pady = 2)
ll3.grid(row = 3, column = 0, sticky = W, pady = 2)
ll4.grid(row = 4, column = 0, sticky = W, pady = 2)


# entry widgets, used to take entry from user

ee1 = Entry(root0)
ee2 = Combobox(root0, state="readonly", values = ["combinational", "sequential"])
ee2.current(0)
ee3 = Combobox(root0, state="readonly", values = ["pos edge", "neg edge"])
ee3.current(0)
ee4 = Combobox(root0, state="readonly", values = ["no reset", "Asynchronous positive", "Asynchronous negative", "Synchronous positive", "Synchronous negative"])
ee4.current(0)

# this will arrange entry widgets
ee1.grid(row = 1, column = 0, pady = 2)
ee2.grid(row = 2, column = 0, pady = 2)
ee3.grid(row = 3, column = 0, pady = 2)
ee4.grid(row = 4, column = 0, pady = 2)

bb1 = Button(root0, text = "Go", command = going)

# arranging button widgets
bb1.grid(row = 5, column = 0, sticky = W)


#message.title("hello")




root = Tk()

root.title("Verilog App")

# chaning window icon
#root.iconbitmap("icon.ico")

# this will create a label widget
l0 = Label(root, text = "Add variables : ", font = "Times 16")
l1 = Label(root, text = "type")
l2 = Label(root, text = "Name")
l3 = Label(root, text = "Width")

# grid method to arrange labels in respective
# rows and columns as specified
l0.grid(row = 0, column = 0, sticky = W, pady = 2)
l1.grid(row = 1, column = 0, sticky = W, pady = 2)
l2.grid(row = 2, column = 0, sticky = W, pady = 2)
l3.grid(row = 3, column = 0, sticky = W, pady = 2)

v0 = StringVar(root)
v0.set("A") # default value

v1 = StringVar(root)
v1.set("1") # default value


# entry widgets, used to take entry from user
e1 = Combobox(root, state="readonly", values = ["input", "output", "inout"])
e1.current(0)
e2 = Entry(root)
e3 = Entry(root)
e3.insert(0, "1") 

# this will arrange entry widgets
e1.grid(row = 1, column = 0, pady = 2)
e2.grid(row = 2, column = 0, pady = 2)
e3.grid(row = 3, column = 0, pady = 2)

# checkbutton widget
#c1 = Checkbutton(root, text = "Preserve")
#c1.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# adding image (remember image should be PNG and not JPG)
#img = PhotoImage(file = r"image.png")
#img1 = img.subsample(2, 2)

# setting image with the help of label
#Label(root, image = img1).grid(row = 0, column = 2, columnspan = 2, rowspan = 2, padx = 5, pady = 5)





columns = ('variable_name', 'type', 'bus_width')

tree = Treeview(root, columns=columns, show='headings')

# define headings
tree.heading('variable_name', text='Variable Name')
tree.heading('type', text='Type')
tree.heading('bus_width', text='Bus width')

scrollbar = Scrollbar(root, orient = VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)



tree.grid(row=4, column=0, columnspan = 2, pady = 5, sticky='nsew')
scrollbar.grid(row=4, column=2, pady = 5, sticky='ns')


# button widget
b1 = Button(root, text = "Add", command = Add_clicked)
b2 = Button(root, text = "Delete", command = delete_selected)

# arranging button widgets
b1.grid(row = 5, column = 0, sticky = W)
b2.grid(row = 5, column = 1, sticky = W)

b3 = Button(root, text = "Create Module", command = create)

b3.grid(row = 6, column = 0, sticky = W, pady = 10)

root.withdraw()
# infinite loop which can be terminated 
# by keyboard or mouse interrupt
mainloop()


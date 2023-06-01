import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import Cdma as cdma
x = []
y = []

x1 = []
y1 = []

x2 = []
y2 = []

win = tk.Tk()
def make_menu(w):
    global the_menu
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

def Start ():    
    make_menu(win)
    win.title("CDMA Simulator")
    # drop down menu
    ttk.Label(win, text="Choisissez le nombre d'utilisateur:").grid(column=0, row=0)
    number = tk.StringVar()
    numberChosen = ttk.Combobox(win, width=12, textvariable=number) 
    numberChosen['values'] = (1, 2)
    numberChosen.current(1)
    numberChosen.grid(column=0, row=1)

    #Slider    
    ttk.Label(win, text="Niveau de bruit").grid(column=0, row=2)
    slider = tk.Scale(win, from_=0, to=100,tickinterval=10,length =300,width =10,orient="horizontal")
    slider.set(20)
    slider.grid(column=1, row=2, sticky=tk.W, columnspan=2)
    
    # scrolled text
    ttk.Label(win, text="Message 1:").grid(column=0, row=4)
    msg_1 = scrolledtext.ScrolledText(win, width=30, height=3, wrap=tk.WORD)
    msg_1.grid(column=0, row=5, sticky='WE', columnspan=3)
    # scrolled text
    ttk.Label(win, text="Message 2:").grid(column=0, row=6)
    msg_2 = scrolledtext.ScrolledText(win, width=30, height=3, wrap=tk.WORD)
    msg_2.grid(column=0, row=7, sticky='WE', columnspan=3 )
    if(numberChosen.get() == 1):
        msg_2.configure(state="disabled")
        # button
    action = ttk.Button(win, text="Start", command= lambda: Start_simulation(numberChosen.get(), slider.get()/100, msg_1.get('1.0', 'end-1c'), msg_2.get('1.0', 'end-1c')))
    action.grid(column=2, row=8)
    
    

def Start_simulation(nombre_users, bruit, msg_1, msg_2):
    # action.configure(text='Start')
    # print('=========== Start simulation ===========')
    # print('Nombre d utilisateurs: '+nombre_users)
    # # nois = 'Oui' if bruit == 1 else 'Non'
    # print('Bruit: '+str(bruit))

    # print('Message 1: '+msg_1)
    # print('Message 2: '+msg_2)

    #Cas 1 user
    if nombre_users =='1':
        #saving input as bits for BER analysis 
        input_1 = cdma.binaire_to_ternaire(cdma.text_to_bits(msg_1))

        Encoded_Volt = cdma.User_sending(msg_1,cdma.Key_1)
        if (bruit > 0):
            Traffic = cdma.Multiplexing(Encoded_Volt ,cdma.Noise_Generator(len(Encoded_Volt),bruit ))
        else : Traffic = Encoded_Volt
    #Cas 2 users
    elif (nombre_users == '2'): 
        #saving input as bits for BER analysis 
        input_2_1 = cdma.binaire_to_ternaire(cdma.text_to_bits(msg_1))
        input_2_2 = cdma.binaire_to_ternaire(cdma.text_to_bits(msg_2))
     
        Encoded_Volt_1 = cdma.User_sending(msg_1,cdma.Key_1)
        Encoded_Volt_2 = cdma.User_sending(msg_2,cdma.Key_2 )
        #saving the lengths
        long1,long2=len(Encoded_Volt_1),len(Encoded_Volt_2)
        if (bruit > 0):
            Traffic = cdma.Multiplexing(cdma.Multiplexing(Encoded_Volt_1,Encoded_Volt_2),cdma.Noise_Generator(max(len(Encoded_Volt_1),len(Encoded_Volt_2)),bruit))
        else : Traffic = cdma.Multiplexing(Encoded_Volt_1,Encoded_Volt_2)
  

    #reception
    if nombre_users== '1':
        Reception=cdma.Decoder_1(Traffic,cdma.Key_1)
        print("Reception")
        #Back to Text 
        # try :
        #     print (cdma.Back_to_text(Reception))
        # except:
        #     print ("Erreurs dans la reconversion en ASCII")
       
        cdma.BER(input_1,Reception)
        x.append(len(input_1))
        y.append(cdma.BER(input_1,Reception))
        print (x)
        print (y)

    elif nombre_users== '2':
        Reception_1 = cdma.Decoder_1(Traffic[:long1],cdma.Key_1)
        Reception_2 = cdma.Decoder_1(Traffic[:long2],cdma.Key_2)
        print("Reception 1")
        x1.append(len(input_2_1))
        y1.append(cdma.BER(input_2_1,Reception_1))
        print (x1)
        print (y1)     
          
        # cdma.BER(input_2_1,Reception_1)
        print("==============")
        print("Reception 2")
        # try :
        #     print(cdma.Back_to_text(Reception_2))
        # except:
        #     print ("Erreur dans la reconversion en ASCII")
        #cdma.BER(input_2_2,Reception_2)
        x2.append(len(input_2_2))
        y2.append(cdma.BER(input_2_2,Reception_2))
        print (x2)
        print (y2)  
 
if __name__ == '__main__':
    Start() 
    win.mainloop()
import os


pic_list = os.listdir("pics/")
sound_list = os.listdir("audio/")

def f_pic_name_list():
    pic_name_list = ["!"+e[:-4] for e in pic_list]
    return (pic_name_list)

def f_sound_name_list():
    sound_name_list = ["!"+e[:-4] for e in sound_list]
    return (sound_name_list)
import os

def handleCommand(command, keyPosition):
    #fblr

    print("\n\n\n")

    if keyPosition != "down":
        return

    if command == 'F':
        print("onforward")
        os.system("cd v4l2scripts ; ./onforward.sh")

    if command == 'B':
        print("onback")
        os.system("cd v4l2scripts; ./onback.sh")

    if command == 'L':
        print("onleft")
        os.system("cd v4l2scripts; ./onleft.sh")

    if command == 'R':
        print("onright")
        os.system("cd v4l2scripts; ./onright.sh")

    if command == 'focus+':
        print("onfocus+")
        os.system("cd v4l2scripts; ./onfocus+.sh")

    if command == 'focus-':
        print("onfocus-")
        os.system("cd v4l2scripts; ./onfocus-.sh")

    if command == 'foc+':
        print("onfocus+")
        os.system("cd v4l2scripts; ./onfocus+.sh")

    if command == 'foc-':
        print("onfocus-")
        os.system("cd v4l2scripts; ./onfocus-.sh")

    if command == 'zoom+':
        print("onzoom+")
        os.system("cd v4l2scripts; ./onzoom+.sh")

    if command == 'zoom-':
        print("onzoom-")
        os.system("cd v4l2scripts; ./onzoom-.sh")

    if command == 'brt+':
        print("onbrt+")
        os.system("cd v4l2scripts; ./onbrt+.sh")

    if command == 'brt-':
        print("onbrt-")
        os.system("cd v4l2scripts; ./onbrt-.sh")

    if command == 'con+':
        print("oncon+")
        os.system("cd v4l2scripts; ./oncon+.sh")

    if command == 'con-':
        print("oncon-")
        os.system("cd v4l2scripts; ./oncon-.sh")

    if command == 'sat+':
        print("onsat+")
        os.system("cd v4l2scripts; ./onsat+.sh")

    if command == 'sat-':
        print("onsat-")
        os.system("cd v4l2scripts; ./onsat-.sh")

    if command == 'gain+':
        print("ongain+")
        os.system("cd v4l2scripts; ./ongain+.sh")

    if command == 'gain-':
        print("ongain-")
        os.system("cd v4l2scripts; ./ongain-.sh")

    if command == 'temp+':
        print("ontemp+")
        os.system("cd v4l2scripts; ./ontemp+.sh")

    if command == 'temp-':
        print("ontemp-")
        os.system("cd v4l2scripts; ./ontemp-.sh")

    if command == 'sharp+':
        print("onsharp+")
        os.system("cd v4l2scripts; ./onsharp+.sh")

    if command == 'sharp-':
        print("onsharp-")
        os.system("cd v4l2scripts; ./onsharp-.sh")

    if command == 'exp+':
        print("onexp+")
        os.system("cd v4l2scripts; ./onexp+.sh")

    if command == 'exp-':
        print("onexp-")
        os.system("cd v4l2scripts; ./onexp-.sh")

    if command == 'pan+':
        print("onpan+")
        os.system("cd v4l2scripts; ./onpan+.sh")

    if command == 'pan-':
        print("onpan-")
        os.system("cd v4l2scripts; ./onpan-.sh")

    if command == 'tilt+':
        print("ontilt+")
        os.system("cd v4l2scripts; ./ontilt+.sh")

    if command == 'tilt-':
        print("onexp-")
        os.system("cd v4l2scripts; ./ontilt-.sh")

    if command == 'atemp':
        print("onatemp")
        os.system("cd v4l2scripts; ./onatemp.sh")

    if command == 'backlight':
        print("onbaclight")
        os.system("cd v4l2scripts; ./onbacklight.sh")

    if command == 'aexp':
        print("onaexp")
        os.system("cd v4l2scripts; ./onaexp.sh")

    if command == 'aexppri':
        print("onaexppri")
        os.system("cd v4l2scripts; ./onaexppri.sh")

    if command == 'afoc':
        print("onafoc")
        os.system("cd v4l2scripts; ./onafoc.sh")

    #print("handle command", command, keyPosition)

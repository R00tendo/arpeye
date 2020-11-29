import socket
import os
import subprocess
import time
import threading
import shutil

rounda = 0
up = []


def ping1():
    global rounda
    while True:
        if rounda > 255:
            print("end")
            exit()
        currant = rounda
        proc = subprocess.Popen(["ping", "-n", "1", "-w", "1", "192.168.1." + str(currant)], stdout=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        if "timed out" in str(out):
            print(rounda)
            pass
        else:
            print("Host: " + "192.168.1." + str(currant))
            up.append("192.168.1." + str(currant))

        rounda = rounda + 1


def ping2():
    global rounda
    while True:
        if rounda > 255:
            print("end")
            exit()
        currant = rounda
        proc = subprocess.Popen(["ping", "-n", "1", "-w", "1", "192.168.1." + str(currant)], stdout=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        if "timed out" in str(out):
            pass
        else:
            print("Host: " + "192.168.1." + str(currant))
            up.append("192.168.1." + str(currant))

        rounda = rounda + 1


def ping3():
    global rounda
    while True:
        if rounda > 255:
            print("end")
            exit()
        currant = rounda
        proc = subprocess.Popen(["ping", "-n", "1", "-w", "1", "192.168.1." + str(currant)], stdout=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        if "timed out" in str(out):
            pass
        else:
            print("Host: " + "192.168.1." + str(currant))
            up.append("192.168.1." + str(currant))

        rounda = rounda + 1


def ping4():
    global rounda
    while True:
        if rounda > 255:
            print("end")
            contas()
        currant = rounda
        proc = subprocess.Popen(["ping", "-n", "1", "-w", "1", "192.168.1." + str(currant)], stdout=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        if "timed out" in str(out):
            pass
        else:
            print("Host: " + "192.168.1." + str(currant))
            up.append("192.168.1." + str(currant))

        rounda = rounda + 1


def contas():
    global up, banner
    for i in range(len(up)):
        proc = subprocess.Popen(["ping", "-n", "1", "-w", "1", "192.168.1." + str(up[i])], stdout=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        if "timed out" in str(out):
            up.remove(str(up[i]))
            print("false positive in: " + str(up[i]))
        else:
            pass
    os.system("cls")
    print("Up:")
    for i in range(len(up)):
        print("Host: " + str(up[i]))

    print("starting scans...")
    for i in range(len(up)):
        os.system("mkdir " + str(up[i]))
        os.chdir(str(up[i]))
        proc = subprocess.Popen(["nmap", "-sV", str(up[i]), ">", str(up[i]) + ".txt"], stdout=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        print(out.decode())
        os.chdir("..")
    print("Nmap done, dumping hostname...")
    for i in range(len(up)):
        try:
            host = socket.gethostbyaddr(up[i])
            os.chdir(up[i])
            os.system("echo " + str(host) + " > domain-" + str(up[i]) + ".txt")
            os.chdir("..")
        except:
            print("Could not resolve ip: " + str(up[i]))
            pass
    print("resolve done, starting vuln scan")
    for i in range(len(up)):
        os.chdir(str(up[i]))
        proc = subprocess.Popen(
            ["nmap", "-sC", "-O", "-A", "--script", "vulners", str(up[i]), ">", "vulns-" + str(up[i]) + ".txt"],
            stdout=subprocess.PIPE,
            shell=True)
        (out, err) = proc.communicate()
        print(out.decode())
        os.chdir("..")
    print("done, starting website scan")
    for i in range(len(up)):
        os.chdir(str(up[i]))
        ports = open(str(up[i]) + ".txt", "r")
        all = ports.readlines()
        ports.close()
        start = []
        for line in all:
            kola = line.find(" open")
            if kola > 1:
                porttest = line.split("/")
                start.append(porttest[0])
        print("\n\n" + str(up[i]))
        print("__________________________________________________________________________")
        for cc in range(len(start)):
            if start[cc] == "443":
                print("Port 443 is open so there's a web interface.")
            else:
                if start[cc] == "80":
                    print("Port 80 is open so there's a web interface.")
                else:
                    if int(start[cc]) < 80:
                        print("Port " + start[cc] + " doesnt have web interface.")
                    else:
                        if int(start[cc]) > 1000:
                            print("Port " + start[cc] + " might have web interface.")
                        else:
                            print("port " + start[cc] + " state unknown")

        os.chdir("..")
    print("all scans done")

    os.mkdir("arpeye-output")
    for i in range(len(up)):
        shutil.move(str(up[i]), "arpeye-output")
    print("Done")
    exit()


if __name__ == "__main__":
    a = threading.Thread(target=ping1)
    a2 = threading.Thread(target=ping2)
    a3 = threading.Thread(target=ping3)
    a4 = threading.Thread(target=ping4)
    a2.start()
    a.start()
    a3.start()
    a4.start()

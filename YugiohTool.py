#!/usr/bin/python
# coding:utf-8

"""
@author: zyatom
@contact: 70906346@qq.com
@software: PyCharm
@file: YugiohTool.py
@time: 2020/4/21 20:50
"""
import importlib
import msvcrt
import os
import sys
import time
import win32gui
import threading
import inspect
import ctypes
import configparser

import requests

from YugiohToolSteam import Steam
from YugiohToolMoniqi import Moniqi
from YugiohToolErrorSteam import ErrorSteam
from YugiohToolErrorMoniqi import ErrorMoniqi
from YugiohToolRebootSteam import RebootSteam
from YugiohToolRebootMoniqi import RebootMoniqi
from regist import regist as reg

importlib.reload(sys)
tuisong_time = None

try:
	temp = ctypes.windll.LoadLibrary('opencv_videoio_ffmpeg420_64.dll')

except:
	pass


def _async_raise(tid, exctype):  # 关闭线程
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):  # 关闭线程
	_async_raise(thread.ident, SystemExit)


def tuisong(cishu, text, serviceapi):  # 推送到手机
	api = serviceapi
	title = "脚本运行" + str(cishu) + "次" + "，" + text
	content = text
	data = {
		"text": title,
		"desp": content
	}
	requests.post(api, data=data)


def tuisongfunction(endTime):
	global tuisong_time
	cf = configparser.ConfigParser()
	cf.read("config.ini")  # 读取配置文件
	count = int(cf.get("config", "count"))
	start_count = count
	start_time = time.time()
	serviceapi = cf.get("config", "serviceapi")
	filename = "config.ini"  # 监控配置文件改动
	while True:
		time.sleep(10)
		cf.read("config.ini")  # 读取配置文件
		info = os.stat(filename)
		count = int(cf.get("config", "count"))
		scount = int(cf.get("config", "scount"))
		if int(str(time.localtime().tm_min)[-1]) is 0:
			# 文件没有改动超过10分钟且运行时间超过10分钟微信推送提醒
			if time.time() - info.st_mtime > 590 and time.time() - start_time > 590:
				if tuisong_time is None or time.time() - tuisong_time > 60:  # 防止重复推送
					count_per_hour = count - start_count
					tuisong(count_per_hour, "脚本异常，重启游戏中...", serviceapi)
					tuisong_time = time.time()
					start_count = count
					reboot()
			# 整点发送推送
			if int(str(time.localtime().tm_min)) == 00:
				if time.time() - info.st_mtime < 600:
					if tuisong_time is None or time.time() - tuisong_time > 60:  # 防止重复推送
						count_per_hour = count - start_count
						start_count = count
						tuisong(count_per_hour, "一切正常！", serviceapi)
						tuisong_time = time.time()
		if endTime is not None:
			seconds = endTime - time.time()
			# m, s = divmod(seconds, 60)
			# h, m = divmod(m, 60)
			# print("%d:%02d:%02d" % (h, m, s))
			if seconds <= 60 or scount == 1:
				print("试用时间已到")
				print("觉得好用的话请联系我购买完整版")
				print("一分钟后脚本自动关闭...")
				cf.set('config', 'scount', '1')
				cf.write(open("config.ini", 'w'))
				time.sleep(60)
				stop_thread(t_main)
				sys.exit()

		else:
			pass


def reboot():
	steam = u'Yu-Gi-Oh! DUEL LINKS'  # steam
	moniqi = u'雷电模拟器'  # 模拟器
	hwnd_steam = win32gui.FindWindow(0, steam)  # 取得窗口句柄
	hwnd_moniqi = win32gui.FindWindow(0, moniqi)  # 取得窗口句柄
	if hwnd_steam:
		RebootSteam(steam).rebootsteam()
	elif hwnd_moniqi:
		RebootMoniqi(moniqi).rebootmoniqi()


def error():
	steam = u'Yu-Gi-Oh! DUEL LINKS'  # steam
	moniqi = u'雷电模拟器'  # 模拟器
	hwnd_steam = win32gui.FindWindow(0, steam)  # 取得窗口句柄
	hwnd_moniqi = win32gui.FindWindow(0, moniqi)  # 取得窗口句柄
	if hwnd_steam:
		ErrorSteam(steam).errorsteam()
	elif hwnd_moniqi:
		ErrorMoniqi(moniqi).errormoniqi()


def main(mode):
	steam = u'Yu-Gi-Oh! DUEL LINKS'  # steam
	moniqi = u'雷电模拟器'  # 模拟器
	hwnd_steam = win32gui.FindWindow(0, steam)  # 取得窗口句柄
	hwnd_moniqi = win32gui.FindWindow(0, moniqi)  # 取得窗口句柄
	if hwnd_steam:
		while True:
			print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ １、ｐｖｐＫＣ杯自杀　　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ２、ｐｖｐ排名决斗自杀　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ３、ｐｖｐ休闲决斗自杀　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ４、自动十级门　　　　　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ５、ｐｖｐ休闲决斗战斗　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ６、ｐｖｐ排名决斗战斗　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ７、最新掷骰子活动全自动            　　　　　　　　　　 ")
			print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("◎◎◎◎◎请输入要选择的功能前面的数字并回车◎◎◎◎◎")
			print("重要说明:近期KC杯官方严查,请勿长时间用模拟器挂机!!!")
			input1 = str(input(""))
			if input1 == '1' or input1 == '2' or input1 == '3':
				demo = Steam(steam, mode)
				demo.pvp_tolose_steam(input1)
				sys.exit()
			elif input1 == '4':
				demo = Steam(steam, mode)
				demo.chuansongmen_steam()
				sys.exit()
			elif input1 == '5' or input1 == '6':
				demo = Steam(steam, mode)
				demo.pvp_towin_steam(input1)
				sys.exit()
			elif input1 == '7':
				demo = Steam(steam, mode)
				demo.huodong_zhitouzi_steam()
				sys.exit()
			else:
				print("!!!!!输入有误,请重新输入!!!!!")
				time.sleep(1)
	elif hwnd_moniqi:
		while True:
			print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ １、ｐｖｐＫＣ杯自杀　　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ２、ｐｖｐ排名决斗自杀　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ３、ｐｖｐ休闲决斗自杀　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ４、自动十级门　　　　　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ５、ｐｖｐ休闲决斗战斗　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ６、ｐｖｐ排名决斗战斗　　　　　　　　　　　　　　　　　　　")
			print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("┃ ７、最新掷骰子活动全自动            　　　　　　　　　　 ")
			print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
			print("◎◎◎◎◎请输入要选择的功能前面的数字并回车◎◎◎◎◎")
			print("重要说明:近期KC杯官方严查,请勿长时间用模拟器挂机!!!")
			input1 = str(input(""))
			if input1 == '1' or input1 == '2' or input1 == '3':
				demo = Moniqi(moniqi, mode)
				demo.pvp_tolose_moniqi(input1)
				sys.exit()
			elif input1 == '4':
				demo = Moniqi(moniqi, mode)
				demo.chuansongmen_moniqi()
				sys.exit()
			elif input1 == '5' or input1 == '6':
				demo = Moniqi(moniqi, mode)
				demo.pvp_towin_moniqi(input1)
				sys.exit()
			elif input1 == '7':
				demo = Moniqi(moniqi, mode)
				demo.huodong_zhitouzi_moniqi()
				sys.exit()
			else:
				print("!!!!!输入有误,请重新输入!!!!!")
				time.sleep(1)
	else:
		print("找不到游戏王决斗链接，请打开游戏后再次尝试")
		time.sleep(5)
		sys.exit()


if __name__ == '__main__':
	reg = reg()
	resule = reg.chk_reg()
	if resule == 'vip':
		print('您是尊贵的VIP会员,当前版本为完整版')
		# time.sleep(2)
		t_tuosong = threading.Thread(target=tuisongfunction, args=(None,))
		t_main = threading.Thread(target=main, args=('1',))
		t_error = threading.Thread(target=error, args=())
		t_tuosong.setDaemon(True)
		t_error.setDaemon(True)
		t_tuosong.start()
		t_error.start()
		t_main.start()
	elif resule == 'connect failed':  # 连接失败,当前时间+半小时
		resule =time.time() + 1800
		timeArray = time.localtime(time.time() + 1800)
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		print('当前为试用模式,试用截止时间%s' % otherStyleTime)
		time.sleep(3)
		t_tuosong = threading.Thread(target=tuisongfunction, args=(resule,))
		t_main = threading.Thread(target=main, args=('2',))
		t_error = threading.Thread(target=error, args=())
		t_tuosong.setDaemon(True)
		t_error.setDaemon(True)
		t_tuosong.start()
		t_error.start()
		t_main.start()
	else:
		timeArray = time.localtime(resule)  # 秒数
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		print('当前为试用模式,试用截止时间%s' % otherStyleTime)
		time.sleep(3)
		t_tuosong = threading.Thread(target=tuisongfunction, args=(resule,))
		t_main = threading.Thread(target=main, args=('2',))
		t_error = threading.Thread(target=error, args=())
		t_tuosong.setDaemon(True)
		t_error.setDaemon(True)
		t_tuosong.start()
		t_error.start()
		t_main.start()

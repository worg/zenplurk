#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       zenPlurk.py
#       
#       Copyright 2010 worg <worg@linuxmail.org>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import gtk
import gobject
import pygtk
import webkit
import plurklib
from threading import Thread
import pynotify
import webbrowser as browser
pygtk.require('2.0')
from sys import path

localpath = path[0]
localpath += '/'

Plurk = plurklib.PlurkAPI("SsiAp8wzi8puMpsnDsyo4ahwMYLUUjWg")

def parsePlurk(oName, aPlurk):
	pID =str(aPlurk['owner_id'])
	text = '<div class="owner"><b>' + oName + ' </b></div>'
	text += '<div class="plurkContent"><div class="plurkText"><span class="qualifier">' + aPlurk['qualifier'] + ': </span>' + aPlurk['content'] + '</div> <br />'
	text += '<div class="actionButtons"><a href="zenplurk:reply' + pID + '" class="reply">Reply</a>'
	text += '<a href="zenplurk:mute' + pID + '" class="mute">Mute</a></div></div>'
	text = '<div class="plurkContainer">\n' + text + '\n</div>'
	return str(text)
		
class timeLineContainer(webkit.WebView):
	__gtype_name__ = 'timeLineContainer'
	
	def __init__(self):
		webkit.WebView.__init__(self)
		gtk.widget_push_composite_child()
		wkSettings = self.get_settings() 
		
		wkSettings.set_property("default-encoding","utf-8")
		wkSettings.set_property("default-font-size",9)
		wkSettings.set_property("enable-default-context-menu",False)
		wkSettings.set_property("enable-plugins", False)
		
		style = open(localpath + 'theme.css')
		script = open(localpath + 'userScript.js')
		self.theme = '<style>' + style.read() + '</style>\n '
		self.theme += '<script type="text/javascript" src="' + script.read() + '"></script>\n <body>'
		self.connect('navigation-policy-decision-requested', self.on_click_link)
		self.content = self.theme
		self.set_size_request(180,-1)
		gtk.widget_pop_composite_child()
	
	def addContent(self,name,content):
		self.content += parsePlurk(name, content)
		self.load_string(self.content,"text/html", "utf-8", "/")
		
	def clearContent(self):
		self.content = self.theme
		self.load_string(self.content,"text/html", "utf-8", "/")
		
	def muteFn(self, pID):
		pID = int(pID)
		response = Plurk.mutePlurks([pID])
		print response
		
	def on_click_link(self, view, frame, req, nav_act, pol_dec):
		uri = req.get_uri()
		
		if uri.startswith('/'): return False
		elif uri.startswith('zenplurk:reply'):
			pID = uri.replace('zenplurk:reply','')
			#Thread(target=self.replyFn, args=(pID,)).start() http://images.plurk.com/
			
		elif uri.startswith('zenplurk:mute'):
			pID = uri.replace('zenplurk:mute', '')
			#Thread(target=self.replyFn, args=(pID,)).start()
			
		elif uri.startswith('http://plurk.com/p/'):
			pID = uri.replace('http://plurk.com/p/', '')
			
		elif uri.startswith('http://www.plurk.com/'):
			pID = uri.replace('http://www.plurk.com/', '')
		
		elif uri.startswith('http://www.plurk.com/'):
			pID = uri.replace('http://www.plurk.com/', '')
				
		else:
			browser.open(uri)
		return True
    
class zenPlurk:
	def __init__(self):
		gtk.gdk.threads_init()
		self.main_fn = self
		self.builder = gtk.Builder() 
		self.builder.add_from_file(localpath + 'plurk.ui')
		self.LoginW = self.builder.get_object('LoginW')
		self.UsrN = self.builder.get_object('UsEn')
		self.PwN = self.builder.get_object('PwEn')
		self.msgL = self.builder.get_object('msgLbl')
		self.MainW = self.builder.get_object('MainW')
		self.list0 = self.builder.get_object('listview0')
		self.list1 = self.builder.get_object('listview1')
		self.list2 = self.builder.get_object('listview2')
		self.infoLog = self.builder.get_object('infoLog')
		self.pbar = self.builder.get_object('pBar')
		self.timeLine = self.builder.get_object('timeLine')

		self.table = gtk.Table(100,1, False)
		self.table2 = gtk.Table(100,1, False)
		
			
		#muestra los elementos de la ventana
		
		self.LoginW.show_all()
		#conectando los botones y eventos de la ventana a las funciones 
		self.builder.connect_signals(self)

	'''  ## Deprecated in favor of timeLineContainer class ##
	class PlurkBox(gtk.HBox):
		__gtype_name__ = 'PlurkBox'
		
		def muteFn(self, widget, ID):
			print ID, self.text
		
		def replyFn(self, widget, ID):
			print ID

		def __init__(self, text='', pID = ''):
			gtk.HBox.__init__(self)
			gtk.widget_push_composite_child()
			self.text = text
			self.set_resize_mode(gtk.RESIZE_IMMEDIATE)
			self.content = webkit.WebView()
			
			self.content.load_string(self.text,"text/html", "utf-8", "/")
			
			wkSettings = self.content.get_settings() 
			gtkSettings = self.get_settings()
			
			wkSettings.set_property("default-encoding","utf-8")
			wkSettings.set_property("default-font-size",9)
			wkSettings.set_property("enable-default-context-menu",False)
			gtkSettings.set_property('gtk-button-images',True)
			
			self.tBar = gtk.Toolbar()
			self.tTips = gtk.Tooltips()
			self.replyBtn = gtk.ToolButton('gtk-jump-to')
			self.muteBtn = gtk.ToolButton('gtk-no')
			self.tBar.insert(self.muteBtn,0)
			self.tBar.insert(self.replyBtn,1)

			self.tBar.set_orientation(gtk.ORIENTATION_VERTICAL)
			self.tBar.set_tooltips(True)
			self.replyBtn.set_size_request(20,25)
			self.replyBtn.set_tooltip(self.tTips,"Reply")
			self.muteBtn.set_size_request(20,25)
			self.muteBtn.set_tooltip(self.tTips,"Mute")
			self.tBar.set_size_request(35,-1)
			self.content.set_size_request(180,100)

			self.pack_start(self.content, True, True,0)
			self.pack_end(self.tBar, False, False,0)
								
			self.replyBtn.connect('clicked', self.replyFn, pID)
			self.muteBtn.connect('clicked', self.muteFn, pID)
			gtk.widget_pop_composite_child()

	'''
 
	def threadLogin(self,widget):
		gobject.timeout_add(0,self.showMe)
		gobject.idle_add(self.Login,widget)
	
	def showMe(self):
		self.infoLog.show_all()
		return False
		
	def close(self,widget):
		widget.hide()
		return True

	def Login(self, widget):
		response = Plurk.login(self.UsrN.get_text(), self.PwN.get_text(), 1)
		self.infoLog.hide()
		if 'success_text' in response:
			self.infoLog.hide()
			self.LoginW.hide()
			#self.list0.add(self.table)
			#self.list1.add(self.table2)
			#self.list2.add(self.timeLine)
			self.getUnread(self)
			self.MainW.show_all()
		else: 
			self.PwN.set_text('')
			self.infoLog.hide()
		#return False
			
	def getUnread(self, widget):
		unreadCount = Plurk.getUnreadCount()['all']
			
		unread = Plurk.getUnreadPlurks()
		
		if(0 < unreadCount):
			pynotify.Notification ('You have',' %s plurks unread' % (unreadCount),"notification-message-email").show()
			
		for a in unread['plurks']:
			oName = unread['plurk_users'][str(a['owner_id'])]['display_name']
			self.timeLine.addContent(oName,a)	
		
	def term(self,widget,data = 0):
		Thread(target=Plurk.logout,args=()).start
		gtk.main_quit()
	
	
	def resizeit(self,widget, data):
		self.table.check_resize()
		self.list0.check_resize()
		#self.MainW.show_all()
		
				
if __name__ == '__main__':
	w = zenPlurk()
	gtk.main()
	
	
''' TODO 

-Reply|Fav|Search Functions
-Own Timeline
-Code Cleanup
-UI Revision

'''

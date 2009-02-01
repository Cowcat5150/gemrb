# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003-2004 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Id$


# GUIMA.py - scripts to control map windows from GUIMA and GUIWMAP winpacks

###################################################

import GemRB
import GUICommonWindows
from GUIDefines import *
from GUICommon import CloseOtherWindow
from GUICommonWindows import *

MapWindow = None
WorldMapWindow = None
WorldMapControl = None
PortraitWindow = None
OptionsWindow = None
OldPortraitWindow = None
OldOptionsWindow = None

def RevealMap ():
	global MapWindow
	global OldPortraitWindow, OldOptionsWindow

	if CloseOtherWindow (ShowMap):
		if MapWindow:
			MapWindow.Unload ()
		if OptionsWindow:
			OptionsWindow.Unload ()
		if PortraitWindow:
			PortraitWindow.Unload ()

		MapWindow = None
		#this window type should block the game
		GemRB.SetVar ("OtherWindow", -1)
		GemRB.SetVisible (0,1)
		GemRB.UnhideGUI ()
		GUICommonWindows.PortraitWindow = OldPortraitWindow
		OldPortraitWindow = None
		GUICommonWindows.OptionsWindow = OldOptionsWindow
		OldOptionsWindow = None

	PosX = GemRB.GetVar ("MapControlX")
	PosY = GemRB.GetVar ("MapControlY")

	GemRB.RevealArea (PosX, PosY, 30, 1)
	GemRB.GamePause (0,0)
	return
###################################################
# for farsight effect
###################################################
def ShowMap ():
	global MapWindow, OptionsWindow, PortraitWindow
	global OldPortraitWindow, OldOptionsWindow

	if CloseOtherWindow (ShowMap):
		if MapWindow:
			MapWindow.Unload ()
		if OptionsWindow:
			OptionsWindow.Unload ()
		if PortraitWindow:
			PortraitWindow.Unload ()

		MapWindow = None
		#this window type should block the game
		GemRB.SetVar ("OtherWindow", -1)
		GemRB.SetVisible (0,1)
		GemRB.UnhideGUI ()
		GUICommonWindows.PortraitWindow = OldPortraitWindow
		OldPortraitWindow = None
		GUICommonWindows.OptionsWindow = OldOptionsWindow
		OldOptionsWindow = None
		return

	GemRB.HideGUI ()
	GemRB.SetVisible (0,0)

	GemRB.LoadWindowPack ("GUIMAP", 640, 480)
	MapWindow = Window = GemRB.LoadWindowObject (2)
	#this window type blocks the game normally, but map window doesn't
	GemRB.SetVar ("OtherWindow", MapWindow.ID)
	#saving the original portrait window
	OldOptionsWindow = GUICommonWindows.OptionsWindow
	OptionsWindow = GemRB.LoadWindowObject (0)
	SetupMenuWindowControls (OptionsWindow, 0, "ShowMap")
	OldPortraitWindow = GUICommonWindows.PortraitWindow
	PortraitWindow = OpenPortraitWindow (0)
	OptionsWindow.SetFrame ()

	# World Map
	Button = Window.GetControl (1)
	Button.SetState (IE_GUI_BUTTON_LOCKED)

	# Hide or Show mapnotes
	Button = Window.GetControl (3)
	Button.SetState (IE_GUI_BUTTON_LOCKED)

	Label = Window.GetControl (0x10000003)
	Label.SetText ("")
	# Map Control
	Window.CreateMapControl (2, 0, 0, 0, 0)
	Map = Window.GetControl (2)
	GemRB.SetVar("ShowMapNotes",IE_GUI_MAP_REVEAL_MAP)
	Map.SetVarAssoc ("ShowMapNotes", IE_GUI_MAP_REVEAL_MAP)
	Map.SetEvent (IE_GUI_MAP_ON_PRESS, "RevealMap")
	OptionsWindow.SetVisible (2)
	Window.SetVisible (1)
	PortraitWindow.SetVisible (2)
	GemRB.GamePause (0,0)
	return

###################################################
def OpenMapWindow ():
	global MapWindow, OptionsWindow, PortraitWindow
	global OldPortraitWindow, OldOptionsWindow

	if CloseOtherWindow (OpenMapWindow):
		if WorldMapWindow: OpenWorldMapWindowInside ()

		GemRB.HideGUI ()
		if MapWindow:
			MapWindow.Unload ()
		MapWindow = None
		GemRB.SetVar ("OtherWindow", -1)
		GemRB.UnhideGUI ()
		return

	GemRB.HideGUI ()

	GemRB.LoadWindowPack ("GUIMAP", 640, 480)
	MapWindow = Window = GemRB.LoadWindowObject (2)
	#this window type blocks the game normally, but map window doesn't
	GemRB.SetVar ("OtherWindow", MapWindow.ID)
	#saving the original portrait window
	OldOptionsWindow = GUICommonWindows.OptionsWindow
	OptionsWindow = GemRB.LoadWindowObject (0)
	SetupMenuWindowControls (OptionsWindow, 0, "OpenMapWindow")
	OptionsWindow.SetFrame ()
	OldPortraitWindow = GUICommonWindows.PortraitWindow
	PortraitWindow = OpenPortraitWindow (0)
	OptionsWindow.SetFrame ()

	# World Map
	Button = Window.GetControl (1)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OpenWorldMapWindowInside")

	# Map Control
	Window.CreateMapControl (2, 0, 0, 0, 0)
	Map = Window.GetControl (2)

	OptionsWindow.SetVisible (1)
	Window.SetVisible (1)
	PortraitWindow.SetVisible (1)
	Map.SetStatus (IE_GUI_CONTROL_FOCUSED)
	GemRB.UnhideGUI ()
	return

def LeftDoublePressMap ():
	print "MoveToPoint"
	return

def OpenWorldMapWindowInside ():
	WorldMapWindowCommon (-1)
	return

def OpenWorldMapWindow ():
	WorldMapWindowCommon (GemRB.GetVar ("Travel"))
	return

def MoveToNewArea ():
	global WorldMapWindow, WorldMapControl

	tmp = WorldMapControl.GetDestinationArea ()
	CloseWorldMapWindow ()
	GemRB.CreateMovement (tmp["Destination"], tmp["Entrance"])
	return

def ChangeTooltip ():
	global WorldMapWindow, WorldMapControl
	global str

	tmp = WorldMapControl.GetDestinationArea ()
	if (tmp):
		str = "%s: %d"%(GemRB.GetString(23084),tmp["Distance"])
	else:
		str=""

	WorldMapControl.SetTooltip (str)
	return

def CloseWorldMapWindow ():
	global WorldMapWindow, WorldMapControl

	if WorldMapWindow:
		WorldMapWindow.Unload ()
	WorldMapWindow = None
	WorldMapControl = None
	GemRB.SetVisible (0,1)
	GemRB.UnhideGUI ()
	return

def WorldMapWindowCommon (Travel):
	global WorldMapWindow, WorldMapControl

	if WorldMapWindow:
		CloseWorldMapWindow ()
		return

	GemRB.HideGUI ()
	GemRB.SetVisible (0,0)

	GemRB.LoadWindowPack ("GUIWMAP", 640, 480)
	WorldMapWindow = Window = GemRB.LoadWindowObject (0)
	MapWindow = None
	Window.SetFrame ()

	Window.CreateWorldMapControl (4, 0, 62, 640, 418, Travel, "infofont")
	WorldMapControl = Window.GetControl (4)
	WorldMapControl.SetAnimation ("WMDAG")
	WorldMapControl.SetEvent (IE_GUI_WORLDMAP_ON_PRESS, "MoveToNewArea")
	WorldMapControl.SetEvent (IE_GUI_MOUSE_ENTER_WORLDMAP, "ChangeTooltip")

	#north
	Button = Window.GetControl (1)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "MapN")

	#south
	Button = Window.GetControl (2)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "MapS")

	# Done
	Button = Window.GetControl (0)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "CloseWorldMapWindow")
	Window.SetVisible (1)
	return

def MapN():
	WorldMapControl.AdjustScrolling (0, -10)
	return

def MapS():
	WorldMapControl.AdjustScrolling (0, 10)
	return


###################################################
# End of file GUIMA.py

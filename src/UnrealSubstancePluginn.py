import tkinter.filedialog #import to create windows
from unreal import ToolMenus,ToolMenuContext, ToolMenuEntryScript,uclass,ufunction #imports functions from unreal
import sys #imports system enviroment
import os #imports operating system
import importlib #imports python module tools
import tkinter #import to create windows also


srcDir = os.path.dirname(os.path.abspath(__file__)) #location of script
if srcDir not in sys.path: #if not found, loaction of script in path
    sys.path.append(srcDir) #find it



import UnrealUtilities #imports utilities from unreal
importlib.reload(UnrealUtilities) #reload unreal utilities after import


@uclass() #defines class to be used as a class in unreal
class LoadFromDirEntryScript(ToolMenuEntryScript):
    @ufunction(override = True) #function for unreal
    def execute(self,context): #run this class with parameters are met
        window = tkinter.Tk() #creates a tkinter window 
        window.withdraw()  #hides tkinter window
        fileDir = tkinter.filedialog.askdirectory() #chooses folder with file dialog
        window.destroy() #destroys tkinter window
        UnrealUtilities.UnrealUtiity().LoadFromDir(fileDir) #uses function LoadFromDir from UnrealUtilities


@uclass() #defines class to be used as a class in unreal
class BuildBaseMaterialEntryScript(ToolMenuEntryScript): #builds base material entry script
    @ufunction(override=True) #unreal funtion
    def execute(self,context:ToolMenuContext) -> None: #makes tool menu context
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial() #finds or creates base material in tool menu


class UnrealSubstancePlugin: #creates plugin in unreal
    def __init__ (self): #makes object in unreal substance plugin
        self.subMenuName = "SubstancePlugin" #name of menu
        self.subMenuLabel = "Substance Plugin" #menu label
        self.InitUI() #adds to UI

    def InitUI(self):  #creates button in UI for unreal engine
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu") #opens level editor in main menu
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name,"","SubstancePlugin","Substance Plugin") #makes submenu
        self.AddEntryScript("BuildBasematerial", "Build Base Material", BuildBaseMaterialEntryScript()) #What button is named/its function, and function from buildbasematerialentry
        ToolMenus.get().refresh_all_widgets() #updates UI

        
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript()) #adding identifier to object from load directory script
        ToolMenus.get().refresh_all_widgets() #updates UI

    def AddEntryScript(self,name,label,script: ToolMenuEntryScript): #adds attributes to object in tool menu entry script
        script.init_entry(self.subMenu.menu_name,self.subMenu.menu_name,"",name,label) #starts menu entry with the attributes of name /label of each object in menu
        script.register_menu_entry() #creates menu entry

UnrealSubstancePlugin() #runs code


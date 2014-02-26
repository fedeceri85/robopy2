import imp
import os

PluginFolder = "./plugins/"
MainModule = "__init__"

def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    print(possibleplugins)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if os.path.splitext(i)[1] == '.py':
		info = imp.find_module(os.path.splitext(i)[0], [PluginFolder])
		plugins.append({"name": i, "info": info})
    return plugins

def loadPlugin(plugin):
    ans = None
    try:
	ans = imp.load_module('MainModule', *plugin["info"])
    except:
	pass
    return ans
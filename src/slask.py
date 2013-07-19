def updateSavers(nameParser = None):
    
    for node in nuke.allNodes("Write"):
        match = re.match('([\w_]+)(GSaver|GElement)$', node.name())
        fileType = node['file_type'].value()
        if fileType == " ":
            return False
        if match:
            element = match.group(1)
            type = match.group(2)
            if type == "GElement":
                if node['elementVersion'] and node['lockVersion']:
                    elementSplit = element.split("_")
                    element = elementSplit.pop()
                    extraPath = ""
                    if len(elementSplit) > 0:
                        extraPath = "/".join(elementSplit)+"/"
                    if not node['lockVersion'].value():
                        node['elementVersion'].setValue(int(nameParser.version.lstrip('v')))
                    basePath = "%s/2dElements/%s/%s%s/v%03d" % (renderBasePath, nameParser.type, extraPath, element, node['elementVersion'].value())
                    node['file'].setValue("%s/%s_%s_%s_v%03d_%s.%%0%dd.%s" % (basePath, nameParser.projectShort, nameParser.sequenceName, nameParser.shotName, node['elementVersion'].value(), element, padding, fileType))
            if type == "GSaver":
                basePath = "%s/compOut/%s" % (renderBasePath, nameParser.version)
                if element == "main":
                    node['file'].setValue("%s/%s_%s_%s_%s_comp.%%0%dd.%s" % (basePath, nameParser.projectShort, nameParser.sequenceName, nameParser.shotName, nameParser.version, padding, fileType))
                else:
                    node['file'].setValue("%s/%s/%s_%s_%s_%s_comp.%%0%dd.%s" % (basePath, element, nameParser.projectShort, nameParser.sequenceName, nameParser.shotName, nameParser.version, padding, fileType))
            if not os.path.exists(os.path.dirname(node['file'].value())):
                os.makedirs(os.path.dirname(node['file'].value()))
    return True


updateSavers()
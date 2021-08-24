from bs4 import BeautifulSoup, Tag
from docutils import nodes
import os.path

known_start_tags = ['p','img','table']
hidden_tag = 'hidden'

def html2Docutils(app, doctree):
    #find all raw nodes
    if not app.env.config.sphinx_md_processRaw:
        return
    filepath = doctree['source']
    htmlCounter = 0
    for node in doctree.traverse(nodes.raw):
        soup = BeautifulSoup(node.astext(),features="html.parser")
        if soup.find():
            if soup.find().name in known_start_tags:
                #send it to converter
                div = nodes.container()
                div['id']='html-content-' + str(htmlCounter)
                htmlCounter += 1
                convertHTML(soup, div, app, filepath)
                parent = node.parent
                parent.replace(node,div.children)
                #replace raw node with output of converter
                #child = nodes.Text("poof")
                #node[0]=child
            elif soup.find().name == hidden_tag:
                hidden_comment = nodes.comment()
                comment_text = nodes.Text("hidden")
                hidden_comment.append(comment_text)
                parent = node.parent
                parent.replace(node,hidden_comment)

def convertHTML(soup, parent, app, filepath):
    if hasattr(soup,"children"):
        for child in soup.children:
            node = None
            if hasattr(child,"name") and child.name is not None:
                if child.name == "table":
                    if filepath not in app.env.config.sphinx_md_tableIDs:
                        app.env.config.sphinx_md_tableIDs['filepath']=0
                    else:
                        app.evn.config.sphinx_md_tableIDs['filepath'] += 1
                    tNode = nodes.table()
                    tNode['ids'].append("id"+str(app.env.config.sphinx_md_tableIDs['filepath']))
                    titleNode = nodes.title()
                    node = nodes.tgroup()
                    ncols = getNumCols(child)
                    node['cols']= ncols
                    for x in range(ncols):
                        colspecNode = nodes.colspec()
                        colspecNode["colwidth"]=1
                        node += colspecNode
                    tNode += titleNode
                    tNode += node
                    parent += tNode
                elif child.name == "p":
                    node = nodes.paragraph()
                    parent += node
                elif child.name == "img":
                    node = nodes.image()
                    imgPath = ""
                    if "alt" in child.attrs:
                        node["alt"]=child.attrs['alt']
                    if "src" in child.attrs:
                        if "https" in child.attrs['src']:
                            node["uri"]=child.attrs['src']
                        else:
                            basepath = app.env.srcdir + "/"
                            docfilename = os.path.splitext(os.path.relpath(filepath,basepath))[0]
                            relpath = os.path.dirname(os.path.relpath(filepath,basepath))
                            imgPath = os.path.join(relpath,child.attrs['src'])
                            node["uri"]= imgPath
                            if os.path.isfile(imgPath):
                                if imgPath not in app.env.images:
                                    imageFileName = os.path.basename(imgPath)
                                    imageTuple = ({docfilename},imageFileName)
                                    app.env.images[imgPath]=imageTuple
                    if "width" in child.attrs:
                        suffix = ''
                        if child.attrs['width'].isnumeric():
                            suffix = 'px'
                        node["width"]=child.attrs['width'] + suffix
                    if "height" in child.attrs:
                        node["height"]=child.attrs['height']
                    node["candidates"]="{'*': '" + imgPath + "'}"
                    parent += node
                elif child.name == "thead":
                    node = nodes.thead()
                    parent += node
                elif child.name == "tbody":
                    node = nodes.tbody()
                    parent += node
                elif child.name == "tr":
                    node = nodes.row()
                    parent += node
                elif child.name == "th" or child.name == "td":
                    eNode = nodes.entry()
                    node = nodes.paragraph()
                    eNode += node
                    parent += eNode
                elif child.name == "sup":
                    node = nodes.superscript()
                    parent += node
                elif child.name == "a":
                    node = nodes.reference()
                    node["refuri"] = child.attrs['href']
                    parent += node
                elif child.name == "code":
                    node = nodes.literal()
                    parent += node
            else:
                if isinstance(parent,nodes.Node):
                #if isinstance(parent, nodes.entry) or isinstance(parent, nodes.paragraph) or isinstance(parent, nodes.image) or isinstance(parent, nodes.superscript) or isinstance(parent, nodes.reference) or isinstance(parent, nodes.literal):
                    node = nodes.Text(child)
                    parent += node
            if node:
                convertHTML(child,node,app,filepath)

def removeHTMLAttributes(soup,tagName):
    tags = soup.find_all(tagName)
    for tag in tags:
        attList = []
        for attr in tag.attrs:
            attList.append(attr)
        for att in attList:
            del tag[att]
    return soup

def replaceTag(soup,oldTag,newTag,delAttrs=True):
    tags = soup.find_all(oldTag)
    for tag in tags:
        tag.name = newTag
        if delAttrs:
            attList = []
            for attr in tag.attrs:
                attList.append(attr)
            for att in attList:
                del tag[att]
    return soup

def fixImages(soup):
    imgTags = soup.find_all('img')
    for imgTag in imgTags:
        altTag = soup.new_tag("alt")
        imgTag.name = "image"
        imgTag['href']=imgTag['src']
        del imgTag['src']
        altTag.string = imgTag['alt']
        del imgTag['alt']
        imgTag.append(altTag)
    return soup


def addTGroup(soup):
    numCols = getNumCols(soup)
    tags = soup.find_all('table')
    for tableTag in tags:
        tableTag.name = 'tgroup'
        tableTag['cols']=numCols
        del tableTag['class']
        wrap(tableTag,soup.new_tag("table"))
    return soup

def wrap(to_wrap, wrap_in):
    contents = to_wrap.replace_with(wrap_in)
    wrap_in.append(contents)

def getNumCols(soup):
    rows = soup.find_all('th')
    return len(rows)
#<?xml version="1.0" encoding="utf-8" ?>
#<data>
#    <country name="Liechtenstein">
#        <rank updated="yes">2</rank>
#        <year>2008</year>
#        <gdppc>141100</gdppc>
#        <neighbor name="Austria" direction="E"/>
#        <neighbor name="Switzerland" direction="W"/>
#    </country>
#</data>

from xml.etree.ElementTree import parse
 
f = open('demo.xml')
# 第1个参数为输入源，返回一个ElementTree对象
et = parse(f)
# 通过元素树(ElementTree)得到根结点
root = et.getroot()
print(root)
# 查看标签
print(root.tag)
# 查看属性
print(root.attrib)
# 查看文本,去除空格
print(root.text.strip())
 
# 遍历元素树
# 得到节点的子元素,python3中getchildren被废弃
children = list(root)
print(children)
# 获取每个子节点元素的属性
for child in root:
    print(child.get('name'))
'''
find、findall和iterfind只能找对于
当前的元素它的直接子元素,不能查找孙子元素。
    
'''
# 根据标签寻找子元素,find总是找到第1个碰到的元素
print(root.find('country'))
# findall是找到所有的的元素
print(root.findall('country'))
# 不需要列表，希望是一个可迭代对象,得到一个生成器对象
print(root.iterfind('country'))
 
for e in root.iterfind('country'):
    print(e.get('name'))
 
# 无论在那个层级下都能找到rank标签
# 在默认情况下不输入参数，会列出整个当前节点之下的所有元素
print(list(root.iter()))
# 递归的去寻找标签为rank的子节点
print(list(root.iter('rank')))

#############################################################################
from xml.etree.ElementTree import parse
 
f = open('demo.xml')
# 第1个参数为输入源，返回一个ElementTree对象
et = parse(f)
# 通过元素树(ElementTree)得到根结点
root = et.getroot()
 
# *能匹配所有的child,只想找root的所有孙子节点
print(root.findall('country/*'))
# 查找任意层次下的子元素，.点为当前节点，..为父节点
print(root.findall('.//rank'))
print(root.findall('.//rank/..'))
# @描述包含某一属性，[@attrib]
print(root.findall('country[@name]'))
# 指定属性为特定值，[@attrib='value']
print(root.findall('country[@name="Singapore"]'))
# 指定一个元素必须包含一个指定的子元素，[tag]
print(root.findall('country[rank]'))
# 指定元素的文本必须等于特定的值，[tag='text']
print(root.findall('country[rank="5"]'))
# 找多个元素路径指定相对位置，[position]
print(root.findall('country[1]'))
print(root.findall('country[2]'))
# last()为倒着找
print(root.findall('country[last()]'))
# 找倒数第二个
print(root.findall('country[last()-1]'))
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
# ��1������Ϊ����Դ������һ��ElementTree����
et = parse(f)
# ͨ��Ԫ����(ElementTree)�õ������
root = et.getroot()
print(root)
# �鿴��ǩ
print(root.tag)
# �鿴����
print(root.attrib)
# �鿴�ı�,ȥ���ո�
print(root.text.strip())
 
# ����Ԫ����
# �õ��ڵ����Ԫ��,python3��getchildren������
children = list(root)
print(children)
# ��ȡÿ���ӽڵ�Ԫ�ص�����
for child in root:
    print(child.get('name'))
'''
find��findall��iterfindֻ���Ҷ���
��ǰ��Ԫ������ֱ����Ԫ��,���ܲ�������Ԫ�ء�
    
'''
# ���ݱ�ǩѰ����Ԫ��,find�����ҵ���1��������Ԫ��
print(root.find('country'))
# findall���ҵ����еĵ�Ԫ��
print(root.findall('country'))
# ����Ҫ�б�ϣ����һ���ɵ�������,�õ�һ������������
print(root.iterfind('country'))
 
for e in root.iterfind('country'):
    print(e.get('name'))
 
# �������Ǹ��㼶�¶����ҵ�rank��ǩ
# ��Ĭ������²�������������г�������ǰ�ڵ�֮�µ�����Ԫ��
print(list(root.iter()))
# �ݹ��ȥѰ�ұ�ǩΪrank���ӽڵ�
print(list(root.iter('rank')))

#############################################################################
from xml.etree.ElementTree import parse
 
f = open('demo.xml')
# ��1������Ϊ����Դ������һ��ElementTree����
et = parse(f)
# ͨ��Ԫ����(ElementTree)�õ������
root = et.getroot()
 
# *��ƥ�����е�child,ֻ����root���������ӽڵ�
print(root.findall('country/*'))
# �����������µ���Ԫ�أ�.��Ϊ��ǰ�ڵ㣬..Ϊ���ڵ�
print(root.findall('.//rank'))
print(root.findall('.//rank/..'))
# @��������ĳһ���ԣ�[@attrib]
print(root.findall('country[@name]'))
# ָ������Ϊ�ض�ֵ��[@attrib='value']
print(root.findall('country[@name="Singapore"]'))
# ָ��һ��Ԫ�ر������һ��ָ������Ԫ�أ�[tag]
print(root.findall('country[rank]'))
# ָ��Ԫ�ص��ı���������ض���ֵ��[tag='text']
print(root.findall('country[rank="5"]'))
# �Ҷ��Ԫ��·��ָ�����λ�ã�[position]
print(root.findall('country[1]'))
print(root.findall('country[2]'))
# last()Ϊ������
print(root.findall('country[last()]'))
# �ҵ����ڶ���
print(root.findall('country[last()-1]'))
import json
import shutil
from socket import timeout
import requests
import os

#每个线程重复运行测试数据次数
repeat_cnt=100

class HttpTest:
	headers = {'Content-Type': 'application/json'}

	def __init__(self,url_infos):
		self.url_infos=url_infos
		self.ret_data={}
		self.summy={}
		self.summy_failed={}
		self.summy_success={}
		self.except_error={}

	def SaveTestData(self,bin_dir='bin'):
		if os.path.exists(bin_dir):
			shutil.rmtree(bin_dir)
			
		os.makedirs(bin_dir)
		json.dump(self.ret_data,open(bin_dir+"/test_res.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
		json.dump(self.summy,open(bin_dir+"/summy.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
		json.dump(self.summy_failed,open(bin_dir+"/summy_failed.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
		json.dump(self.except_error,open(bin_dir+"/except_error.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)

	def Json(response):
		try:
			ret_obj=response.json()
			return (not ret_obj['error'],ret_obj)
		except :
			return (False,  str(response.content, encoding="utf-8"))

	def AddMapMapKeyValue(map_obj,map_key,key,value):
		if not map_key in map_obj:
			map_obj[map_key]={}
		map_obj[map_key][key]=value

	def RecordRes(self,response,url_key,test_key):
		ret_obj=HttpTest.Json(response)
		HttpTest.AddMapMapKeyValue(self.ret_data,url_key,test_key,ret_obj[1])
		summy_str=("success" if response.ok and ret_obj[0] else "failed:")+ "used time:",response.elapsed.microseconds
		HttpTest.AddMapMapKeyValue(self.summy,url_key,test_key,summy_str)
		if response.ok and ret_obj[0]:
			HttpTest.AddMapMapKeyValue(self.summy_success,url_key,test_key,summy_str)
		else:
			HttpTest.AddMapMapKeyValue(self.summy_failed,url_key,test_key,summy_str)

	def ExceptionError(self,url_key,test_key,exception):
		HttpTest.AddMapMapKeyValue(self.except_error,url_key,test_key,"exception error:"+str(exception))

	def SetupTest(self):
		for x in range(repeat_cnt):
			for url_info in self.url_infos.items():
				for test_info in url_info[1]:
					test_info_json=json.dumps(test_info)
					try:
						response = requests.post(url=url_info[0],headers=HttpTest.headers, data=test_info_json,timeout=5)
						test_info_json+="("+str(x)+")"
						self.RecordRes(response,url_info[0],test_info_json)
					except Exception as exception:
						self.ExceptionError(url_info[0],test_info_json,exception)

			#self.SaveTestData()
if __name__=="__main__":
	url_infos=json.load(open("market_20108.json",encoding='utf8'))
	test=HttpTest(url_infos)
	test.SetupTest()
	test.SaveTestData()
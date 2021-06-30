// ATLSimpleObject.h : Declaration of the CATLSimpleObject

#pragma once
#include "resource.h"       // main symbols



#include "ATLProject2_i.h"
#include <string>
#include<fstream>



#if defined(_WIN32_WCE) && !defined(_CE_DCOM) && !defined(_CE_ALLOW_SINGLE_THREADED_OBJECTS_IN_MTA)
#error "Single-threaded COM objects are not properly supported on Windows CE platform, such as the Windows Mobile platforms that do not include full DCOM support. Define _CE_ALLOW_SINGLE_THREADED_OBJECTS_IN_MTA to force ATL to support creating single-thread COM object's and allow use of it's single-threaded COM object implementations. The threading model in your rgs file was set to 'Free' as that is the only threading model supported in non DCOM Windows CE platforms."
#endif

using namespace ATL;


// CATLSimpleObject

class ATL_NO_VTABLE CATLSimpleObject :
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CATLSimpleObject, &CLSID_ATLSimpleObject>,
	public IDispatchImpl<IATLSimpleObject, &IID_IATLSimpleObject, &LIBID_ATLProject2Lib, /*wMajor =*/ 1, /*wMinor =*/ 0>,
	public IDispatchImpl<_IDTExtensibility2, &__uuidof(_IDTExtensibility2), &LIBID_AddInDesignerObjects, /* wMajor = */ 1, /* wMinor = */ 0>,
	public IDispatchImpl<IRibbonExtensibility, &__uuidof(IRibbonExtensibility), &LIBID_Office, /* wMajor = */ 2, /* wMinor = */ 4>
{
public:
	CATLSimpleObject()
	{
	}

DECLARE_REGISTRY_RESOURCEID(106)


BEGIN_COM_MAP(CATLSimpleObject)
	COM_INTERFACE_ENTRY(IATLSimpleObject)
	COM_INTERFACE_ENTRY2(IDispatch, IATLSimpleObject)
	COM_INTERFACE_ENTRY(_IDTExtensibility2)
	COM_INTERFACE_ENTRY(IRibbonExtensibility)
END_COM_MAP()



	DECLARE_PROTECT_FINAL_CONSTRUCT()

	HRESULT FinalConstruct()
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}

public:




// _IDTExtensibility2 Methods
public:
	STDMETHOD(OnConnection)(LPDISPATCH Application, ext_ConnectMode ConnectMode, LPDISPATCH AddInInst, SAFEARRAY * * custom)
	{
		 return S_OK;
	}

	STDMETHOD(OnDisconnection)(ext_DisconnectMode RemoveMode, SAFEARRAY * * custom)
	{
		 return S_OK;
	}

	STDMETHOD(OnAddInsUpdate)(SAFEARRAY * * custom)
	{
		 return S_OK;
	}

	STDMETHOD(OnStartupComplete)(SAFEARRAY * * custom)
	{
		 return S_OK;
	}

	STDMETHOD(OnBeginShutdown)(SAFEARRAY * * custom)
	{
		 return S_OK;
	}

private:
	IRibbonUI* m_IRibbonUI = nullptr;

// IRibbonExtensibility Methods
public:
	STDMETHOD(GetCustomUI)(BSTR RibbonID, BSTR *GetCustomUI)
	{
		char fileNamePath[_MAX_PATH];
		//获取本模块的路径，
		GetModuleFileNameA(GetModuleHandleA("ATLProject2.dll"), fileNamePath, sizeof(fileNamePath));
		PathRemoveFileSpecA(fileNamePath);

		std::string filename = std::string(fileNamePath)+ R"(/menu.xml)";
		std::ifstream infile(filename.c_str());
		infile.seekg(0, infile.end);
		auto totalBytes = infile.tellg();//文件的总共多少字节
		infile.seekg(0, infile.beg);
		std::shared_ptr<char> pbuff(new char[totalBytes] {}, std::default_delete<char[]>());
		infile.read(pbuff.get(), totalBytes);
		CComBSTR cbstr(_com_util::ConvertStringToBSTR(pbuff.get()));
		*GetCustomUI = cbstr.Detach();

		return (*GetCustomUI ? S_OK : E_OUTOFMEMORY);
	}
	STDMETHOD(OnStart)(IDispatch* RibbonControl);
	STDMETHOD(GetVisible)(IDispatch* RibbonControl, VARIANT_BOOL* pvarReturnedVal);
	STDMETHOD(OnLoad)(IDispatch* RibbonControl);
	STDMETHOD(GetEnabled)(IDispatch* RibbonControl, VARIANT_BOOL* pvarReturnedVal);
};

OBJECT_ENTRY_AUTO(__uuidof(ATLSimpleObject), CATLSimpleObject)

// dllmain.h : Declaration of module class.

class CATLProject2Module : public ATL::CAtlDllModuleT< CATLProject2Module >
{
public :
	DECLARE_LIBID(LIBID_ATLProject2Lib)
	DECLARE_REGISTRY_APPID_RESOURCEID(IDR_ATLPROJECT2, "{266a7ba0-7a0f-4afb-b4a0-8d05a89a9d75}")
};

extern class CATLProject2Module _AtlModule;

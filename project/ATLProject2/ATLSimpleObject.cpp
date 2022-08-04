// ATLSimpleObject.cpp : Implementation of CATLSimpleObject

#include "pch.h"
#include "ATLSimpleObject.h"


// CATLSimpleObject



STDMETHODIMP CATLSimpleObject::OnStart(IDispatch* RibbonControl) {
    // TODO: 在此添加实现代码
    IRibbonControl* pCtrl = NULL;

    RibbonControl->QueryInterface(IID_IRibbonControl, (LPVOID*)&pCtrl);
    if (pCtrl) {
        BSTR button_id = NULL;
        pCtrl->get_Id(&button_id);
       //deal_id_func(button_id);
    }
    return S_OK;
}


STDMETHODIMP CATLSimpleObject::GetVisible(IDispatch* RibbonControl, VARIANT_BOOL* pvarReturnedVal) {
    // TODO: Add your implementation code here
    IRibbonControl* pCtrl = nullptr;
    RibbonControl->QueryInterface(IID_IRibbonControl, (LPVOID*)&pCtrl);
    if (pCtrl) {
        BSTR ctrlId = nullptr;
        pCtrl->get_Id(&ctrlId);

        const bool bEnable = true;
        *pvarReturnedVal = bEnable ? VARIANT_TRUE : VARIANT_FALSE;
    }

    return S_OK;
}


STDMETHODIMP CATLSimpleObject::OnLoad(IDispatch* RibbonControl) {
	// TODO: Add your implementation code here
	RibbonControl->QueryInterface(IID_IRibbonUI, (LPVOID*)&m_IRibbonUI);
	//m_IRibbonUI->Invalidate();  刷新界面
	return S_OK;
}


STDMETHODIMP CATLSimpleObject::GetEnabled(IDispatch* RibbonControl, VARIANT_BOOL* pvarReturnedVal) {
    // TODO: Add your implementation code here
    IRibbonControl* pCtrl = nullptr;
    RibbonControl->QueryInterface(IID_IRibbonControl, (LPVOID*)&pCtrl);
    if (pCtrl) {
        BSTR bstr = nullptr;
        pCtrl->get_Id(&bstr);
        const bool bEnable = true;
        *pvarReturnedVal = bEnable ? VARIANT_TRUE : VARIANT_FALSE;
    }

    return S_OK;
}

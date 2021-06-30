

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.01.0622 */
/* at Tue Jan 19 11:14:07 2038
 */
/* Compiler settings for ATLProject2.idl:
    Oicf, W1, Zp8, env=Win32 (32b run), target_arch=X86 8.01.0622 
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */



/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 500
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif /* __RPCNDR_H_VERSION__ */

#ifndef COM_NO_WINDOWS_H
#include "windows.h"
#include "ole2.h"
#endif /*COM_NO_WINDOWS_H*/

#ifndef __ATLProject2_i_h__
#define __ATLProject2_i_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __IATLSimpleObject_FWD_DEFINED__
#define __IATLSimpleObject_FWD_DEFINED__
typedef interface IATLSimpleObject IATLSimpleObject;

#endif 	/* __IATLSimpleObject_FWD_DEFINED__ */


#ifndef __ATLSimpleObject_FWD_DEFINED__
#define __ATLSimpleObject_FWD_DEFINED__

#ifdef __cplusplus
typedef class ATLSimpleObject ATLSimpleObject;
#else
typedef struct ATLSimpleObject ATLSimpleObject;
#endif /* __cplusplus */

#endif 	/* __ATLSimpleObject_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "shobjidl.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __IATLSimpleObject_INTERFACE_DEFINED__
#define __IATLSimpleObject_INTERFACE_DEFINED__

/* interface IATLSimpleObject */
/* [unique][nonextensible][dual][uuid][object] */ 


EXTERN_C const IID IID_IATLSimpleObject;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("f2772e15-32b0-4e99-a028-1e0a6441f355")
    IATLSimpleObject : public IDispatch
    {
    public:
        virtual /* [id] */ HRESULT STDMETHODCALLTYPE OnStart( 
            /* [in] */ IDispatch *RibbonControl) = 0;
        
        virtual /* [id] */ HRESULT STDMETHODCALLTYPE GetVisible( 
            /* [in] */ IDispatch *GetVisible,
            /* [retval][out] */ VARIANT_BOOL *pvarReturnedVal) = 0;
        
        virtual /* [id] */ HRESULT STDMETHODCALLTYPE OnLoad( 
            /* [in] */ IDispatch *RibbonControl) = 0;
        
        virtual /* [id] */ HRESULT STDMETHODCALLTYPE GetEnabled( 
            /* [in] */ IDispatch *RibbonControl,
            /* [retval][out] */ VARIANT_BOOL *pvarReturnedVal) = 0;
        
    };
    
    
#else 	/* C style interface */

    typedef struct IATLSimpleObjectVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            IATLSimpleObject * This,
            /* [in] */ REFIID riid,
            /* [annotation][iid_is][out] */ 
            _COM_Outptr_  void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            IATLSimpleObject * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            IATLSimpleObject * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            IATLSimpleObject * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            IATLSimpleObject * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            IATLSimpleObject * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            IATLSimpleObject * This,
            /* [annotation][in] */ 
            _In_  DISPID dispIdMember,
            /* [annotation][in] */ 
            _In_  REFIID riid,
            /* [annotation][in] */ 
            _In_  LCID lcid,
            /* [annotation][in] */ 
            _In_  WORD wFlags,
            /* [annotation][out][in] */ 
            _In_  DISPPARAMS *pDispParams,
            /* [annotation][out] */ 
            _Out_opt_  VARIANT *pVarResult,
            /* [annotation][out] */ 
            _Out_opt_  EXCEPINFO *pExcepInfo,
            /* [annotation][out] */ 
            _Out_opt_  UINT *puArgErr);
        
        /* [id] */ HRESULT ( STDMETHODCALLTYPE *OnStart )( 
            IATLSimpleObject * This,
            /* [in] */ IDispatch *RibbonControl);
        
        /* [id] */ HRESULT ( STDMETHODCALLTYPE *GetVisible )( 
            IATLSimpleObject * This,
            /* [in] */ IDispatch *GetVisible,
            /* [retval][out] */ VARIANT_BOOL *pvarReturnedVal);
        
        /* [id] */ HRESULT ( STDMETHODCALLTYPE *OnLoad )( 
            IATLSimpleObject * This,
            /* [in] */ IDispatch *RibbonControl);
        
        /* [id] */ HRESULT ( STDMETHODCALLTYPE *GetEnabled )( 
            IATLSimpleObject * This,
            /* [in] */ IDispatch *RibbonControl,
            /* [retval][out] */ VARIANT_BOOL *pvarReturnedVal);
        
        END_INTERFACE
    } IATLSimpleObjectVtbl;

    interface IATLSimpleObject
    {
        CONST_VTBL struct IATLSimpleObjectVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define IATLSimpleObject_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define IATLSimpleObject_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define IATLSimpleObject_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define IATLSimpleObject_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define IATLSimpleObject_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define IATLSimpleObject_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define IATLSimpleObject_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#define IATLSimpleObject_OnStart(This,RibbonControl)	\
    ( (This)->lpVtbl -> OnStart(This,RibbonControl) ) 

#define IATLSimpleObject_GetVisible(This,GetVisible,pvarReturnedVal)	\
    ( (This)->lpVtbl -> GetVisible(This,GetVisible,pvarReturnedVal) ) 

#define IATLSimpleObject_OnLoad(This,RibbonControl)	\
    ( (This)->lpVtbl -> OnLoad(This,RibbonControl) ) 

#define IATLSimpleObject_GetEnabled(This,RibbonControl,pvarReturnedVal)	\
    ( (This)->lpVtbl -> GetEnabled(This,RibbonControl,pvarReturnedVal) ) 

#endif /* COBJMACROS */


#endif 	/* C style interface */




#endif 	/* __IATLSimpleObject_INTERFACE_DEFINED__ */



#ifndef __ATLProject2Lib_LIBRARY_DEFINED__
#define __ATLProject2Lib_LIBRARY_DEFINED__

/* library ATLProject2Lib */
/* [version][uuid] */ 


EXTERN_C const IID LIBID_ATLProject2Lib;

EXTERN_C const CLSID CLSID_ATLSimpleObject;

#ifdef __cplusplus

class DECLSPEC_UUID("8cb3ed76-4a3e-40c9-a375-dc3affecdb47")
ATLSimpleObject;
#endif
#endif /* __ATLProject2Lib_LIBRARY_DEFINED__ */

/* Additional Prototypes for ALL interfaces */

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif



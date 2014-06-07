#include <Python.h>
#include <string>
#include <sstream>
#include <iostream>

#define BUFFER_SIZE 1024

typedef struct {
	PyObject_HEAD
	usbDevice_t* usbDevice;
	uint8_t send_buf[BUFFER_SIZE];
	uint8_t recv_buf[BUFFER_SIZE];
} linkmpy_LinkMObj;

static PyObject* LinkMError;

void doLinkMError(const std::string& err) {
	PyErr_SetString(LinkMError, err.c_str());
}

// Have to declare anything that is directly passed into python with extern C
extern "C" {
	static void LinkMObj_dealloc(linkmpy_LinkMObj* self);
	static PyObject * LinkMObj_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
	static int LinkMObj_init(linkmpy_LinkMObj* self, PyObject* args, PyObject* kwds);
	PyMODINIT_FUNC initlinkmpy(void);
	//DL_EXPORT(void) initflp();
}

static void
LinkMObj_dealloc(linkmpy_LinkMObj* self)
{
	if(self->usbDevice) {
		linkm_close(self->usbDevice);
	}

	//delete self->usbDevice; // do we need to do some deallocation here?

	self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
LinkMObj_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	linkmpy_LinkMObj *self;

	self = (linkmpy_LinkMObj*)type->tp_alloc(type, 0);
	if (self != NULL) {
		self->usbDevice = NULL;
	}

	return (PyObject *)self;
}

static int
LinkMObj_init(linkmpy_LinkMObj* self)
{
	// Connect to link m thingy?
	int res = linkm_open(self->usbDevice);
	if(res != 0) { // is 0 the no error return? or is 1?
		// throw an error
		self->usbDevice = NULL;
		doLinkMError("Some kind of LinkM error?");
		return -1;
	}

	return 0;
}

static PyObject* LinkMObj_close(linkmpy_LinkMObj* self) {
	if(self->usbDevice) {
		linkm_close(self->usbDevice);
		self->usbDevice = NULL; // should we delete it first?
	}

	Py_RETURN_NONE;
}

static PyObject* LinkMObj_command(linkmpy_LinkMObj* self, PyObject *args) {
	if(self->usbDevice) {
		int cmd;
		int bytes_send;
		int bytes_recv;
		char* send_buff;
		int send_buf_len;
		if (! PyArg_ParseTuple(args, "iiis#", &cmd, &bytes_send, &bytes_recv, &send_buff, &send_buf_len) )
		{
			Py_RETURN_NONE;
		}
		// what if bytes_send does not match the length of the provided string?
		int res = linkm_command(self->usbDevice, 
                  cmd, 
                  bytes_send, 
                  bytes_recv,
                  send_buff, 
                  self->recv_buf);
		// is res an error code that we should check?
		return Py_BuildValue("is#", res, self->recv_buf, BUFFER_SIZE);
	}

	Py_RETURN_NONE;
}

static PyObject* LinkMObj_error_msg(linkmpy_LinkMObj* self, PyObject *args) {
	if(self->usbDevice) {
		int inputErrorCode = 0;
		if (! PyArg_ParseTuple(args, "i", &inputErrorCode) )
		{
			Py_RETURN_NONE;
		}
		char* ret = linkm_error_msg(inputErrorCode);
		// assuming linkm_error_msg returns null terminated string
		return Py_BuildValue("s", ret);
	}

	Py_RETURN_NONE;
}

	

static PyMethodDef LinkMObj_methods[] = {
	{"close", (PyCFunction)LinkMObj_close, METH_NOARGS,
	 "Close the linkm object"},
	{"command", (PyCFunction)LinkMObj_command, METH_VARARGS,
	 "Send a command to the object"},
	{"error_msg", (PyCFunction)LinkMObj_error_msg, METH_VARARGS,
	 "I don't know what this does"},
	{NULL}  /* Sentinel */
};

static PyTypeObject linkmpy_LinkMObjType = {
	PyObject_HEAD_INIT(NULL)
	0,                         			/*ob_size*/
	"linkmpy.Camera",             		/*tp_name*/
	sizeof(linkmpy_LinkMObj), 		/*tp_basicsize*/
	0,                         			/*tp_itemsize*/
	(destructor)LinkMObj_dealloc,   /*tp_dealloc*/
	0,                         			/*tp_print*/
	0,                         			/*tp_getattr*/
	0,                         			/*tp_setattr*/
	0,                         			/*tp_compare*/
	0,                         			/*tp_repr*/
	0,                         			/*tp_as_number*/
	0,                         			/*tp_as_sequence*/
	0,                         			/*tp_as_mapping*/
	0,                         			/*tp_hash */
	0,                         			/*tp_call*/
	0,                         			/*tp_str*/
	0,                         			/*tp_getattro*/
	0,                         			/*tp_setattro*/
	0,                         			/*tp_as_buffer*/
	Py_TPFLAGS_DEFAULT,        			/*tp_flags*/
	"LinkM objects",          			/*tp_doc*/
	0,		               				/* tp_traverse */
	0,		               				/* tp_clear */
	0,		               				/* tp_richcompare */
	0,		               				/* tp_weaklistoffset */
	0,		               				/* tp_iter */
	0,		               				/* tp_iternext */
	LinkMObj_methods,      			/* tp_methods */
	0, /*LinkMPyObj_members,*/      	/* tp_members */
	0,                         			/* tp_getset */
	0,                         			/* tp_base */
	0,                         			/* tp_dict */
	0,                         			/* tp_descr_get */
	0,                         			/* tp_descr_set */
	0,                         			/* tp_dictoffset */
	(initproc)LinkMObj_init,		/* tp_init */
	0,                         			/* tp_alloc */
	LinkMObj_new,          			/* tp_new */
};


static PyObject *
linkm_version(PyObject *self, PyObject *args)
{
	std::string versionString = "unknown";
	return Py_BuildValue("s", versionString.c_str());
}

static PyMethodDef LinkMPyMethods[] = {
	{"version",  linkm_version, METH_VARARGS,
	 "Return a version string."},
	{NULL, NULL, 0, NULL}        /* Sentinel */
};

void addIntConstant(PyObject* dest, const char* constName, unsigned int constVal) 
{
	PyObject* tempVal = Py_BuildValue("i", constVal);	
	PyModule_AddObject(dest, constName, tempval);
}

void addEnums(PyObject* dest) 
{
	addIntConstant(dest, "IDENT_VENDOR_NUM", IDENT_VENDOR_NUM);
	addIntConstant(dest, "IDENT_PRODUCT_NUM", IDENT_PRODUCT_NUM);
	addIntConstant(dest, "IDENT_VENDOR_STRING", IDENT_VENDOR_STRING);
	addIntConstant(dest, "IDENT_PRODUCT_STRING", IDENT_PRODUCT_STRING);
	addIntConstant(dest, "START_BYTE", START_BYTE);
	addIntConstant(dest, "LINKM_CMD_NONE", LINKM_CMD_NONE);
	addIntConstant(dest, "LINKM_CMD_I2CTRANS", LINKM_CMD_I2CTRANS);
	addIntConstant(dest, "LINKM_CMD_I2CWRITE", LINKM_CMD_I2CWRITE);
	addIntConstant(dest, "LINKM_CMD_I2CREAD", LINKM_CMD_I2CREAD);
	addIntConstant(dest, "LINKM_CMD_I2CSCAN", LINKM_CMD_I2CSCAN);
	addIntConstant(dest, "LINKM_CMD_I2CCONN", LINKM_CMD_I2CCONN);
	addIntConstant(dest, "LINKM_CMD_I2CINIT", LINKM_CMD_I2CINIT);
	addIntConstant(dest, "LINKM_CMD_VERSIONGET", LINKM_CMD_VERSIONGET);
	addIntConstant(dest, "LINKM_CMD_STATLEDSET", LINKM_CMD_STATLEDSET);
	addIntConstant(dest, "LINKM_CMD_STATLEDGET", LINKM_CMD_STATLEDGET);
	addIntConstant(dest, "LINKM_CMD_PLAYSET", LINKM_CMD_PLAYSET);
	addIntConstant(dest, "LINKM_CMD_PLAYGET", LINKM_CMD_PLAYGET);
	addIntConstant(dest, "LINKM_CMD_EESAVE", LINKM_CMD_EESAVE);
	addIntConstant(dest, "LINKM_CMD_EELOAD", LINKM_CMD_EELOAD);
	addIntConstant(dest, "LINKM_CMD_GOBOOTLOAD", LINKM_CMD_GOBOOTLOAD);
	addIntConstant(dest, "LINKM_ERR_NONE", LINKM_ERR_NONE);
	addIntConstant(dest, "LINKM_ERR_BADSTART", LINKM_ERR_BADSTART);
	addIntConstant(dest, "LINKM_ERR_BADARGS,", LINKM_ERR_BADARGS,);
	addIntConstant(dest, "LINKM_ERR_I2C,", LINKM_ERR_I2C,);
	addIntConstant(dest, "LINKM_ERR_I2CREAD,", LINKM_ERR_I2CREAD,);
	addIntConstant(dest, "LINKM_ERR_NOTOPEN", LINKM_ERR_NOTOPEN);
}

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC
initlinkmpy(void)
{
	PyObject* m;

	linkmpy_LinkMObjType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&linkmpy_LinkMObjType) < 0)
		return;

	m = Py_InitModule3("linkmpy", LinkMPyMethods,
					   "Python interface to the PointGrey flycapture sdk.");

	Py_INCREF(&linkmpy_LinkMObjType);
	PyModule_AddObject(m, "USBLink", (PyObject *)&linkmpy_LinkMObjType);

	// add the c++ defined enums+defines to the module
	addEnums(m);

	// PyErr_NewException requires a non-constant char* for the name, 
	// probably due to an oversight, hence this strange little dance
	char errName[] = "linkmpy.LinkMError\0";
	LinkMError = PyErr_NewException(errName, NULL, NULL);
	Py_INCREF(LinkMError);
	PyModule_AddObject(m, "LinkMError", LinkMError);
}

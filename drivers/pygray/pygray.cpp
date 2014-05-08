#include <Python.h>
#include <string>
#include <sstream>
#include "FlyCapture2.h"
#include <iostream>

using namespace FlyCapture2;

typedef struct {
    PyObject_HEAD
    Camera* cam;
    bool useColor;
    CameraInfo* camInfo;
} pygray_CameraObject;

static PyObject* CameraError;

void doCameraError(Error& err) {
	err.PrintErrorTrace();
	PyErr_SetString(CameraError, err.GetDescription());
}

void printGuid(PGRGuid& guid) {
  std::cout << guid.value[0] << "|"
	    << guid.value[1] << "|"
	    << guid.value[2] << "|"
	    << guid.value[3] << std::endl;
}

std::string guidToString(PGRGuid& guid) {
    std::stringstream ss;
    ss << std::hex << guid.value[0];
    ss << std::hex << guid.value[1];
    ss << std::hex << guid.value[2];
    ss << std::hex << guid.value[3];
    return ss.str();
}

unsigned int hexStrToUInt(const std::string& src) {
  std::stringstream ss(src);
  unsigned int ret;
  ss >> std::hex >> ret;
  return ret;
}

void stringToGuid(const char* raws, PGRGuid& guid) {
  std::string s(raws);
  guid.value[0] = hexStrToUInt(s.substr( 0, 8));
  guid.value[1] = hexStrToUInt(s.substr( 8, 8));
  guid.value[2] = hexStrToUInt(s.substr(16, 8));
  guid.value[3] = hexStrToUInt(s.substr(24, 8));
    //sscanf(s, "%x%x%x%x", &(guid.val[0]), &(guid.val[1]), &(guid.val[2]), &(guid.val[3]));
}

// Have to declare anything that is directly passed into python with extern C
extern "C" {
    static void PygrayCamera_dealloc(pygray_CameraObject* self);
    static PyObject * PygrayCamera_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
    static int PygrayCamera_init(pygray_CameraObject* self, PyObject* args, PyObject* kwds);
    PyMODINIT_FUNC initpygray(void);
    //DL_EXPORT(void) initflp();
}

static void
PygrayCamera_dealloc(pygray_CameraObject* self)
{
	if(self->cam) {
		self->cam->StopCapture();
		self->cam->Disconnect();
	}

	delete self->cam;
	delete self->camInfo;

    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
PygrayCamera_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pygray_CameraObject *self;

    self = (pygray_CameraObject*)type->tp_alloc(type, 0);
    if (self != NULL) {
    	self->cam = NULL;
    	self->camInfo = NULL;
	self->useColor = false;
    }

    return (PyObject *)self;
}

static int
PygrayCamera_init(pygray_CameraObject* self, PyObject* args, PyObject* kwds)
{
    PGRGuid guid;
    Error error;

    char* tempstr;

    if (! PyArg_ParseTuple(args, "s", &tempstr) )
    {
        return -1; 
    }
    stringToGuid(tempstr, guid);
    printGuid(guid);

    self->cam = new Camera;
    self->camInfo = new CameraInfo;

    // Connect to a camera
    error = self->cam->Connect(&guid);
    if (error != PGRERROR_OK)
    {
    	doCameraError(error);
        delete self->cam;
        delete self->camInfo;
        self->cam = NULL;
        self->camInfo = NULL;
        return -1;
    }

    // Get the camera information
    error = self->cam->GetCameraInfo(self->camInfo);
    if (error != PGRERROR_OK)
    {
    	doCameraError(error);
        delete self->cam;
        delete self->camInfo;
        self->cam = NULL;
        self->camInfo = NULL;
        return -1;
    }

    return 0;
}

static PyObject* PygrayCamera_setcolormode(pygray_CameraObject* self, 
					   PyObject *args) {
  if(self->cam) {
    int colorMode = 0;
    if (! PyArg_ParseTuple(args, "i", &colorMode) )
    {
      Py_RETURN_NONE;
    }
    self->useColor = (colorMode > 0);
  }

  Py_RETURN_NONE;
}

static PyObject* PygrayCamera_start(pygray_CameraObject* self) {
	if(self->cam) {
		Error error = self->cam->StartCapture();
		if (error != PGRERROR_OK) {
			doCameraError(error);
			return NULL;
		}
	}

	Py_RETURN_NONE;
}

static PyObject* PygrayCamera_stop(pygray_CameraObject* self) {
	if(self->cam) {
		Error error = self->cam->StopCapture();
		if (error != PGRERROR_OK) {
			doCameraError(error);
			return NULL;
		}
	}

	Py_RETURN_NONE;
}

static PyObject* PygrayCamera_getframestr(pygray_CameraObject* self) {
	if(self->cam) {
		Image rawImage;
		Error error = self->cam->RetrieveBuffer( &rawImage );
		if (error != PGRERROR_OK)
        {
            doCameraError(error);
            return NULL;
        }

        // Create a converted image
        Image convertedImage;

        // Convert the raw image (BGR because that's what opencv likes)
	if(self->useColor) {
	  error = rawImage.Convert( PIXEL_FORMAT_BGR, &convertedImage );
	} else {
	  error = rawImage.Convert( PIXEL_FORMAT_MONO8, &convertedImage );
	}

        if (error != PGRERROR_OK)
        {
            doCameraError(error);
            return NULL;
        }

        // return a python tuple
        int imcols = convertedImage.GetCols();
        int imrows = convertedImage.GetRows();
        int stride = convertedImage.GetStride();
        int datasize = convertedImage.GetDataSize();
	
        return Py_BuildValue("iiiis#", imrows, imcols, stride, datasize, (char*)(convertedImage.GetData()), datasize);
	} else {
	  Py_RETURN_NONE;
	}
}

static PyObject* PygrayCamera_getinfo(pygray_CameraObject* self) {
	PyObject *d = PyDict_New();
	if(self->camInfo) {
		CameraInfo* info = self->camInfo;
	    PyDict_SetItemString(d, "serialNumber", PyInt_FromLong(info->serialNumber));
	    PyDict_SetItemString(d, "modelName", PyString_FromString(info->modelName));
	    PyDict_SetItemString(d, "vendorName", PyString_FromString(info->vendorName));
	    PyDict_SetItemString(d, "sensorInfo", PyString_FromString(info->sensorInfo));
	    PyDict_SetItemString(d, "sensorResolution", PyString_FromString(info->sensorResolution));
	    PyDict_SetItemString(d, "firmwareVersion", PyString_FromString(info->firmwareVersion));
	    PyDict_SetItemString(d, "firmwareBuildTime", PyString_FromString(info->firmwareBuildTime));
	}
    return d;
}

static PyMethodDef PygrayCamera_methods[] = {
    {"start", (PyCFunction)PygrayCamera_start, METH_NOARGS,
     "Start capturing from the camera"},
    {"stop", (PyCFunction)PygrayCamera_stop, METH_NOARGS,
     "Stop capturing from the camera"},
    {"getFrameStr", (PyCFunction)PygrayCamera_getframestr, METH_NOARGS,
	 "Grab a frame from the camera as a python string"},
	{"getInfo", (PyCFunction)PygrayCamera_getinfo, METH_NOARGS,
	 "Get information about the camera."},
    {"setColorMode", (PyCFunction)PygrayCamera_setcolormode, METH_VARARGS,
     "Set whether to return color images."},
    {NULL}  /* Sentinel */
};

// no members
//static PyMemberDef PygrayCamera_members[] = {
//    {NULL}  /* Sentinel */
//};

static PyTypeObject pygray_CameraType = {
    PyObject_HEAD_INIT(NULL)
    0,                         			/*ob_size*/
    "pygray.Camera",             		/*tp_name*/
    sizeof(pygray_CameraObject), 		/*tp_basicsize*/
    0,                         			/*tp_itemsize*/
    (destructor)PygrayCamera_dealloc,   /*tp_dealloc*/
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
    "Camera objects",          			/*tp_doc*/
    0,		               				/* tp_traverse */
    0,		               				/* tp_clear */
    0,		               				/* tp_richcompare */
    0,		               				/* tp_weaklistoffset */
    0,		               				/* tp_iter */
    0,		               				/* tp_iternext */
    PygrayCamera_methods,      			/* tp_methods */
    0, /*PygrayCamera_members,*/      			/* tp_members */
    0,                         			/* tp_getset */
    0,                         			/* tp_base */
    0,                         			/* tp_dict */
    0,                         			/* tp_descr_get */
    0,                         			/* tp_descr_set */
    0,                         			/* tp_dictoffset */
    (initproc)PygrayCamera_init,		/* tp_init */
    0,                         			/* tp_alloc */
    PygrayCamera_new,          			/* tp_new */
};


std::string getPointGrayVersionString()
{
    FC2Version fc2Version;
    Utilities::GetLibraryVersion( &fc2Version );
    std::stringstream ss;
    ss << fc2Version.major << "."
       << fc2Version.minor << "."
       << fc2Version.type  << "."
       << fc2Version.build;
    return ss.str();
}

static PyObject *
pygray_version(PyObject *self, PyObject *args)
{
	std::string versionString = getPointGrayVersionString();
    return Py_BuildValue("s", versionString.c_str());
}

static PyObject *
pygray_listcams(PyObject *self, PyObject *args)
{
	Error error;
    BusManager busMgr;
    unsigned int numCameras;
    error = busMgr.GetNumOfCameras(&numCameras);
    if (error != PGRERROR_OK)
    {
        doCameraError(error);
        return NULL;
    }

    printf( "Number of cameras detected: %u\n", numCameras );

    PyObject* ret = PyList_New((Py_ssize_t)numCameras);
    for (unsigned int i=0; i < numCameras; i++)
    {
        PGRGuid guid;
        error = busMgr.GetCameraFromIndex(i, &guid);
        if (error != PGRERROR_OK)
        {
	        doCameraError(error);
	        return NULL;
        }
	printGuid(guid);
        std::string guidStr = guidToString(guid);
        PyList_SetItem(ret, i, 
        	Py_BuildValue("s", guidStr.c_str()));
    }

    return ret;
}

static PyMethodDef PygrayMethods[] = {
    {"version",  pygray_version, METH_VARARGS,
     "Return the flycapture sdk version as a string."},
    {"listcams", pygray_listcams, METH_VARARGS,
 	 "Get a list of connected cameras."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC
initpygray(void)
{
    PyObject* m;

    pygray_CameraType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&pygray_CameraType) < 0)
        return;

    m = Py_InitModule3("pygray", PygrayMethods,
                       "Python interface to the PointGrey flycapture sdk.");

    Py_INCREF(&pygray_CameraType);
    PyModule_AddObject(m, "Camera", (PyObject *)&pygray_CameraType);

    // PyErr_NewException requires a non-constant char* for the name, 
    // probably due to an oversight, hence this strange little dance
    char errName[] = "pygray.cameraError\0";
    CameraError = PyErr_NewException(errName, NULL, NULL);
    Py_INCREF(CameraError);
    PyModule_AddObject(m, "cameraError", CameraError);
}

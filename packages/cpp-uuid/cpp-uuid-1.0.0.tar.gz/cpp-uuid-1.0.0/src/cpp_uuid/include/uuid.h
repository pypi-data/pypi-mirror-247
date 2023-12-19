#ifndef UUID_UUID_H
#define UUID_UUID_H

#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "uuid_v4.h"

PyObject *Python_uuid4(PyObject * self, PyObject * args);
PyObject *Python_UUID(PyObject * self, PyObject * args);

extern PyTypeObject UUIDType;


typedef struct UUID_object_struct UUID_struct;
struct UUID_object_struct {
    PyObject_HEAD
    UUIDv4::UUID uuid;
};


#endif //UUID_UUID_H

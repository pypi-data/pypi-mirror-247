#include <iostream>
#include <string>

#include "include/uuid.h"

UUIDv4::UUIDGenerator<std::mt19937_64> uuidGenerator;

static PyMethodDef moduleFunctions[] = {
        {
                .ml_name = "UUID",
                .ml_meth = &Python_UUID,
                .ml_flags = METH_VARARGS,
                .ml_doc =
                "Create a UUID from either a string or a string of 16 bytes.\n\n"
                "When a string of hex digits is given, curly braces, hyphens, and a URN prefix are all optional.\n\n",
        },
        {
                .ml_name = "uuid4",
                .ml_meth = Python_uuid4,
                .ml_flags = METH_NOARGS,
                .ml_doc = "Generate a random UUID v4.",
        },
        {nullptr, nullptr, 0, nullptr},
};

/* Module Definition */
static struct PyModuleDef moduleDefinitions{
        PyModuleDef_HEAD_INIT,
        "cpp_uuid",
        "UUID objects (universally unique identifiers) according to RFC 4122 written in C.\n"
        "This module replaces uuid4() function and UUID object (class UUID) from Python-builtin library.",
        -1,
        moduleFunctions,
};

static PyObject *Python_UUID_new(PyTypeObject *type, PyObject *args, PyObject *kwargs) {
    UUID_struct *self;
    self = (UUID_struct *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

static int Python_UUID_init(UUID_struct *self, PyObject *args, PyObject *kwargs) {
    const char *kwargs_list[] = {"hex", "bytes", nullptr};
    const char *arg_hex = nullptr;
    const char *arg_bytes = nullptr;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|sy", const_cast<char **>(kwargs_list), &arg_hex, &arg_bytes))
        return -1;

    if (arg_hex != nullptr) {
        self->uuid = UUIDv4::UUID::fromStrFactory(arg_hex);

    } else if (arg_bytes != nullptr) {
        UUIDv4::UUID uuid((uint8_t *) arg_bytes);
        self->uuid = uuid;

    } else {
        self->uuid = uuidGenerator.getUUID();
    }

    return 0;
}

static PyObject *Python_UUID_str(UUID_struct *self, PyObject *args) {
    return PyUnicode_FromString(self->uuid.str().c_str());
}

static Py_hash_t *Python_UUID_hash(UUID_struct *self) {
    return reinterpret_cast<Py_hash_t *>(self->uuid.hash());
}

static void class_dealloc(UUID_struct *self) {
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *Python_UUID_bytes(UUID_struct *self, char *name) {
    return Py_BuildValue("y#", &self->uuid, 16);
}

static PyGetSetDef Python_UUID_getset[] = {
        {
                .name = "bytes",
                .get = (getter) Python_UUID_bytes,
                .set = nullptr,
                .doc = "UUID as a 16-byte string.",
                .closure = nullptr,
        },
        {nullptr},
};

static PyObject *Python_UUID_compare(UUID_struct *self, UUID_struct *other, int op) {
    PyObject * result;
    UUIDv4::UUID other_uuid = other->uuid;

    if (strcmp(self->ob_base.ob_type->tp_name, other->ob_base.ob_type->tp_name) != 0) {
        PyObject * data = PyObject_Str((PyObject *) other);
        PyObject * str = PyUnicode_AsEncodedString(data, "utf-8", "~E~");
        const char *bytes = PyBytes_AS_STRING(str);
        other_uuid = UUIDv4::UUID::fromStrFactory(bytes);
        Py_XDECREF(data);
        Py_XDECREF(str);
    }

    int c;
    switch (op) {
        case Py_LT:
            c = self->uuid < other_uuid;
            break;
        case Py_LE:
            c = self->uuid <= other_uuid;
            break;
        case Py_EQ:
            c = self->uuid == other_uuid;
            break;
        case Py_NE:
            c = self->uuid != other_uuid;
            break;
        case Py_GT:
            c = self->uuid > other_uuid;
            break;
        case Py_GE:
            c = self->uuid >= other_uuid;
            break;
    }
    result = c ? Py_True : Py_False;
    Py_INCREF(result);
    return result;
}

PyTypeObject UUIDType = {
        .ob_base = PyVarObject_HEAD_INIT(nullptr, 0)
        .tp_name = "cpp_uuid.UUID",
        .tp_basicsize = sizeof(UUID_struct),
        .tp_itemsize = 0,
        .tp_dealloc = (destructor) class_dealloc,
        .tp_repr = (reprfunc) Python_UUID_str,
        .tp_hash = (hashfunc) Python_UUID_hash,
        .tp_str = (reprfunc) Python_UUID_str,
        .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
        .tp_doc = PyDoc_STR(
                          "Instances of the UUID class represent UUIDs v4.\n\n"
                          "UUID objects are immutable, hashable, and usable as dictionary keys.\n"
                          "UUID objects have single read-only attribute `bytes`."
                  ),
        .tp_richcompare = (richcmpfunc) Python_UUID_compare,
        .tp_getset = Python_UUID_getset,
        .tp_init = (initproc) Python_UUID_init,
        .tp_new = (newfunc) Python_UUID_new,
};

/* Module Initialization */
PyMODINIT_FUNC PyInit_cpp_uuid(void) {
    Py_Initialize();
    PyObject * pModule = PyModule_Create(&moduleDefinitions);

    if (PyType_Ready(&UUIDType) < 0)
        return nullptr;

    Py_INCREF(&UUIDType);
    PyModule_AddObject(pModule, "UUID", (PyObject *) &UUIDType);
    return pModule;
}

PyObject *Python_uuid4(PyObject * self, PyObject * args) {
    UUIDv4::UUID uuid = uuidGenerator.getUUID();
    PyObject * value = PyUnicode_FromString(uuid.str().c_str());
    PyObject * obj = PyObject_CallFunction((PyObject *) &UUIDType, "s", value);
    Py_DECREF(value);
    return (PyObject *) obj;
}

PyObject *Python_UUID(PyObject * self, PyObject * args) {
    Py_RETURN_NONE;
}

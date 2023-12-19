// In all C files, include its corresponding header file in the very first line.
// No need to include <Python.h> as we did that already in the header file.
// Just make sure that <Python.h> is included BEFORE any other header file.
#include "match.h"
#include "FMM/src/driver.h"

// Our function implementation
// Our modified function implementation to accept two lists
PyObject *match_wrapper(PyObject *self, PyObject *args)
{
    PyObject *list1;
    PyObject *list2;
    PyObject *list3;
    PyObject *list4;

    // Parse the input arguments, expecting two lists of integers
    if (!PyArg_ParseTuple(args, "OOOO", &list1, &list2, &list3, &list4))
    {
        return NULL;
    }

    // Check if the input is a list
    if (!PyList_Check(list1) || !PyList_Check(list2) || !PyList_Check(list3) || !PyList_Check(list4))
    {
        PyErr_SetString(PyExc_TypeError, "All inputs must be lists");
        return NULL;
    }

    // return match(list1, list2);
    match(list1, list2, list3, list4);
    // return list4;
    Py_RETURN_NONE;
}

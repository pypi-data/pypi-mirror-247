# [MIT] Copyright (c) 2023 Michel Novus

import json
import unittest
from typing import Union, Any

PyCoreObject = Union[dict[str, Any], list, str, int, float, bool, None]
"""dict and list types recursively accept only PyCoreObject type values.

Look is_pycoreobject function to check types.
"""


def is_pycoreobject(object: Any) -> bool:
    """Check 'object' is some kind of PyCoreObject.

    Return True if 'object' is a some kind of
    PyCoreObject, False otherwise.
    """
    if isinstance(object, (str, int, float, bool, type(None))):
        return True
    elif isinstance(object, dict):
        for key in object.keys():
            if not isinstance(key, str):
                return False
        for value in object.values():
            object_is_valid = is_pycoreobject(value)
            if not object_is_valid:
                return False
        return True
    elif isinstance(object, list):
        for value in object:
            object_is_valid = is_pycoreobject(value)
            if not object_is_valid:
                return False
        return True
    else:
        return False


def serialize(data: PyCoreObject, strict: bool = True) -> bytes:
    """Serializes 'data' to a compact JSON string bytes.

    ### Exceptions:
    - TypeError: if data is not PyCoreObject
    """
    if strict and not is_pycoreobject(data):
        raise TypeError(f"data type is not a PyCoreObject")
    json_data = json.dumps(data, separators=(",", ":"))
    return json_data.encode("utf-8")


def deserialize(data: bytes, strict: bool = True) -> PyCoreObject:
    """Deserializes 'data' JSON string bytes to a Python Core Object.

    ### Exceptions:
    - JSONDecodeError: if data is not a valid JSON bytes
    - TypeError: if data is not PyCoreObject
    """
    json_data = json.loads(data)
    if strict and not is_pycoreobject(json_data):
        raise TypeError(f"data type is not a PyCoreObject")
    return json_data


# ----------------------------------------------------------------------


class _TestSerializer(unittest.TestCase):
    def setUp(self):
        self._python_data = (
            {"DA": 12, "TO": None, "22": True, "KEY": {"b": None, "0.1": True}},
            ["data", "chik", "foo", 922, None, True, False, "nada"],
            "Ejemplo de cadena",
            4033927,
            123.9281,
            True,
            False,
            None,
        )
        self._serialized_data = (
            b'{"DA":12,"TO":null,"22":true,"KEY":{"b":null,"0.1":true}}',
            b'["data","chik","foo",922,null,true,false,"nada"]',
            b'"Ejemplo de cadena"',
            b"4033927",
            b"123.9281",
            b"true",
            b"false",
            b"null",
        )

    def test_serialize(self):
        for pydata, serial in zip(self._python_data, self._serialized_data):
            self.assertEqual(
                serialize(pydata), serial, "Error en la codificación JSON."
            )
        self.assertRaises(TypeError, serialize, {22: None})
        self.assertRaises(TypeError, serialize, b"error")

    def test_deserialize(self):
        for pydata, serial in zip(self._python_data, self._serialized_data):
            self.assertEqual(
                deserialize(serial), pydata, "Error en la codificación JSON."
            )
        self.assertRaises(json.JSONDecodeError, deserialize, b"algo")
        self.assertRaises(TypeError, deserialize, {22: None})

    def test_is_pycoreobject(self):
        for value in self._python_data:
            self.assertTrue(is_pycoreobject(value))
        self.assertTrue(is_pycoreobject("cadena de python"))
        self.assertTrue(is_pycoreobject(239))
        self.assertTrue(is_pycoreobject(0.213))
        self.assertTrue(is_pycoreobject(True))
        self.assertTrue(is_pycoreobject(False))
        self.assertTrue(is_pycoreobject(None))

        self.assertTrue(is_pycoreobject([]))
        self.assertTrue(is_pycoreobject([22, "pepe", None, True]))
        self.assertTrue(
            is_pycoreobject([22, [93, "anidado", ["otra anidación", True]]])
        )

        self.assertTrue(is_pycoreobject({}))
        self.assertTrue(
            is_pycoreobject(
                {
                    "cadena": 12,
                    "otra": [1, 2, [4, 3, 2]],
                    "anidado": {
                        "cadena anidada": 99,
                        "pepe": True,
                        "rey": None,
                        "otro diccionario": {"más anidado": 3, "nada": False},
                    },
                }
            )
        )

        self.assertFalse(is_pycoreobject(callable))
        self.assertFalse(is_pycoreobject(b"soy una cadena de bytes"))
        self.assertFalse(is_pycoreobject({220: None}))

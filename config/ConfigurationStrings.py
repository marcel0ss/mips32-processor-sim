MIPS32_STANDARD_CONFIG = '''{
    "dmemory": {
        "capacity": 1024,
        "start": "RANDOM",
        "file": ""
    },

    "imemory": {
        "capacity": 128,
        "start": "FILE",
        "file": "config/mem.txt"
    },

    "cache": [
        {
            "capacity": 32,
            "assocativity": 2,
            "line_size": 16
        },
        {
            "capacity": 64,
            "assocativity": 2,
            "line_size": 16
        }
    ],

    "architecture": 32,
    "endianness": "LITTLE"
}'''

# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from seaplane_framework.api.paths.object import Api

from seaplane_framework.api.paths import PathValues

path = PathValues.OBJECT
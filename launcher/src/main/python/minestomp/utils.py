
from java.util.function import Consumer
from net.minestom.server.instance.block import Block
from net.minestom.server.item import Material
from net.minestom.server.instance.generator import Generator

# Hacks due to jython failing to access interface fields
def block_type(type): return Block.fromNamespaceId("minecraft:"+type)
def material_type(type): return Material.fromNamespaceId("minecraft:"+type)

# Syntactic sugaring so Python lambdas will work with Java
# recievers.
class jc(Consumer):
    def __init__(self, fn):
        self.accept=fn

# This helps for multiline lambda via:
# jcv(lambda x:[first(), second(), third()])
class jcv(Consumer):
    def __init__(self, fn):
        self.fn=fn
    def accept(self, parm):
        self.fn(parm)
        return None

# Minestom API specific sugaring
class Gen(Generator):
    def __init__(self, fn):
        self.fn=fn

    def generate(self, unit):
        self.fn(unit)

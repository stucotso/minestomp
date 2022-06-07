
from java.util.function import Consumer
from net.minestom.server.instance.block import Block
from net.minestom.server.item import Material
from net.minestom.server.instance.generator import Generator

def testUtils(): print ("testUtils")

# Hacks due to jython failing to access interface fields of classes
def block_type(type): return Block.fromNamespaceId("minecraft:"+type)
def material_type(type): return Material.fromNamespaceId("minecraft:"+type)

class jc(Consumer):
    def __init__(self, fn):
        self.accept=fn

class jcv(Consumer):
    def __init__(self, fn):
        self.fn=fn
    def accept(self, parm):
        self.fn(parm)
        return None

class Gen(Generator):
    def __init__(self, fn):
        self.fn=fn
    def generate(self, unit):
        self.fn(unit)
        #unit.modifier().fillHeight(0, 40, block_type("stone"))
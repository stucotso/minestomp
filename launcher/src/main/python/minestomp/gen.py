from de.articdive.jnoise.generators.noise_parameters.interpolation import Interpolation
from de.articdive.jnoise.generators.noisegen.opensimplex import FastSimplexNoiseGenerator
from de.articdive.jnoise.generators.noisegen.perlin import PerlinNoiseGenerator
from de.articdive.jnoise.pipeline import JNoise
from net.minestom.server.coordinate import Point
from net.minestom.server.coordinate import Vec
from net.minestom.server.instance import Chunk
from net.minestom.server.instance.block import Block
from net.minestom.server.instance.generator import GenerationUnit
from net.minestom.server.instance.generator import Generator
from org.jetbrains.annotations import NotNull

import random

from minestomp.utils import *

class TestGen (Generator):

    treeNoise = JNoise.newBuilder() \
        .fastSimplex(FastSimplexNoiseGenerator.newBuilder().setSeed(123).build()) \
        .scale(999) \
        .build()

    jNoise = JNoise.newBuilder() \
        .perlin(PerlinNoiseGenerator.newBuilder().setSeed(123).setInterpolation(Interpolation.LINEAR).build()) \
        .scale(0.4).build()

    def getHeight(self, x, z):
        preHeight = (TestGen.jNoise.evaluateNoise(x / 44.0, z / 44.0) + 1.0) / 2.0
        #print preHeight,
        #return int((( preHeight * 6 if preHeight > 0 else preHeight * 4.0) + 64.0))
        #return int( preHeight * 100.0 if preHeight > 0.5 else preHeight * 50.0)
        return int(preHeight * preHeight * preHeight * 100.0)

    def generate(self, unit):
        water_height = 10
        start = unit.absoluteStart()
        #print "gen:", start
        for x in range(Chunk.CHUNK_SIZE_X):
            for z in range(Chunk.CHUNK_SIZE_Z):
                pos=None
                
                absX = start.blockX() + x
                absZ = start.blockZ() + z
                height = self.getHeight(absX, absZ)
                pos = Vec(absX, height, absZ)
                
                posp1 = pos.add(1, 0, 1)

                # Underground
                unit.modifier().fill(pos.withY(0), posp1, block_type("stone"))
                unit.modifier().fill(pos.withY(pos.y() - 7), posp1, block_type("dirt"))                
                unit.modifier().fill(pos.withY(0), posp1.withY(1), block_type("bedrock"))
                
                if (pos.y() < water_height): # Water
                    unit.modifier().fill(pos, posp1.withY(water_height), block_type("water"))
                    #unit.modifier().fill(pos.withY(0), posp1, block_type("air"))
                    #return
                else: # Regular terrain                    
                    unit.modifier().fill(pos.withY(pos.y() - 1), posp1, block_type("grass_block"))          
                
                    if (TestGen.treeNoise.evaluateNoise(pos.x(), pos.z()) > 0.95):
                        TreePopulator.populate(pos, unit)

class TreePopulator:
    @staticmethod
    def genTree(origin, unit, setter):
        tree_height=int((random.random()*15) + 3)
        tree_crown_height=int(tree_height * 0.45)
        tree_crown_radius=int((random.random()*5) + 2)

        for y in range(tree_height):
            setter.setBlock(origin.add(0, y, 0), block_type("oak_log"))
        
        for y in range(tree_crown_height, tree_height+1):
            for x in range(-tree_crown_radius, tree_crown_radius):
                for z in range(-tree_crown_radius, tree_crown_radius):
                    if (not (x == 0 and z == 0)) and random.random() < 0.4:
                        setter.setBlock(origin.add(x, y, z), block_type("oak_leaves"))

    @staticmethod
    def populate(origin, unit):
        unit.fork(jcv(lambda setter: [
            TreePopulator.genTree(origin, unit, setter)
        ]))  
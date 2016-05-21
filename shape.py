""" Create shapes in a minecraft world """

import sys
import math

import mcpi
from mc import *

Blocks = {}
for key, value in mcpi.block.__dict__.iteritems():
    key = key.replace('HARDENED_CLAY_STAINED', 'STAINED_HARDENED_CLAY')
    key = key.replace('REDSTONE_LAMP_INACTIVE', 'REDSTONE_LAMP')
    key = key.replace('_SPRUCE', '')
    key = key.replace('_DECAYABLE', '')
    key = key.replace('_PERMANENT', '')
    key = key.replace('WOOD_BUTTON', 'WOODEN_BUTTON')
    key = key.replace('GLOWSTONE_BLOCK', 'GLOWSTONE')
    key = key.replace('SNOW_BLOCK', 'SNOW')
    key = key.replace('SUGAR_CANE', 'REEDS')
    key = key.replace('DOOR_IRON', 'IRON_DOOR')
    key = key.replace('FURNACE_INACTIVE', 'FURNACE')
    key = key.replace('MOSS_STONE', 'MOSSY_COBBLESTONE')
    key = key.replace('STONE_SLAB_DOUBLE', 'DOUBLE_STONE_SLAB')
    key = key.replace('COBWEB', 'WEB')
    key = key.replace('LAZULI', '')
    key = key.replace('WOOD_PLANKS', 'PLANKS')
    key = key.replace('STONE_BRICK', 'STONEBRICK')
    key = key.replace('', '')
    Blocks[key] = value

# add my own block names here
Blocks.update({
    #'LAVA': Block(10),
    })


def lookupBlock(blockName):
    """ Look up block name string in name list
        data value (e.g. color) override may be appended to the end
        e.g. stained_hardened_clay_10
        Note: block name lookup is case insensitive
    """
    blockName = blockName.upper()
    try:
        try:
            name, data = blockName.rsplit('_', 1)
        except ValueError:
            return Blocks[blockName]
        else:
            try:
                data = int(data)
            except ValueError:
                return Blocks[blockName]
            return Block(Blocks[name].id, data)
    except KeyError:
        print 'Invalid block name:', blockName
        sys.exit()

def smallRing(center, r, block):
    """ Create a ring around center of radius r blocks using block type """

    block = lookupBlock(block)
    x = r
    z = 0
    y = 0
    while z < x:
        mc.setBlock(center.x + x, center.y + y, center.z + z, block)
        mc.setBlock(center.x + z, center.y + y, center.z + x, block)
        mc.setBlock(center.x - x, center.y + y, center.z - z, block)
        mc.setBlock(center.x - z, center.y + y, center.z - x, block)
        mc.setBlock(center.x + x, center.y + y, center.z - z, block)
        mc.setBlock(center.x + z, center.y + y, center.z - x, block)
        mc.setBlock(center.x - x, center.y + y, center.z + z, block)
        mc.setBlock(center.x - z, center.y + y, center.z + x, block)
        oldx = x
        z += 1
        x = sqrt(r * r - z * z)
        x = int(round(x))
    if oldx != z:
        mc.setBlock(center.x + x, center.y + y, center.z + z, block)
        mc.setBlock(center.x - x, center.y + y, center.z - z, block)
        mc.setBlock(center.x + x, center.y + y, center.z - z, block)
        mc.setBlock(center.x - x, center.y + y, center.z + z, block)

def ring(center, r, block, height=1):
    mc.setBlock(center.x, center.y - 1, center.z, WOOL)
    for y in xrange(height):
        newPos = mcpi.vec3.Vec3(center.x, center.y + y, center.z)
        smallRing(newPos, r, block)
        print center.y
       
try:
    __file__
except: 
    sys.argv = [sys.argv[0], '20', '3']

message = "Usage: /py shape <ring|hill>"
try:
    operation = sys.argv[1]
except IndexError:
    print message
    sys.exit()

mc = Minecraft()
playerPos = mc.player.getPos()

operations = {
    'ring': "Usage: /py shape ring <radius> <block> [height]",
    'hill': "Usage: /py shape hill <radius> <height>",
    'circle': "Usage: /py shape circle <radius> <block>, [height]"
    }

if operation not in operations:
    print message
    sys.exit()

helpMsg = operations[operation]
requiredParameters = helpMsg.count('<')
if len(sys.argv)-2 < requiredParameters:
    print helpMsg
    sys.exit()

params = []
for param in sys.argv[2:]:
    try:
        params.append(int(param))
    except ValueError:
        params.append(param)

globals()[operation](playerPos, *params)
print "Created a", operation 
    
        

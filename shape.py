""" Create shapes in a minecraft world """

import sys
import math

import mcpi
from mc import *

Blocks = {}
for key, value in mcpi.block.__dict__.iteritems():
    key = key.replace('HARDENED_CLAY_STAINED', 'STAINED_HARDENED_CLAY')
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
        name, data = blockName.rsplit('_', 1)
    except ValueError:
        block = Blocks[blockName]
    else:
        try:
            data = int(data)
        except ValueError:
            block = Blocks[blockName]
            return block
        block = Block(Blocks[name].id, data)
    return block

def ring(center, r, block, height=1):
    """ Create a ring around center of radius r blocks using block type """

    block = lookupBlock(block)
    c = 2 * math.pi * r
    #print "Circumference:", c
    for point in xrange(0, int(round(c))):
        angle = point * 360 / c
        radians = math.radians(angle)
        x = int(round(r * math.cos(radians)))
        z = int(round(r * math.sin(radians)))
        
        for y in xrange(height):
            #print point, x, y, z
            mc.setBlock(center.x + x, center.y + y, center.z + z, block)
            

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
    
        

from net.minestom.server import MinecraftServer
from net.minestom.server.instance import InstanceManager
from net.minestom.server.instance import InstanceContainer
from net.minestom.server.world import DimensionType

from net.minestom.server.coordinate import Pos

from net.minestom.server.event import EventNode
from net.minestom.server.event.player import PlayerLoginEvent
from net.minestom.server.event.player import PlayerDeathEvent
from net.minestom.server.event.player import PlayerDisconnectEvent
from net.minestom.server.event.player import PlayerSpawnEvent
from net.minestom.server.event.item import PickupItemEvent

from net.minestom.server.item import ItemStack
from net.minestom.server.item.metadata import BundleMeta
from net.minestom.server.item import Materials
from net.minestom.server.inventory import InventoryType
from net.minestom.server.inventory import Inventory
from net.kyori.adventure.text import Component
from net.minestom.server.event.player import PlayerBlockBreakEvent
from net.minestom.server.event.player import PlayerStartDiggingEvent

from net.minestom.server.entity import GameMode

from net.minestom.server.command.builder import Command

from java.util import Set


from minestomp.utils import *
from minestomp.gen import *

class PlayersCommand(Command):
    def __init__(self):
        super(PlayersCommand, self).__init__("players")
        self.setDefaultExecutor(self.usage)    

    def usage(self, sender, context):
        players = MinecraftServer.getConnectionManager().getOnlinePlayers()
        playerCount = players.size()
        sender.sendMessage(Component.text("Total players: " + str(playerCount)))
        limit = 15
        if playerCount <= limit:
            for player in players:
                sender.sendMessage(Component.text(player.getUsername()))            
        else:
            for player in players.stream().limit(limit).toList():
                sender.sendMessage(Component.text(player.getUsername()))
            sender.sendMessage(Component.text("..."))        



minecraftServer = MinecraftServer.init()
MinecraftServer.setTerminalEnabled(False)

commandManager = MinecraftServer.getCommandManager()

commandManager.register(PlayersCommand())

instanceManager = MinecraftServer.getInstanceManager()

#instanceManager.createInstanceContainer(DimensionType.OVERWORLD).setGenerator(Gen(
#    lambda unit: unit.modifier().fillHeight(0, 40, block_type("stone"))
#))

#instanceManager.createInstanceContainer(DimensionType.OVERWORLD).setGenerator(NoiseTestGenerator())
instanceManager.createInstanceContainer(DimensionType.OVERWORLD).setGenerator(TestGen())

inventory = Inventory(InventoryType.CHEST_1_ROW, Component.text("Test inventory"))
inventory.setItemStack(3, ItemStack.of(material_type("diamond"), 34))

def log(s): print s

mineables = {
    "stone": {"stone":1},
    "oak_leaves": {"oak_log":1},
    "oak_log": {"oak_log":1}
}
def shortBlockName(name):
    if name is None: return ""
    return name.split(":")[1]

def handlePlayerBlockBreak(event):
    name = shortBlockName(event.getBlock().name())
    if name in mineables.keys():
        for key in mineables[name].keys():
            event.getPlayer().getInventory().addItemStack(ItemStack.builder(material_type(key)).amount(mineables[name][key]).build())
    else:
        event.setCancelled(True)

MinecraftServer.getGlobalEventHandler().addChild(EventNode.all("demo")

    .addListener(PlayerLoginEvent, jcv(lambda event: [
        event.setSpawningInstance(MinecraftServer.getInstanceManager().getInstances().iterator().next()),
        event.getPlayer().setRespawnPoint(Pos(0, 142.0, 0))
    ]))

    .addListener(PlayerDeathEvent, jc(lambda event: event.setChatMessage(Component.text("custom death message"))))

    .addListener(PlayerDisconnectEvent, jc(lambda event: log("DISCONNECTION " + event.getPlayer().getUsername())))

    .addListener(PlayerSpawnEvent, jcv(lambda event: [
        event.getPlayer().getInventory().addItemStack(ItemStack.builder(material_type("stone")).amount(64).meta(
            jcv(lambda itemMetaBuilder: itemMetaBuilder.canPlaceOn(Set.of(block_type("stone"))).canDestroy(Set.of(block_type("diamond_ore"))))
        ).build()),

        event.getPlayer().getInventory().addItemStack(ItemStack.builder(material_type("bundle")).meta(BundleMeta, jcv(lambda bundleMetaBuilder: [
            bundleMetaBuilder.addItem(ItemStack.of(material_type("diamond"), 5)),
            bundleMetaBuilder.addItem(ItemStack.of(material_type("rabbit_foot"), 5))
        ])).build()),

        event.getPlayer().setGameMode(GameMode.CREATIVE),
        #player.setPermissionLevel(4);
    ]))

    .addListener(PickupItemEvent, jcv(lambda event: [
        # Cancel event if player does not have enough inventory space
        event.setCancelled(not entity.getInventory().addItemStack(event.getItemEntity().getItemStack())) if isinstance(event.getLivingEntity(), Player) else None       
    ]))

    .addListener(PlayerStartDiggingEvent, jcv(lambda event: [
        log("PlayerStartDiggingEvent:" + str(event.getBlock().name())),
        #event.setCancelled(True) if shortBlockName(event.getBlock().name()) not in mineables.keys() else event.setCancelled(True)
    ]))

    .addListener(PlayerBlockBreakEvent, jcv(lambda event: [
        log("PlayerBlockBreakEvent:" + str(event.getBlock().name())),
        #handlePlayerBlockBreak(event)
    ]))
)

minecraftServer.start("0.0.0.0", 25565)
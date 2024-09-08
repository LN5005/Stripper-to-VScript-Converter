# Stripper-to-VScript Converter
A converter that transforms entity code from Stripper format to VScript format.

自动生成 director_base_addon、自动运行用于生成实体的脚本：
* _entities.nut -- 没有 Output 的一般实体，如 prop_dynamic;
* _events.nut -- 需要添加 Output 的实体，如 logic_auto;
* _OnMapSpawn.nut -- 在地图生成后通过 logic_auto 进行的操作，例如 EntityOutputs.AddOutput， EntFire 之类的。
* _OnFullyOpen.nut -- 由安全门执行的脚本；在没有安全门的地图上使用 trigger_once 替代。 
* _ladders.nut -- 各种梯子

一般要求：
把 Stripper 的代码扔进 input.txt 里；
在 config.cfg 里填入地图名称（如 c5m2_park）和地图起始安全门的名称；如果安全门不存在，则应更改相关参数以使相关功能能够按预期工作。

### 配置文件说明
* config_..._values.cfg -- 键值的各种类型；将键以相应的格式，根据键值放入其中。
  - 例如 targetname 的键值是 string 类的，因此请将其放入 config_string_values.cfg 来让脚本生成适用于此类键值的代码格式。
* config_event_classnames 将会出现在 _events.nut 中的实体类名。
* config_entity_outputs 在 _entities.cfg 中处理的 Output。
* config_classname_blacklist.cfg 则是被排除的类名。参见 https://github.com/ValveSoftware/Source-1-Games/issues/6333
* config_items 是由安全门生成的实体类名，之所以使用安全门生成实体，是因为通过其他方法生成的医疗包、燃烧瓶、弹药包等实体会因为不明原因而不可见（invisible）。
  - 也可将某些代码写入到 _OnFullyOpen.nut 以推迟其执行顺序，如用于 kill（移除）TLS 更新所添加的实体的代码。

一般情况下，被放入 _entities.nut 的实体（即 {} 内）会以插入 float 或 int 的形式插入未知参数及其键值。
如果键及其键值属于 Output，那么这会导致代码不工作，游戏引擎运行 _entities.nut 时也会因此报错。例如：
```
SpawnEntityFromTable("prop_physics",
{
	targetname = entity_472,
	origin = Vector(-7350,-8272,-27),
	angles = Vector(0,90,0),
	model = "models/props_vehicles/airport_baggage_cart2.mdl",
	OnAwakened = ['physical_gate_wall_road,EnableMotion,,0,-1', 'bus_station_saferoom_door_nav_blocker_02,BlockNav,,0,-1'],
	spawnflags = 1025,
});
```
* 在这种情况下，要么将 output 的名称添加到上述的配置文件中来让脚本以处理 output 的形式处理该键及其键值，要么将 classname 放入 config_event_classnames 中。

被放入 _events.nut 的实体则会以处理 Output 的格式来处理未知参数及其键值，但不包括 _values.cfg 定义的参数及其键值（这些参数和键值会放入实体内）。
* config_event_classnames  决定了具有哪些类名的实体会被放入 _events.nut。
### 已知问题
由于 EntFire 和 EntityOutput.AddOutput 不对 worldspawn 实体起作用，所以没有办法修改天空盒（skybox）。
* 这要么是因为 director_base_addon.nut 的执行顺序不够前，要么是因为 skybox 的修改需要通过删除实体并重建实体来实现，要么是 mapspawn 必须通过我不知道的 VScript 方法来修改。无论是哪种情况，修改该实体可能都是高风险的（可能会引起游戏崩溃）。
* 参见 https://developer.valvesoftware.com/wiki/Worldspawn

ED_Alloc: No free edicts
* 你在地图上添加的实体太多了，或者你使用的其他插件生成了太多的东西。先用 EntFire 删除一些 Vanilla（原版）实体，再用 OnFullyOpen 生成实体。
* 可以用 Stripper 的 stripper_dump 控制台命令来获取官图上的实体，然后根据需要移除其中的不必要实体。
* 参见： https://developer.valvesoftware.com/wiki/Entity_limit

怎么修改 vanilla 梯子的 team 参数键值？
* 该参数虽然可以用 entfire 或者 entityoutput 的方法修改，但是却会引起 navmesh 方面上的初始化错误，具体来说就是地图上不生成任何 common（小僵尸）
* 需要删除梯子，然后将生成梯子的代码拍进 _ladder.nut 文件里
 
如果 input.txt 内有 func_simpleladder 类实体，那么它会在 _ladder.nut 底部创建一个列表和相关代码：

> local ladder_models = [……

将梯子的 model 键值扔进这个列表里，再将列表和跟列表有关的代码移动到顶部。这个列表会根据 model 的键值删除地图上的所有梯子，包括你添加的梯子和 TLS 更新所添加的梯子。这是因为梯子没有 targetname 和 origin 所以没办法通过一般的方法针对性地删除。

_entities.nut 无法运行 -- 这通常是因为输入的代码的格式不正确引起的问题。打开游戏内控制台，查找类似的字符串：
```
Initializing Director's script
Loading addon script c:\program files (x86)\steam\steamapps\common\left 4 dead 2\left4dead2\scripts\vscripts\director_base_addon.nut
c1m1_hotel_vscript executing script: c1m1_hotel_entities
scripts/vscripts/c1m1_hotel_entities.nut line = (266) column = (2) : error expression expected 
```
打开 _events.nut, 跳到第 266 行：
> }

看起来 input.txt 里的某些东西格式不正确，然后导致脚本生成了一个 }。只需要删除 input.txt 内的 } 就好了。

再次运行 _entities.nut，报错：
> scripts/vscripts/c1m1_hotel_entities.nut line = (528) column = (49) : error expected '='

跳到第 528 行

> onhurtplayer = !activator,speakresponseconcept,PlayerBackUp,0,5, 

将 onhurtplayer 添加到 config_entitiy_outputs.cfg，该参数及其键值就会在转换脚本运行时被转换成兼容的格式：

> EntityOutputs.AddOutput(Entities.FindByName(null,"sky_fire_hurt"),"OnHurtPlayer","!activator","speakresponseconcept","PlayerBackUp",0.0,5);

再次运行 _entities.nut，报错：

> scripts/vscripts/c1m1_hotel_entities.nut line = (1554) column = (55) : error constant too long

……… 重复这个过程。

除非地图只有用 Object Spawner( https://github.com/fbef0102/L4D1_2-Plugins/tree/master/l4d2_spawn_props ) 生成的 prop_dyanmic 类实体，否则报错应该是不可避免的。

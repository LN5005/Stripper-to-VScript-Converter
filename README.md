# Stripper-to-VScript Converter
A converter that transforms entity code from Stripper format to VScript format.

work in progress.

自动生成 director_base_addon、自动运行用于生成实体的脚本：
* _entities.nut -- 没有 Output 的一般实体，如 prop_dynamic;
* _events.nut -- 需要添加 Output 的实体，如 logic_auto;
* _OnMapSpawn.nut -- 在地图生成后通过 logic_auto 进行的操作，例如 EntityOutputs.AddOutput， EntFire 之类的。
* _ladders.nut -- 各种梯子

一般要求：
把 Stripper 的代码扔进 input.txt 里；
在 config.cfg 里填入地图名称（如 c5m2_park）。

### 配置文件说明
* config_..._values.cfg -- 键值的各种类型；将键以相应的格式，根据键值放入其中。
  - 例如 targetname 的键值是 string 类的，因此请将其放入 config_string_values.cfg 来让脚本生成适用于此类键值的代码格式。
* config_event_classnames 将会出现在 _events.nut 中的实体类名。
* config_entity_outputs 在 _entities.cfg 中处理的 Output。
* config_classname_blacklist.cfg 则是被排除的类名。参见 https://github.com/ValveSoftware/Source-1-Games/issues/6333 

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

被放入 _events.nut 的实体则会以特定的格式在实体外处理未知参数及其键值，但不包括 _values.cfg 定义的参数及其键值（这些参数和键值会放入实体内）。
* config_event_classnames  决定了具有哪些类名的实体会被放入 _events.nut。
> [!WARNING]
> _请不要用这个脚本做坏事。如果乱用这个脚本（比如在不考虑著作权的情况下将别人的 Stripper 文件转换成 VScript 并上传到 Workshop）可能会让你吃红信（社区封禁）。_

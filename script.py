import re
import linecache
import csv
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding = 'utf=8')

MAP_name = config.get('MAP', 'Name_map').strip()
SDN = config.get('SDB', 'SDB_targetname').strip()
SD_exists = config.get('SDB', 'SDB_exists').strip()

SD_once_targetname = config.get('STV_once', 'STV_targetname').strip()

SD_once_origin = config.get('STV_once', 'STV_origin').strip()
SD_once_origin = SD_once_origin.replace(' ', ',')

SD_once_mins = config.get('STV_once', 'STV_mins').strip()
SD_once_maxs = config.get('STV_once', 'STV_maxs').strip()

# string keyvalues

with open('config_string_values.cfg', 'r', encoding='utf-8') as string_keyvalues_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(string_keyvalues_file, delimiter=',')

    # 定义一个空字典来存储键值对
    string_keyvalues = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0] , row[1] #  假设键和值总是成对出现
        string_keyvalues[key.lower()] = value

# vector keyvalues
with open('config_vector_values.cfg', 'r', encoding='utf-8') as vector_keyvalues_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(vector_keyvalues_file, delimiter=',')

    # 定义一个空字典来存储键值对
    vector_keyvalues = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0], row[1]  # 假设键和值总是成对出现
        vector_keyvalues[key.lower()] = value

# int keyvalues
with open('config_int_values.cfg', 'r', encoding='utf-8') as int_keyvalues_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(int_keyvalues_file, delimiter=',')

    # 定义一个空字典来存储键值对
    int_keyvalues = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0], row[1]  # 假设键和值总是成对出现
        int_keyvalues[key.lower()] = value

# float keyvalues
with open('config_float_values.cfg', 'r', encoding='utf-8') as float_keyvalues_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(float_keyvalues_file, delimiter=',')

    # 定义一个空字典来存储键值对
    float_keyvalues = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0], row[1]  # 假设键和值总是成对出现
        float_keyvalues[key.lower()] = value

with open('config_event_classnames.cfg', 'r', encoding='utf-8') as event_classnames_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(event_classnames_file, delimiter=',')

    # 定义一个空字典来存储键值对
    event_classnames = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0], row[1]  # 假设键和值总是成对出现
        event_classnames[key.lower()] = value

# entity_outputs for _entities.nut
with open('config_entity_outputs.cfg', 'r', encoding='utf-8') as entity_outputs_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(entity_outputs_file, delimiter=',')

    # 定义一个空字典来存储键值对
    entity_outputs = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0], row[1]  # 假设键和值总是成对出现
        entity_outputs[key.lower()] = value

# blacklisted classnames
with open('config_classname_blacklist.cfg', 'r', encoding='utf-8') as classname_blacklist_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(classname_blacklist_file, delimiter=',')

    # 定义一个空字典来存储键值对
    classname_blacklist = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0], row[1]  # 假设键和值总是成对出现
        classname_blacklist[key.lower()] = value

# item classnames
with open('config_items.cfg', 'r', encoding='utf-8') as items_file:
    # 创建一个csv reader，使用逗号作为分隔符
    reader = csv.reader(items_file, delimiter=',')

    # 定义一个空字典来存储键值对
    items = {}

    # 读取每一行，并构建键值对
    for row in reader:
        # 将每一行中的元素依次作为键和值
        key, value = row[0], row[1]  # 假设键和值总是成对出现
        items[key.lower()] = value

def convert_entity_code(
    input_file,
    output_file,
    output_ladder_file,
    output_event_file,
    onmapspawn_file,
    onfullyopen_file,
    director_base_addon
    ):
    
    ignore_keywords = ["add:", "modify:", "filter:"]
    #ignore_classnames = [
    #    "func_playerinfected_clip",
    #    "func_playerghostinfected_clip", 
    #    "func_illusionary", 
    #    "func_nav_attribute_region", 
    #    "another_classname", 
    #    "yet_another_classname"
    #    ] # 要忽略的类名
    # 如果你不想这个脚本处理某些类实体，那么可以修改该行代码中的键值来排除掉相关类名（黑名单）
    # 更新：把不想要的类名扔进 config_classname_blacklist.cfg 里。
    
    ladder_models = []
    ladder_counter = 1  # 用于跟踪 func_simpleladder 的序号
    logic_auto_counter = 1  # 用于跟踪 logic_auto 的序号
    logic_relay_counter = 1  # 用于跟踪 logic_relay 的序号
    logic_case_counter = 1  # 用于跟踪 logic_case 的序号
    trigger_once_counter = 1
    func_door_rotating_counter = 1
    func_entity_counter = 1
    entity_counter = 1
    prop_physics_counter = 1
    item_counter = 1

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile, \
         open(output_ladder_file, 'w', encoding='utf-8') as ladder_outfile, \
         open(output_event_file, 'w', encoding='utf-8') as output_event_file, \
         open(onmapspawn_file, 'w', encoding='utf-8') as onmapspawn_file, \
         open(onfullyopen_file, 'w', encoding='utf-8') as onfullyopen_file, \
         open(director_base_addon, 'w', encoding='utf-8') as director_base_addon:

        content = infile.readlines()
        content_iter = iter(content)  # 创建一个迭代器

        last_line_empty = False  # 跟踪前一行是否为空行

        # 处理注释行和实体部分
        for line in content_iter:
            if line.strip().startswith(';'):
                outfile.write(line.replace(';', '//', 1))
                last_line_empty = False
            elif any(keyword in line for keyword in ignore_keywords):
                continue
            elif line.strip() == '{':
                entity_lines = [line]  # 包含起始的 '{' 行
                nesting_level = 1  # 嵌套层次计数器
                while nesting_level > 0:
                    line = next(content_iter, '')
                    entity_lines.append(line)
                    if '{' in line:
                        nesting_level += line.count('{')
                    if '}' in line:
                        nesting_level -= line.count('}')

                entity = ''.join(entity_lines)

                lines = entity.strip('{} \n').split('\n')
                entity_dict = {}
                for entity_line in lines:
                    matches = re.findall(r'"([^"]*)"', entity_line)
                    if len(matches) == 2:
                        key, value = matches
                        if key in entity_dict:
                            if isinstance(entity_dict[key], list):
                                entity_dict[key].append(value)
                            else:
                                entity_dict[key] = [entity_dict[key], value]
                        else:
                            entity_dict[key] = value

                classname = entity_dict.get("classname")
                if not classname or classname in classname_blacklist:
                    continue  # 忽略没有 classname 或 classname 在 config_classname_blacklist.cfg 列表中的实体

                # 警告：func_simpleladder 类实体必须在 director_base_addon.nut 内执行，否则它将会干扰导航网络（navmesh）的正常工作，并导致 common 不在地图上生成！
                if classname == "func_simpleladder":
                    solid = entity_dict.get("solid", "0")
                    origin = entity_dict.get("origin", "0 0 0").replace(' ', ',')
                    angles = entity_dict.get("angles", "0 0 0").replace(' ', ',')
                    targetname = entity_dict.get("targetname", f"ladder_{ladder_counter}")
                    ladder_counter += 1

                    output = f'if ( Entities.FindByName(null,"{targetname}") == null)\n'
                    output += '{\n'
                    output += f'SpawnEntityFromTable("{classname}",\n{{\n'
                    output += f'\torigin = Vector({origin}),\n'
                    output += f'\tangles = Vector({angles}),\n'
                    output += f'\ttargetname = "{targetname}",\n'

                    # 处理其他键值对
                    for key, value in entity_dict.items():
                        key_lower = key.lower()
                        if key_lower not in ["classname", "solid", "origin", "angles"]:
                            if key_lower == "rendermode":
                                output += f'\trendermode = {value},\n'
                            elif key_lower == "model":
                                output += f'\tmodel = "{value}",\n'
                                ladder_models.append(value)  # 收集 model 参数的键值
                            elif key_lower == "normal.z": # 忽略 normal.z 参数（不将该参数及其键值作为 SpawnEntityFromTable 的一部分写入到输出当中）
                                output += f''
                            elif key_lower == "normal.x": # 同上
                                output += f''
                            elif key_lower == "normal.y": # 同上
                                output += f''
                            else:
                                output += f'\t{key} = {value},\n' # 如果参数名称不为 model targetname rendermode etc, 则根据该规则写入到输出
                                # 例如，spawnflags = 2,
                                # 对于 string 类的输出（如targetname），需要在上述列表中添加相应的规则，同时手动为输出的键值添加双引号。
                                # 因为 Stripper 的代码格式无法区分键值是不是 string（所有键值都包含双引号），所以脚本没办法自动识别并处理此类键值。

                    output += f'}});\n'

                    # 处理 normal.x, normal.y, normal.z 参数
                    if "normal.z" in entity_dict:
                        output += f'EntFire("{targetname}","addoutput","normal.z {entity_dict["normal.z"]}");\n'
                    if "normal.x" in entity_dict:
                        output += f'EntFire("{targetname}","addoutput","normal.x {entity_dict["normal.x"]}");\n'
                    if "normal.y" in entity_dict:
                        output += f'EntFire("{targetname}","addoutput","normal.y {entity_dict["normal.y"]}");\n'

                    output += '}\nelse{}\n\n'

                    # 检查前一行是否为空行
                    if not last_line_empty:
                        ladder_outfile.write('\n')

                    ladder_outfile.write(output)
                    last_line_empty = True
                    
                elif classname in items: # 要扔进 OnFullyOpen.nut 里的实体类型，config_items.cfg
                
                    targetname = entity_dict.get("targetname", f"item_{item_counter}")
                    item_counter += 1
                    
                    output = f'SpawnEntityFromTable("{classname}",\n{{\n'
                    output += f'\ttargetname = "{targetname}",\n'
                    
                    for key, value in entity_dict.items():
                        key_lower = key.lower()
                        if key_lower not in ["classname", "targetname"]:
                            if key_lower in string_keyvalues:
                                output += f'\t{key} = "{value}",\n'
                        
                            elif key_lower in vector_keyvalues:
                                vector_keyvalue = entity_dict.get(f'{key}', "0 0 0").replace(' ', ',')
                                value = vector_keyvalue # 将替换后的值重新赋值给 value by Google Gemini
                                output += f'\t{key} = Vector({value}),\n'

                            elif key_lower in int_keyvalues:
                                output += f'\t{key} = {value},\n'

                            elif key_lower in float_keyvalues:
                                output += f'\t{key} = {value},\n'

                    output += f'}});\n'
                    for key, value in entity_dict.items():
                        if key in entity_outputs:
                            # 确保 value 是字符串
                            if isinstance(value, list):
                                value = ','.join(value)
                                
                            values = value.split(',')
                            param1 = values[0] if len(values) > 0 else ""
                            param2 = values[1] if len(values) > 1 else ""
                            param3 = values[2] if len(values) > 2 else ""
                            param4 = values[3] if len(values) > 3 else "0"
                            param5 = values[4] if len(values) > 4 else "-1"
                            try:
                                param4 = float(param4)
                            except ValueError:
                                param4 = 0
                            try:
                                param5 = int(param5)
                            except ValueError:
                                param5 = -1
                            output += f'EntityOutputs.AddOutput(Entities.FindByName(null,"{targetname}"),"{key}","{param1}","{param2}","{param3}",{param4},{param5});\n'

                    # 检查前一行是否为空行
                    if not last_line_empty:
                        onfullyopen_file.write('\n')

                    onfullyopen_file.write(output)
                    last_line_empty = True
                    
                    if line.strip():  # 只写入非空行
                        onfullyopen_file.write('\n')  # 保留其他行的原始格式
                        last_line_empty = False
                    else:
                        last_line_empty = True
                            
                elif classname in event_classnames: # 要扔进 events.nut 里的实体类型，config_event_classnames.cfg
                    
                    default_prefix = "unnamed_"
                    counter_map = {
                    "logic_auto": logic_auto_counter,
                    "logic_relay": logic_relay_counter,
                    "logic_case": logic_case_counter,
                    "trigger_once": trigger_once_counter,
                    "func_door_rotating": func_door_rotating_counter,
                    "prop_physics": prop_physics_counter,
                    }
                    counter = counter_map.get(classname, None)
                    default_suffix = f"_{counter}" if counter else ""
                    targetname = entity_dict.get("targetname", f"{default_prefix}{classname}{default_suffix}")
                    
                    if classname == "logic_auto":
                        logic_auto_counter += 1
                    elif classname == "logic_relay":
                        logic_relay_counter += 1
                    elif classname == "logic_case":
                        logic_case_counter += 1
                    elif classname == "trigger_once":
                        trigger_once_counter += 1
                    elif classname == "func_door_rotating":
                        func_door_rotating_counter += 1
                    elif classname == "prop_physics":
                        prop_physics_counter += 1
                    else:
                        func_entity_counter += 1

                    output = f'SpawnEntityFromTable("{classname}",\n{{\n'
                    output += f'\ttargetname = "{targetname}",\n'
                    
                    for key, value in entity_dict.items():
                        key_lower = key.lower()
                        if key_lower not in ["classname", "targetname"]:
                            if key_lower in string_keyvalues:
                                output += f'\t{key} = "{value}",\n'
                        
                            elif key_lower in vector_keyvalues:
                                vector_keyvalue = entity_dict.get(f'{key}', "0 0 0").replace(' ', ',')
                                value = vector_keyvalue # 将替换后的值重新赋值给 value by Google Gemini
                                output += f'\t{key} = Vector({value}),\n'

                            elif key_lower in int_keyvalues:
                                output += f'\t{key} = {value},\n'

                            elif key_lower in float_keyvalues:
                                output += f'\t{key} = {value},\n'
                                
                            elif key_lower in entity_outputs:
                                output += f''
                                
                    output += f'}});\n'

                    for key, value in entity_dict.items():
                        key_lower = key.lower()
                        if key_lower == "parentname":
                            onmapspawn_file.write(f'EntFire("{targetname}","setparent","{value}");\n')
                            # 如果键值需要使用 addoutput 添加
                        elif any(key_lower in lst for lst in [vector_keyvalues, string_keyvalues, int_keyvalues, float_keyvalues]):
                            # 如果键属于 vector, string, int 或 float 表中定义的任何键，则不执行任何操作
                            output += f''
                        elif key_lower not in [ # 不使用 EntityOutputs.AddOutput 的参数
                                ]:
                            if isinstance(value, list):
                                for item in value:
                                    values = item.split(',')
                                    param1 = values[0] if len(values) > 0 else ""
                                    param2 = values[1] if len(values) > 1 else ""
                                    param3 = values[2] if len(values) > 2 else ""
                                    param4 = values[3] if len(values) > 3 else "0"
                                    param5 = values[4] if len(values) > 4 else "-1"
                                    try:
                                        param4 = float(param4)
                                    except ValueError:
                                        param4 = 0
                                    try:
                                        param5 = int(param5)
                                    except ValueError:
                                        param5 = -1
                                    if key_lower == "onmapspawn":
                                       onmapspawn_file.write(f'EntFire("{param1}","{param2}","{param3}",{param4},{param5});\n')
                                    else:
                                        output += f'EntityOutputs.AddOutput(Entities.FindByName(null,"{targetname}"),"{key}","{param1}","{param2}","{param3}",{param4},{param5});\n'
                            else:
                                values = value.split(',')
                                param1 = values[0] if len(values) > 0 else ""
                                param2 = values[1] if len(values) > 1 else ""
                                param3 = values[2] if len(values) > 2 else ""
                                param4 = values[3] if len(values) > 3 else "0"
                                param5 = values[4] if len(values) > 4 else "-1"
                                try:
                                    param4 = float(param4)
                                except ValueError:
                                    param4 = 0
                                try:
                                    param5 = int(param5)
                                except ValueError:
                                    param5 = -1
                                output += f'EntityOutputs.AddOutput(Entities.FindByName(null,"{targetname}"),"{key}","{param1}","{param2}","{param3}",{param4},{param5});\n'
                            output += f'\n'

                    # 检查前一行是否为空行
                    if not last_line_empty:
                        output_event_file.write('\n')

                    output_event_file.write(output)
                    last_line_empty = True
                    
                    
                else: # entities.nut
                    targetname = entity_dict.get("targetname", f"entity_{entity_counter}")
                    entity_counter += 1

                    output = f'SpawnEntityFromTable("{classname}",\n{{\n'
                    output += f'\ttargetname = "{targetname}",\n'
                    
                    # 处理其他键值对
                    for key, value in entity_dict.items():
                        key_lower = key.lower()
                        if key_lower not in ["classname", "targetname"]:
                        
                            if key_lower in string_keyvalues:
                                output += f'\t{key} = "{value}",\n'

                            elif key_lower in vector_keyvalues:
                            
                                if isinstance(value, list):
                                    value = ' '.join(value)
                                    value = value.replace(' ', ',')
                                else:
                                    vector_keyvalue = entity_dict.get(f'{key}', "0 0 0").replace(' ', ',')
                                    value = vector_keyvalue # 将替换后的值重新赋值给 value by Google Gemini
                                output += f'\t{key} = Vector({value}),\n'

                            elif key_lower in int_keyvalues:
                                output += f'\t{key} = {value},\n'

                            elif key_lower in float_keyvalues:
                                output += f'\t{key} = {value},\n'

                            elif key_lower == "parentname":
                                onmapspawn_file.write(f'EntFire("{targetname}","setparent","{value}");\n')
                                
                            elif key_lower in entity_outputs:
                                output += f''
                                
                            else:
                                output += f'\t{key_lower} = {value},\n'

                    output += f'}});\n\n'
                    # 如果被放入 entities.nut 的实体具有由 config_entity_outputs.cfg 定义的 output 键值
                    for key, value in entity_dict.items():
                        key_lower = key.lower()
                        if key_lower in entity_outputs:
                            # 确保 value 是字符串
                            if isinstance(value, list):
                                value = ','.join(value)
                                
                            values = value.split(',')
                            param1 = values[0] if len(values) > 0 else ""
                            param2 = values[1] if len(values) > 1 else ""
                            param3 = values[2] if len(values) > 2 else ""
                            param4 = values[3] if len(values) > 3 else "0"
                            param5 = values[4] if len(values) > 4 else "-1"
                            try:
                                param4 = float(param4)
                            except ValueError:
                                param4 = 0
                            try:
                                param5 = int(param5)
                            except ValueError:
                                param5 = -1
                            output += f'EntityOutputs.AddOutput(Entities.FindByName(null,"{targetname}"),"{key}","{param1}","{param2}","{param3}",{param4},{param5});\n'
                    # 检查前一行是否为空行
                    if not last_line_empty:
                        outfile.write('\n')

                    outfile.write(output)
                    last_line_empty = True
            else:
                if line.strip():  # 只写入非空行
                    outfile.write(line)  # 保留其他行的原始格式
                    last_line_empty = False
                else:
                    last_line_empty = True

        # 在 output_ladder.txt 的最后写入收集的 model 参数键值
        if ladder_models:
            ladder_outfile.write('// If you are modifying a vanilla ladder, move the code below to top; else,remove them. \n')
            ladder_outfile.write("// Put vanilla ladder's model in the list. \n\n")
            ladder_outfile.write('local ladder_models =\n[\n')
            for model in ladder_models:
                ladder_outfile.write(f'\t"// {model}"\n')
            ladder_outfile.write(']\n\n')
            ladder_outfile.write('foreach( ladder_targets in ladder_models )\n')
            ladder_outfile.write('{\n')
            ladder_outfile.write('	local ladder_list = null\n')
            ladder_outfile.write('	while ( ladder_list = Entities.FindByModel(ladder_list, ladder_targets))\n')
            ladder_outfile.write('	ladder_list.Kill()\n')
            ladder_outfile.write('}\n')
        # 生成 director_base_addon
            director_base_addon.write("// Generated by LN5005's Stripper-to-VScript Converter\n")
            director_base_addon.write("// Github: https://github.com/LN5005/Stripper-to-VScript-Converter \n")
            director_base_addon.write("// follow me, plz: https://steamcommunity.com/id/LN5005/myworkshopfiles/ \n\n")
            director_base_addon.write(f'local whatisthemapname = null\n')
            director_base_addon.write(f'whatisthemapname = Director.GetMapName()\n')
            director_base_addon.write(f'if(whatisthemapname == "{MAP_name}")\n')
            director_base_addon.write('{\n')
            director_base_addon.write(f'	IncludeScript("{MAP_name}_ladders.nut", this);\n')
            director_base_addon.write(f'	if ( Entities.FindByName(null,"{MAP_name}_vscript") == null)\n')
            director_base_addon.write('		{\n')
            director_base_addon.write(f'			SpawnEntityFromTable("logic_script",\n')
            director_base_addon.write('			{\n')
            director_base_addon.write(f'				targetname = "{MAP_name}_vscript",\n')
            director_base_addon.write(f'				vscripts = "{MAP_name}_entities",\n')
            director_base_addon.write('			});\n')
            director_base_addon.write(f'			printl("{MAP_name}_vscript has been spawned.")\n')
            director_base_addon.write('		}\n')
            director_base_addon.write(f'		else\n')
            director_base_addon.write('		{\n')
            director_base_addon.write('		}\n\n')
		
            director_base_addon.write(f'if ( Entities.FindByName(null,"{MAP_name}_events_spawner") == null)\n')
            director_base_addon.write('		{\n')
            director_base_addon.write(f'			SpawnEntityFromTable("logic_auto",\n')
            director_base_addon.write('			{\n')
            director_base_addon.write(f'				targetname = "{MAP_name}_events_spawner",\n')
            director_base_addon.write('			});\n\n')
			
            director_base_addon.write(f'			IncludeScript("{MAP_name}_events.nut", this);\n\n')
			
            director_base_addon.write(f'//			EntityOutputs.AddOutput(Entities.FindByName(null,"{MAP_name}_events_spawner"),"OnMapSpawn","!self","RunScriptFile","{MAP_name}_events",0.0,-1);\n')

            director_base_addon.write(f'			EntityOutputs.AddOutput(Entities.FindByName(null,"{MAP_name}_events_spawner"),"OnMapSpawn","!self","RunScriptFile","{MAP_name}_OnMapSpawn",0.0,-1);\n')
            director_base_addon.write(f'			printl("c5m3_events_spawner has been spawned.")\n')
            director_base_addon.write('		}\n')
            director_base_addon.write('		else\n')
            director_base_addon.write('		{\n')
            
            if SD_exists == "1":
                director_base_addon.write(f'		EntityOutputs.AddOutput(Entities.FindByName(null,"{SDN}"),"OnFullyOpen","!self","RunScriptFile","{MAP_name}_OnFullyOpen",0.0,1);\n')

            else:
                output_event_file.write(f'SpawnEntityFromTable("trigger_once",\n')
                output_event_file.write("{\n")
                output_event_file.write(f'    targetname = "{SD_once_targetname}",\n')
                output_event_file.write(f'    filtername = "survivor",\n')
                output_event_file.write(f'    spawnflags = 1,\n')
                output_event_file.write(f'    startdisabled = 0,\n')
                
                output_event_file.write(f'    origin = Vector({SD_once_origin}),\n')
                output_event_file.write("});\n")
                output_event_file.write(f'EntityOutputs.AddOutput(Entities.FindByName(null,"{SD_once_targetname}"),"OnTrigger","!self","RunScriptFile","{MAP_name}_OnFullyOpen",0.0,1);\n')
                
                onmapspawn_file.write(f'EntFire("{SD_once_targetname}","addoutput","mins {SD_once_mins}",0.0,-1);\n')
                onmapspawn_file.write(f'EntFire("{SD_once_targetname}","addoutput","maxs {SD_once_maxs}",0.0,-1);\n')
                onmapspawn_file.write(f'EntFire("{SD_once_targetname}","addoutput","solid 2",0.0,-1);\n')

            director_base_addon.write('		}\n')
            director_base_addon.write('}\n')

# 使用示例
convert_entity_code(
    'input.txt',
    f'{MAP_name}_entities.nut',
    f'{MAP_name}_ladders.nut',
    f'{MAP_name}_events.nut',
    f'{MAP_name}_OnMapSpawn.nut',
    f'{MAP_name}_OnFullyOpen.nut',
    'director_base_addon.nut')
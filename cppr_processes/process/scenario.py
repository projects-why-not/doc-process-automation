from xml.etree import ElementTree as ET
from .instruction import *
from .data import *
from ..utils.path import LocalPath
from ..utils.xml_tag_parsing import XMLTagParser


class Scenario:
    @classmethod
    def _parse_parameters(cls, param_node):
        dtypes = {"str": str,
                  "int": int,
                  "float": float,
                  # TODO
                  }
        params = {}
        for item in param_node:
            if item.tag != "param":
                raise ValueError("Only <param> tags are allowed inside <parameters> tag!")
            params[item.attrib["label"]] = dtypes[item.attrib["type"]](item.text)
        return params

    @classmethod
    def _parse_data(cls, data_node):
        if data_node is None:
            raise Exception("Data required!")
        data_info = {}
        for item in data_node:
            if item.tag == "file":
                data_info[item.attrib["label"]] = File(item.attrib["path"], item.attrib["type"])
            elif item.tag == "template":
                data_info[item.attrib["label"]] = Template(item.attrib["path"], item.attrib["type"])
            elif item.tag == "dir":
                data_info[item.attrib["label"]] = Directory(item.attrib["path"])
            else:
                raise ValueError
        return data_info

    @classmethod
    def _play_cmd(cls, cmd_xml, data):
        def get_document(data, cmd_info):
            obj = data[cmd_info["data_label"]]
            if callable(obj) and cmd_info["data_tag"] != "name":
                storage_provider = None
                if obj.storage == "yadisk":
                    storage_provider = data.get("__yadisk", None)
                obj = obj(storage_provider)
            return obj

        def play_io_cmd(cmd_info):
            if cmd_info["type"] == "cout":
                if type(cmd_info["contents"]) is str:
                    value = [cmd_info["contents"]]
                else:
                    value = [cls._play_cmd(cmd, data)
                             for cmd in cmd_info["contents"]]
                return Console()(*value)

            obj = get_document(data, cmd_info)
            # obj = data[cmd_info["data_label"]]
            # if callable(obj) and cmd_info["data_tag"] != "name":
            #     obj = obj()

            if cmd_info["type"] == "get":
                return Get()(obj,  # data[cmd_info["data_label"]](),
                             cmd_info["data_tag"])
            elif cmd_info["type"] == "set":
                if type(cmd_info["contents"]) is str:
                    # MARK: text supposed inside
                    value = cmd_info["contents"]
                else:
                    # MARK: subcommand GET (or another ONE command) is expected
                    if len(cmd_info["contents"]) != 1:
                        raise ValueError("Only one command expected inside <set>!")
                    value = cls._play_cmd(cmd_info["contents"][0], data)

                return Set()(obj,  # data[cmd_info["data_label"]](),
                             cmd_info["data_tag"],
                             value, *cmd_info["filter"])
            # elif cmd_info["type"] == "cout":
            #     if type(cmd_info["contents"]) is str:
            #         value = [cmd_info["contents"]]
            #     else:
            #         value = [cls._play_cmd(cmd, data)
            #                  for cmd in cmd_info["contents"]]
            #     return Console()(*value)

            raise ValueError("Wrong type of cmd in play_io_cmd!")

        def play_file_io_cmd(cmd_info):
            if cmd_info["type"] == "open":
                if type(cmd_info["contents"]) is not str:
                    raise ValueError("New label must be provided in contents!")
                data[cmd_info["contents"]] = data[cmd_info["data_label"]]()
                return True
            elif cmd_info["type"] == "save":
                cmd_obj = cmd_info["data_label"]
                cmd_path = cmd_info["contents"]
                if type(cmd_path) is not str:
                    if len(cmd_path) != 1:
                        raise ValueError("Only one name must be provided!")
                    cmd_path = cls._play_cmd(cmd_path[0], data)

                if "dir" in cmd_info:
                    dir_path = data[cmd_info["dir"]]()
                    cmd_path = str(LocalPath(dir_path) + cmd_path)
                return SaveDocument()(data[cmd_obj](), cmd_path)
            raise ValueError("Wrong cmd type in play_file_io_cmd!")

        def play_if(cmd_info):
            condition_info = [tag for tag in cmd_info["contents"] if tag["type"] == "condition"]
            then_cmds = [tag["contents"] for tag in cmd_info["contents"] if tag["type"] == "then"]
            else_cmds = [tag["contents"] for tag in cmd_info["contents"] if tag["type"] == "else"]

            if len(condition_info) != 1 or len(then_cmds) != 1 or len(else_cmds) > 1:
                raise ValueError("Wrong condition block provided!")
            condition_info = condition_info[0]
            then_cmds = then_cmds[0]
            if len(else_cmds) > 0:
                else_cmds = else_cmds[0]

            output = None

            cond_operands = [cls._play_cmd(tag, data)
                             for tag in condition_info["contents"]]
            # print("check res:", IfCondition()(condition_info, *cond_operands))
            if IfCondition()(condition_info, *cond_operands):
                # MARK: if true
                for cmd in then_cmds:
                    output = cls._play_cmd(cmd, data)
            else:
                # MARK: if false
                if len(else_cmds) == 0:
                    return output
                for cmd in else_cmds:
                    output = cls._play_cmd(cmd, data)
                    print(output)
            return output

        def play_yadisk_cmd(cmd_info):
            yadisk_instance = data.get("__yadisk", None)
            cmd_res = YandexDiskInstruction(yadisk_instance)(cmd_info["data_label"],
                                                             *[cls._play_cmd(cmd, data)
                                                               for cmd in (cmd_info["contents"]
                                                                           if type(cmd_info["contents"]) is not str
                                                                           else [cmd_info["contents"]])])
            if cmd_info["data_label"] == "login" and yadisk_instance is None:
                data["__yadisk"] = cmd_res
            return cmd_res

        if type(cmd_xml) is dict:
            cmd_info = cmd_xml
        elif type(cmd_xml) is str:
            if cmd_xml[0] == "$":
                return data["param"][cmd_xml[1:]]
            return cmd_xml
        else:
            cmd_info = XMLTagParser.parse(cmd_xml)

        if cmd_info["type"] in ["get", "set", "cout"]:
            return play_io_cmd(cmd_info)
        elif cmd_info["type"] in ["open", "save", "close"]:
            return play_file_io_cmd(cmd_info)
        elif cmd_info["type"] == "yadisk":
            play_yadisk_cmd(cmd_info)
        elif cmd_info["type"] == "string":
            return FormattedString()(cmd_info["data_label"],
                                     *[cls._play_cmd(cmd, data)
                                       for cmd
                                       in (cmd_info["contents"]
                                           if type(cmd_info["contents"]) is not str
                                           else [cmd_info["contents"]])],
                                     filter=cmd_info["filter"] if "filter" in cmd_info else None)
        elif cmd_info["type"] == "for":
            parent_node = data[cmd_info["data_label"]]
            if type(parent_node) is not Directory:
                parent_node = get_document(data, cmd_info)
            # if callable(parent_node) and type(parent_node) is not Directory:
            #     parent_node = parent_node()
            if type(parent_node) is Directory and parent_node._kind == "yadisk":
                parent_node.server = data["__yadisk"]

            if len(cmd_info["data_tag"]) > 0:
                tag_pts = cmd_info["data_tag"].split("@")
                for pt in tag_pts:
                    parent_node = parent_node[pt]

            nest_level = len([key for key in data.keys() if "__iter" in key])
            for subnode in parent_node:
                # print("\t", subnode)
                data[f"__iter{nest_level}"] = subnode
                for cmd in cmd_info["contents"]:
                    cls._play_cmd(cmd, data)
            del data[f"__iter{nest_level}"]
        elif cmd_info["type"] == "if":
            return play_if(cmd_info)
        else:
            raise ValueError("Unknown command!")

    @classmethod
    def play(cls, desc_path):
        scenario_desc = ET.parse(desc_path).getroot()
        scenario = {}

        # MARK: data
        data_node = scenario_desc.find("data")
        scenario["data"] = cls._parse_data(data_node)

        # MARK: parameters
        param_node = scenario_desc.find("parameters")
        if param_node is not None:
            scenario["data"]["param"] = cls._parse_parameters(param_node)

        # MARK: instructions
        instr_node = scenario_desc.find("commands")
        for cmd in list(instr_node):
            cls._play_cmd(cmd, scenario["data"])

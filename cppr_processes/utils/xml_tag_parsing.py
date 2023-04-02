
class XMLTagParser:
    @classmethod
    def parse(cls, xml_tag):
        if type(xml_tag) is str:
            return xml_tag

        cmd_type = xml_tag.tag
        if cmd_type in ["if", "condition", "then", "else", "cout", "login", "filename", "subject", "body", "receivers",
                        "insert", "remove"]:
            cmd_f_label, cmd_tag = None, None
        elif cmd_type == "string" and "obj" not in xml_tag.attrib:
            cmd_f_label, cmd_tag = "{}", ""
        else:
            cmd_f_label, cmd_tag = xml_tag.attrib["obj"].split("*")[0], "*".join(xml_tag.attrib["obj"].split("*")[1:])
        cmd_info = {"type": cmd_type,
                    "data_label": cmd_f_label,
                    "data_tag": cmd_tag,
                    "filter": []}
        for attr_name, attr_val in xml_tag.attrib.items():
            if attr_name == "obj":
                continue
            if attr_name == "filter":
                cmd_info["filter"] = cls._parse_filters(attr_val)
                continue
            cmd_info[attr_name] = str(attr_val)

        cmd_info["contents"] = cls._parse_contents(xml_tag)

        return cmd_info

    @classmethod
    def _parse_filters(cls, filt_string):
        def parse_filter_val(value):
            if value == "False":
                return False
            if value == "True":
                return True
            if value.isnumeric():
                # FIXME: are floats principally possible?
                return int(value)

            # MARK: BASIC BEHAVIOR
            if value is not None:
                return True
            return False

        filters = []
        for filt in filt_string.split("*"):
            if "{" in filt:
                filt_name, filt_param_str = filt.replace(" ", "").split("{")
            else:
                filt_name, filt_param_str = filt, ""
            if len(filt_param_str) == 0:
                filters += [filt_name]
            else:
                filt_params = {key_val_pair.split("=")[0]: parse_filter_val(key_val_pair.split("=")[1])
                               for key_val_pair in filt_param_str[:-1].split(",")}
                filters += [(filt_name, filt_params)]

        # print(filters)
        return filters

    @classmethod
    def _parse_contents(cls, xml_tag):
        if len(list(xml_tag)) == 0:
            if xml_tag.text is None or len(xml_tag.text.replace("\n", "").replace("\t", "")) == 0:
                return None
            return xml_tag.text

        return [cls.parse(el) for el in list(xml_tag)]

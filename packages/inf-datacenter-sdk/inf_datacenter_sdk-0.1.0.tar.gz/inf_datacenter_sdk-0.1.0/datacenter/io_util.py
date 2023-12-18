#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:zexiang
"""
import json
import os
import dill
import yaml


def read_file_by_extension(fn):
    if fn.endswith('.json'):
        with open(fn, encoding='utf-8') as file:
            data = json.load(file)
    elif fn.endswith('.jsonl'):
        data = read_jsonl_to_list(fn)
    elif fn.endswith('.yaml'):
        data = load_yaml_file(fn)
    else:
        # elif fn.endswith('.pkl') or fn.endswith('.pickle'):
        data = load_dill_obj(fn)
    return data


def write_file_by_extension(obj, fn):
    if fn.endswith('.json'):
        with open(fn, 'w', encoding='utf-8') as file:
            json.dump(obj, file)
    elif fn.endswith('.jsonl'):
        write_jsonl_to_file(obj, fn)
    elif fn.endswith('.yaml'):
        save_yaml_file(obj, fn)
    else:
        # elif fn.endswith('.pkl') or fn.endswith('.pickle'):
        dump_dill_obj(obj, fn)


def write_jsonl_to_file(obj_list, jsonl_fn):
    with open(jsonl_fn, 'w', encoding='utf-8') as file:
        for obj in obj_list:
            file.write(json.dumps(obj, ensure_ascii=False) + '\n')


def read_jsonl_to_list(jsonl_fn):
    with open(jsonl_fn, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file.readlines()]


def load_yaml_file(fn):
    if isinstance(fn, str):
        with open(fn, 'r', encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config
    else:
        return fn


def save_yaml_file(obj, fn):
    folder = os.path.dirname(fn)
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)
    with open(fn, 'w', encoding="utf-8") as file:
        yaml.dump(obj, file)
    return fn


def dump_dill_obj(obj, fn):
    with open(fn, 'wb') as file:
        dill.dump(obj, file)


def load_dill_obj(fn):
    with open(fn, 'rb') as file:
        return dill.load(file)

def check_file_exists(fn)->bool:
    if not os.path.exists(fn):
        return False
    return True

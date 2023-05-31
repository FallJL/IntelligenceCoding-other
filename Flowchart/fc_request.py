#!/usr/bin/python
#encoding=utf-8
import time
import base64
import io
import os
import sys
import uuid
from tempfile import TemporaryFile, NamedTemporaryFile

from flask import json, Flask, request, jsonify, send_file, render_template
from flask_cors import CORS

from Flowchart import get_fc_code_by_pyflowchart, get_code2flow, add_comment, gen_fc_from_comment

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/helloworld')
def hello_world():
    return 'Hello, World!'

@app.route('/python/project/', methods=['GET', 'POST'])
def hello():
    data = request.json
    print(data)
    print(type(data))
    if request.method == 'GET':
        return '[GET METHOD] your name is ' + request.args.get('name', 'unknown')
    else:
        return '[POST METHOD] your name is ' + request.form.get('name', 'unknown')

"""
生成程序流程图的接口
"""
@app.route('/python/submitCodeASTGraph', methods=['POST'])
def submitCodeASTGraph():
    if request.method == 'POST':
        subdata = request.json
        if subdata["content"]:
            if subdata["languageName"] == "PYTHON":  # only support python now
                if subdata["graphtype"] == "AST":
                    # TODO 需要解决：如果代码带有class（像力扣那样），则会出错，
                    #  但单纯的把第一行class Solution去掉，又会有缩进错误
                    ASTfc_code = get_fc_code_by_pyflowchart(subdata["content"])   # 注意：这里返回的是AST的代码，不是图！代码在前端解析为图
                    if not ASTfc_code:
                        result_dict = {
                            "success": False,
                            "information": "Nothing to parse. Check given code and field please."
                        }
                    else:
                        result_dict = {
                            "success": True,
                            "ASTfc_code": ASTfc_code
                        }
                    return result_dict
    else:
        result_dict = {
            "result_code": 2000,
            "param": "options"
        }
        return result_dict

""" 暂时弃用...
"""
cg_file = ""
@app.route('/python/submitCodecallGraph', methods=['POST'])
def submitCodecallGraph():
    if request.method == 'POST':
        subdata = request.json
        if subdata["content"]:
            if subdata["languageName"] == "PYTHON":  # only support python now
                if subdata["graphtype"] == "callGraph":
                    with NamedTemporaryFile('w+t', encoding='utf-8', prefix="callGraph_", suffix='.py') as f:
                        # 生成中间数据
                        f.write(subdata["content"])
                        global cg_file
                        cg_file = f.name
                        img_file = get_code2flow(cg_file)
                    if cg_file:
                        print("send_image "+cg_file+".png")
                        return send_file(img_file+".png")
    else:
        result_dict = {
            "result_code": 2000,
            "param": "options"
        }
        return result_dict


""" 暂时弃用...
生成流程图step1：加特殊的注释
"""
com_file= ""
@app.route('/python/submitCodeComment', methods=['POST'])
def submitCodeComment():
    print('在这里1')
    if request.method == 'POST':
        subdata = request.json
        print('在这里2')
        print(subdata)
        if subdata["content"]:
            if subdata["languageName"] == "PYTHON":  # only support python now
                if subdata["graphtype"] == "sum_code":
                    print('在这里3')
                    global com_file
                    com_file = "NCS_out/data/python/tmp/genCom_"+uuid.uuid4().hex+".py"
                    with open(com_file, 'w') as wf:
                        wf.writelines( subdata["content"] )
                    print('在这里4')
                    com_code, fun_sum, sum_line, func_name = add_comment(com_file, l="python")

                    print("-"*50)
                    print("com_code:")
                    print(com_code)
                    print("-" * 50)

                    # print("-" * 50)
                    # print("fun_sum:")
                    # print(fun_sum)
                    # print("-" * 50)
                    #
                    # print("-" * 50)
                    # print("sum_line:")
                    # print(sum_line)
                    # print("-" * 50)
                    #
                    # print("-" * 50)
                    # print("func_name:")
                    # print(func_name)
                    # print("-" * 50)

                    result_dict = {
                        "success": True,
                        "com_code": com_code,
                        "fun_sum": fun_sum,
                        "sum_line": sum_line,
                        "func_name": func_name,
                    }
                    return result_dict
    else:
        result_dict = {
            "result_code": 2000,
            "param": "options"
        }
        return result_dict


""" 暂时弃用...
生成流程图step2：根据特殊的注释，生成流程图
"""
fc_files = []
@app.route('/python/submitCodeFC', methods=['POST'])
def submitCodeFC():
    if request.method == 'POST':
        subdata = request.json
        if subdata["content"]:
            if subdata["languageName"] == "PYTHON":  # only support python now
                if subdata["graphtype"] == "FC":
                    global fccode_file
                    fccode_file = "NCS_out/data/python/tmp/FC_"+uuid.uuid4().hex+".py"
                    with open(fccode_file, 'w') as wf:
                        wf.writelines( subdata["content"] )
                    global fc_files
                    func_names,fc_files = gen_fc_from_comment(fccode_file)
                    if fc_files:
                        print(fc_files)
                        print('func_names[-1]:', func_names[-1])
                        print('fc_files[-1]:', fc_files[-1])
                        return send_file(fc_files[-1] + ".png")
                    # with NamedTemporaryFile('w+t', encoding='utf-8', prefix="FC_", suffix='.py') as f:
                    #     # 生成中间数据
                    #     f.write(subdata["content"])
                    #     global fc_file
                    #     fc_file = f.name
                    #     print("gen_fc_from_comment "+fc_file)
                    #     img_file = gen_fc_from_comment(fc_file)
                    #     if fc_file:
                    #         print("send_image "+img_file)
                    #         return send_file(img_file)
    else:
        result_dict = {
            "result_code": 2000,
            "param": "options"
        }
        return result_dict


""" 暂时弃用...
每个请求处理后，还要进行删除相关文件、图的操作，防止硬盘不够用
"""
@app.after_request
def after_request(response):
    if request.endpoint=="submitCodecallGraph" and request.method=="POST":
        global cg_file
        os.remove("code2flow_out"+cg_file+"_png.png")
        os.remove("code2flow_out"+cg_file+"_png.gv")
        print("delete_tmp_image "+cg_file)
    elif request.endpoint=="submitCodeComment" and request.method=="POST":
        global com_file
        os.remove(com_file)
        os.remove(com_file + ".code")
        print("delete_tmp_file "+com_file)
        print("delete_tmp_file " + com_file + ".code")
    # elif request.endpoint=="submitCodeFC" and request.method=="POST":
    #     global fc_files
    #     for i in fc_files:
    #         os.remove(i)
    #         os.remove(i + ".png")
    #         print("delete_tmp_image " + i)
    # todo 怎么删除这些流程图？
    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='127.0.0.1')
import json
import ast
import tokenize
import os

import intervaltree as intervaltree
from pyflowchart import Flowchart


# 识别函数区间：开始行号，结束行号
from python_flowChart_out import gen_flowchart


def _compute_interval(node):
    if hasattr(node, "lineno"):
        min_lineno = node.lineno
        max_lineno = node.lineno
    else:
        # not a func
        return False
    for node in ast.walk(node):
        if hasattr(node, "lineno"):
            min_lineno = min(min_lineno, node.lineno)
            max_lineno = max(max_lineno, node.lineno)
    return (min_lineno, max_lineno)


def parse_file(filename):
    with tokenize.open(filename) as f:
        return ast.parse(f.read(), filename=filename)


def file_to_tree(filename):
    parsed = parse_file(filename)
    tree = intervaltree.IntervalTree()
    for node in ast.walk(parsed):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start, end = _compute_interval(node)
            tree[start:end] = node
    return tree


# 识别函数和类
def get_func_class_from_file(filename):
    code_tree = file_to_tree(filename)
    # code_tree = file_to_tree(filename+".py")
    funcs_code = []
    classes_code = []
    for i in code_tree.items():
        if isinstance(i.data, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if hasattr(i.data, "name"):
                with open(filename, 'r') as fp:
                # with open(filename+".py", 'r') as fp:
                    lines = fp.readlines()
                    func_lines = lines[i.begin-1:i.end]
                # (func_name, func_lines)
                funcs_code.append((i.data.name,''.join(func_lines)))
        elif isinstance(i.data, (ast.ClassDef)):
            if hasattr(i.data, "name"):
                # with open(filename+".py", 'r') as fp:
                with open(filename, 'r') as fp:
                    lines = fp.readlines()
                    class_lines = lines[i.begin-1:i.end]
                # (class_name, class_lines)
                classes_code.append((i.data.name,''.join(class_lines)))
    return funcs_code,classes_code


filename = "sample"
with open(filename+".py") as fp:
    content = fp.read()
# print(content)


# code2flow函数调用
def get_code2flow(filename):
    # 生成函数调用图：out_png.png
    code2flow_png_cmd = "code2flow " + filename + " -o code2flow_out" + filename + "_png.png -q"
    # code2flow_png_cmd = "code2flow " + filename + ".py -o code2flow_out/" + filename + "_png.png -q"
    out = os.popen(code2flow_png_cmd)
    print(out.read())
    return "code2flow_out"+filename+"_png"

    # 生成函数调用json文件
    # code2flow_json_cmd = "code2flow " + filename + " -o code2flow_out/" + filename + "_json.json -q"
    # # code2flow_json_cmd = "code2flow " + filename + ".py -o code2flow_out/" + filename + "_json.json -q"
    # out = os.popen(code2flow_json_cmd)
    # print(out.read())
    # with open("code2flow_out/" + filename + "_json.json",'r') as load_f:
    #     load_dict = json.load(load_f)["graph"]
    #     # nodes: 调用函数
    #     nodes = load_dict["nodes"]
    #     nodes_num = len(nodes)
    #     names = []  # 函数名集合
    #     for i in nodes.items():
    #         print(i[1]["label"])  # 行号:函数名
    #         temp =  i[1]["label"].split(': ')
    #         names.append(temp[-1])
    #         # print(nodes[i]["uid"])
    #     # edges: 调用关系
    #     edges = load_dict["edges"]
    #     edges_num = len(edges)


# pyflowchart生成流程图（实际上只是代码，并不是真正意义上的图）
def get_fc_code_by_pyflowchart(content):
    field_ast = Flowchart.find_field_from_ast(ast.parse(content), "")
    if hasattr(field_ast, "body") and field_ast.body:
        fc = Flowchart.from_code(content)
        # output flowchart code
        fc_code = fc.flowchart()
        # with open("pyflowchart_out/"+filename+"_fc_code.flowchart",'w') as wf:
        #     wf.write(fc_code)
        return fc_code  # 注：这里只是代码，不是图！
    else:
        return False
    # 前端展示流程图
    # 参考：
    # https://github.com/sunziping2016/oak-tree-house/blob/master/packages/%40oak-tree-house/vuepress-plugin-diagrams/FlowchartDiagram.vue
    # http://flowchart.js.org
    # https://github.com/adrai/flowchart.js


# 行末添加注释
def add_comment_at_end(str_in,comment):
    temp = list(str_in)
    temp.insert(-1, comment)
    str_out = ''.join(temp)
    return str_out


# NeuralCodeSum 生成函数注释
def gen_codesum_by_NCS(filename, funcs_code, l="python"):
    # 模型文件：/NCS_out/model/code2jdoc.mdl
    # write code in /NCS_out/data/python/[filename].code
    code_lines = []
    names = []
    for i in funcs_code:
        names.append(i[0])
        lines = i[1]
        t_line = ''.join(lines.split('\t'))
        t_line = ''.join(t_line.split('\r'))
        t_line = ''.join(t_line.split('\n'))
        one_line = t_line+"\n"
        code_lines.append(one_line)
    names.append("CODE SUM")
    # whole code at last line
    with open(filename, 'r') as fp:
    # with open(filename+".py", 'r') as fp:
        file_lines = fp.read()
        t_line = ''.join(file_lines.split('\t'))
        t_line = ''.join(t_line.split('\r'))
        one_line = ''.join(t_line.split('\n'))
        code_lines.append(one_line)
    if len(code_lines) == len(funcs_code)+1:
        sum_num = len(code_lines)
        # with open("NCS_out/data/"+l+"/"+filename+".code", 'w') as wf:
        with open(filename+".code", 'w') as wf:
            wf.writelines(code_lines)
        # 生成摘要 /NCS_out/model/code2jdoc_beam.json
        # device = "-1" # cpu
        # gen_codesum_cmd = "bash NCS_out/scripts/generate.sh " + device + " code2jdoc " + filename + ".code"
        # out = os.popen(gen_codesum_cmd)
        # print(out.read())
        code_sums = {}
        with open("NCS_out/model/code2jdoc_beam.json",'r') as load_f:
            json_file = json.load(load_f)
        j = 0
        for i in range(sum_num):
            if names[i] in code_sums.keys():
                code_sums[names[i]+j.__str__()]=json_file[i.__str__()][0]
                j +=1
            code_sums[names[i]]=json_file[i.__str__()][0]
        return code_sums
    else:
        print("Unexpected lines num during writing .code file!")
        return False


# 函数头尾添加注释
def add_comment(filename, l="python"):
    COMMENTS = {'C': '/*',
                'python': '#'}
    REF_COMMENT = ['fc:startStop',
                   'fc:process',
                   'fc:ifBranch',
                   'fc:ifMacro',
                   'fc:else',
                   'fc:forLoop',
                   'fc:subFunc',
                   'fc:subRoutine',
                   'fc:interrupt',
                   'fc:middleware',
                   'fc:end',
                   'fc:return']
    parsed = parse_file(filename)
    # parsed = parse_file(filename+".py")
    sum = []
    sum_lineno = []
    func_name = []
    funcs_code, _ = get_func_class_from_file(filename)
    funcs_codesum = gen_codesum_by_NCS(filename, funcs_code,"python")
    # print("code_sum:", funcs_codesum["CODE SUM"])
    sum.append(funcs_codesum["CODE SUM"])
    sum_lineno.append(0)
    func_name.append("CODE SUM")
    # with open(filename+".py", 'r') as fp:
    with open(filename, 'r') as fp:
        lines = fp.readlines()
        for node in ast.walk(parsed):

            if isinstance(node, (ast.While, ast.For)):
                start, end = _compute_interval(node)
                t_line = ''.join(lines[start-1].split('\t'))
                t_line = ''.join(t_line.split('\r'))
                t_line = ''.join(t_line.split('\n'))
                lines[start-1] = add_comment_at_end(lines[start-1], " "+COMMENTS[l]+REF_COMMENT[5]+' "LOOP" ')
                lines[end-1] = add_comment_at_end(lines[end-1], "  "+COMMENTS[l]+REF_COMMENT[10]+' "LOOP END" ')
            elif isinstance(node, (ast.If)):
                start, end = _compute_interval(node)
                t_line = ''.join(lines[start-1].split('\t'))
                t_line = ''.join(t_line.split('\r'))
                t_line = ''.join(t_line.split('\n'))
                lines[start-1] = add_comment_at_end(lines[start-1], "  "+COMMENTS[l]+REF_COMMENT[2]+' "IF" ')
                lines[end-1] = add_comment_at_end(lines[end-1], "  "+COMMENTS[l]+REF_COMMENT[10]+' "IF END"')
                # todo: ifel else
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start, end = _compute_interval(node)
                # 首尾添加fc:startStop
                func_sum = funcs_codesum[node.name]
                lines[start-1] = add_comment_at_end(lines[start-1], "  "+COMMENTS[l]+REF_COMMENT[0]+' "FUNC ['+node.name+']: '+func_sum+'"')
                lines[end-1] = add_comment_at_end(lines[end-1], "  "+COMMENTS[l]+REF_COMMENT[0]+' FUNC ['+node.name+']: END')
                sum.append(func_sum)
                sum_lineno.append(start)
                func_name.append(node.name)
            elif isinstance(node, (ast.ClassDef)):
                start, end = _compute_interval(node)
                t_line = ''.join(lines[start-1].split('\t'))
                t_line = ''.join(t_line.split('\r'))
                t_line = ''.join(t_line.split('\n'))
                lines[start-1] = add_comment_at_end(lines[start-1], '  '+COMMENTS[l]+REF_COMMENT[0]+' CLASS ['+node.name+']')
                lines[end-1] = add_comment_at_end(lines[end-1], '  '+COMMENTS[l]+REF_COMMENT[0]+' CLASS ['+node.name+'] END')
            else:
                continue
        lines_comment = ''.join(lines)
    # with open("python-flowChart_out/"+filename+"_comment.py", 'w') as wf:
    #     wf.writelines( lines_comment )
    return lines_comment, sum, sum_lineno, func_name


# 注释生成流程图
def gen_fc_from_comment(filename):
    # env_cmd = "source activate IC"
    # out = os.popen(env_cmd)
    # print(out.read())
    # gen_flowChart_with_comment_cmd = "python python_flowChart_out/gen_flowchart.py -s python_flowChart_out/" + filename + "_comment.py " \
    #                                             "-d python-flowChart_out/out " \
    #                                             "-l python"
    # gen_flowChart_with_comment_cmd = "python python_flowChart_out/gen_flowchart.py " \
    #                                  "-s " + filename + " "\
    #                                  "-d python_flowChart_out/out " \
    #                                  "-l python"

    filenames,filepaths = gen_flowchart.main(filename, "python-flowChart_out/out", "python")
    # out = os.popen(gen_flowChart_with_comment_cmd)
    # print(out.read())
    return filenames,filepaths


# add_comment(filename)


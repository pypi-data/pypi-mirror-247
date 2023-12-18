from gxl_ai_utils.utils import utils_data


def do_test_namespaceObj():
    """"""
    dic = {'a': 1, 'b': 2}
    namespaceObj = utils_data.do_dict2simpleNamespaceObj(dic)
    print(namespaceObj.a)
    print(namespaceObj.b)
    # print(namespaceObj.c)
    namespaceObj.a = 'gxl'
    print(namespaceObj.a)


if __name__ == '__main__':
    do_test_namespaceObj()

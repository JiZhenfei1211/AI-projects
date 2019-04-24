import matplotlib.pyplot as plt

decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plot_node(node_text, centerPt, parentPt, node_type):
    create_plot.ax1.annotate(node_text, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                             textcoords='axes fraction',
                             va='center', ha='center', bbox=node_type, arrowprops=arrow_args)


def create_plot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plot_tree.totalW = float(get_leaf_nums(inTree))
    plot_tree.totalD = float(get_depth(inTree))
    plot_tree.xOff = -0.5 / plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(inTree, (0.5, 1.0), '')
    plt.savefig('tree.png')
    plt.show()


def get_leaf_nums(decTree):
    num_leaf = 0
    first_str = list(decTree.keys())[0]
    second_dict = decTree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            num_leaf += get_leaf_nums(second_dict[key])
        else:
            num_leaf += 1
    return num_leaf


def get_depth(decTree):
    max_depth = 0
    first_str = list(decTree.keys())[0]
    second_dict = decTree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            depth = 1 + get_depth(second_dict[key])
        else:
            depth = 1
        if depth > max_depth:
            max_depth = depth
    return max_depth


def plot_mid_text(cenPt, parentPt, txtString):
    """Plots text between child and parent"""
    xMid = (parentPt[0] - cenPt[0]) / 2 + cenPt[0]
    yMid = (parentPt[1] - cenPt[1]) / 2 + cenPt[1]
    create_plot.ax1.text(xMid, yMid, txtString)


def plot_tree(decTree, parentPt, nodeTxt):
    num_leaf = get_leaf_nums(decTree)
    first_str = list(decTree.keys())[0]
    cenPt = (plot_tree.xOff + (1.0 + float(num_leaf)) / 2.0 / plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(cenPt, parentPt, nodeTxt)
    plot_node(first_str, cenPt, parentPt, decision_node)
    second_dict = decTree[first_str]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            plot_tree(second_dict[key], cenPt, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff), cenPt, leaf_node)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cenPt, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD


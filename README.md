由于作者的Python水平有限，本程序不应该被视为使用Python的样本。它要示范的，是怎样写一个自我验证的程序。这包括一个随机输入数据产生器（MakeData），以及一个结果验证器（CheckResult)。

这个Python程序，含对以下问题的一个解。

问题：从30个单位调来100名考官，每个单位不超过5人，其中有20名女考官，每个单位最多有1名女考官。将这些考官分成20个小组，每组5个人。一共两天，分上午和下午，安排四场面试，每场面试的考官要重新分组。现要求：每一场面试的分组中，每一个小组，任何两个女考官不能相遇，同单位的人不能相遇，以前在一个小组的人不能重新相遇。写一个满足以上条件的分组算法。

为了剥离原问题的文化背景，在程序中用豆子(beans)表示考官，红豆(redBeans)表示女考官。桶(buckets)对应考官的单位。用柜子(chests)代表小组。

算法：将柜子编号为0到19，每个柜子有从低到高的5层抽屉（0层到4层），每个抽屉中放一颗豆子，柜子里各层抽屉中豆子的集合为一个小组。首先把20个红豆放在20个柜子各自的0层抽屉里，然后随机拿出一桶豆子，第一个放在0号柜子里最下边仍然空着的抽屉里（1层抽屉），下一个豆子放在1号柜子的最下面的空抽屉中，如此，直到这一桶豆子放完，然后放下一桶，一桶放完再放一桶，桶的次序不重要。如果一桶豆子放到第19号，也就是最后一个柜子还没有放完，就开始使用0号柜子的上一层抽屉。显然，这个分配方案满足设定条件.

怎样产生其他三个半天的分组方案：对20个柜子中同样层高的抽屉进行向右循环平移，第0层的抽屉移动0次（不动），第1层的抽屉移动1次，如此类推，产生第二个半天的分组。其余两个半天的分组方案也用同样方法产生。

下面是对平移的正确性讨论：

1. 很容易看到，平移后的分组满足”以前在一个小组的人不能重新相遇“的条件。
2. 如果在第一次分组时，每一桶的豆子都被放在相同层高的抽屉里，那么平移时，不会让同单位的人相遇。
3. 假设有一桶的豆子被放在不同层高的抽屉里了，那么它们是在相邻的两层，第n和n+1层的抽屉里。在第n层，它们在编号最大的几个柜子里（比如18，19），在n+1层，它们在编号最小的几个柜子里（比如1，2，3）。它们之间有15个柜子中没有来自这一桶的豆子，15就是它们的安全距离。由于在为下一个半天求解的平移中，这相邻两层的相对位移是1，所以可以平移15次，也就是15次重新分组，仍能不使同单位的人相遇。

讨论完毕。






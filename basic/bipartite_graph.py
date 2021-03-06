from bitarray import bitarray
import networkx as nx
import matplotlib.pyplot as plt

from basic.customer import Customer


class BipartiteGraph:
    """
    某一个时点，需要被分单的所有用户，从业务上讲，这些用户都是可以被重新分配资方的.
    """

    def __init__(self, customer_list, num_funder):
        self.customer_list = customer_list
        self.num_rows = len(customer_list)
        self.num_columns = num_funder
        self.customers_map = {}  # 用户id与用户变量编码的对应关系
        self.reverse_customers_map = {}  # 用户变量编码与用户结构体关系
        self.funders_map = {}  # 资方id与资方变量编码的对应关系
        self.reverse_funders_map = {}  # 资方变量编码和资方结构体的对应关系

        size = self.num_rows * self.num_columns
        if size > 0:
            self.bitmap = bitarray(size)
        else:
            self.bitmap = bitarray()

        self.bitmap.setall(0)

        if customer_list is None:
            raise Exception("initialize failed.")
        self._build_map()

    def _build_map(self):
        if self.customer_list is None:
            return

        c_coder = 0
        f_coder = 0

        for customer in self.customer_list:
            if not isinstance(customer, Customer):
                return False

            if customer.id not in self.customers_map:
                self.customers_map[customer.id] = c_coder  # 用户id -> 变量编码
                self.reverse_customers_map[c_coder] = customer  # 变量编码 -> 用户结构体
                c_coder += 1

            for funder in customer.funders:
                if funder.id not in self.funders_map:
                    self.funders_map[funder.id] = f_coder  # 资方id -> 变量编码
                    self.reverse_funders_map[f_coder] = funder  # 变量编码 -> 资方结构体
                    f_coder += 1

                self.bitmap[self.num_columns * self.customers_map[customer.id] + self.funders_map[funder.id]] = 1

        if c_coder != self.num_rows - 1 or f_coder != self.num_columns - 1:
            return False

        return True

    # 前提条件：每日无新增资方，新增用户按照顺序自增
    def add_customer(self, customer):
        self.bitmap.extend([0] * self.num_columns)
        if customer.id not in self.customers_map:
            self.customers_map[customer.id] = self.num_rows  # 用户id -> 变量编码
            self.reverse_customers_map[self.num_rows] = customer  # 变量编码 -> 用户id
            self.num_rows += 1

        for funder in customer.funders:
            if funder.id not in self.funders_map:
                return False

            self.bitmap[self.num_columns * self.customers_map[customer.id] + self.funders_map[funder.id]] = 1

        return True

    # 只删除关系，不改变编码
    def remove_customer(self, customer_id):
        if customer_id not in self.customers_map:
            print("customer {0} is not exist.".format(customer_id))
            return False
        else:
            customer = self.reverse_customers_map[self.customers_map[customer_id]]
            for funder in customer.funders:
                if funder.id not in self.funders_map:
                    continue

                self.bitmap[self.num_columns * self.customers_map[customer.id] + self.funders_map[funder.id]] = 0

        return True

    def print_graph(self):
        self.print_graph_base(lambda i, j: self.bitmap[self.num_columns * i + j])

    def print_graph_base(self, _condition, node_size=5000, font_size=30):
        plt.figure(figsize=(66, 66))
        bi_map = nx.Graph()

        bi_map.add_nodes_from(list(range(self.num_rows)), bipartite=0, color='red')
        bi_map.add_nodes_from([str(item) for item in list(range(self.num_columns))], bipartite=1)
        eds = []
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if _condition(i, j):
                    eds.append((i, str(j)))
        bi_map.add_edges_from(eds)
        # Separate by group
        l, r = nx.bipartite.sets(bi_map)
        pos = {}
        # Update position for node from each group
        pos.update((node, (1, index)) for index, node in enumerate(l))
        pos.update((node, (2, index)) for index, node in enumerate(r))
        nx.draw(bi_map, pos=pos, nodelist=list(range(self.num_rows)), node_color='r', node_size=node_size,
                with_labels=True, font_size=font_size, font_color='white')
        nx.draw(bi_map, pos=pos, nodelist=[str(item) for item in list(range(self.num_columns))], node_color='b',
                node_size=node_size, with_labels=True, font_size=font_size, font_color='white')

        plt.show()

        return eds

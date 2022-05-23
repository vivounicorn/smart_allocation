import math

from ortools.sat.python import cp_model

from basic.bipartite_graph import BipartiteGraph
from basic.db_op import build_funders_data, build_customers_data

PRECISION = 10000  # 所有小数转换为整数，转换精度为保留小数点后5位
UNIT = 10000  # 所有涉及钱的都换算到单位：万


class CpModelOptimizer:
    def __init__(self, cfg):
        self.config = cfg
        self.funders_map = build_funders_data(cfg)
        self.customer_list, self.funders_customers_map = build_customers_data(self.funders_map, cfg)

        self.bp = BipartiteGraph(self.customer_list, len(self.funders_map))
        self.model = cp_model.CpModel()
        self.xi, self.xj, self.bt, self.variables, _ = self.__build_variables()

    def __build_variables(self):
        variables = []
        xi = {}
        xj = {}
        bt = {}

        for i in range(self.bp.num_rows):  # 真正变量是last_idx之后的每日新增用户.
            for j in range(self.bp.num_columns):
                if self.bp.bitmap[self.bp.num_columns * i + j]:
                    v = (self.model.NewIntVar(0, 1, 'x{0}{1}'.format(i, j)), i, j)
                    variables.append(v)
                    if i not in xi:
                        xi[i] = [v]
                    else:
                        xi[i].append(v)

                    if j not in xj:
                        xj[j] = [v]
                    else:
                        xj[j].append(v)

                    bus_t = self.bp.reverse_customer_map[i].t
                    if bus_t not in bt:
                        bt[bus_t] = [v]
                    else:
                        bt[bus_t].append(v)

        return xi, xj, bt, variables, len(variables)

    def __make_objective_function(self):
        # Create the objection function.
        obj = []
        for i in self.xi:
            for xij in self.xi[i]:
                cus = self.bp.reverse_customer_map[xij[1]]
                fun = self.bp.reverse_funder_map[xij[2]]
                obj.append(xij[0] * cus.m * (cus.e() - cus.pd * cus.lgd - fun.c))

        self.model.Maximize(sum(item for item in obj))
        print('The definition of optimization problem:')
        print('--------------------------------------')
        print('max ', sum(item for item in obj))
        print('s.t.')

    def __make_constraint_a(self):
        # Creates the constraints.
        # 构造约束条件:a.
        for j in self.xj:
            a_xij = self.xj[j]
            a_sumj = sum(x[0] * math.floor(self.bp.reverse_customer_map[x[1]].m / UNIT * PRECISION) for x in a_xij)
            smooth = sum(self.bp.reverse_customer_map[x[1]].m for x in a_xij) / UNIT
            smooth = smooth / self.bp.reverse_funder_map[j].s / UNIT - 1

            smooth = math.floor((1 - math.exp(smooth)) * self.bp.reverse_funder_map[j].s * UNIT * PRECISION)

            self.model.AddLinearConstraint(a_sumj, 0, smooth)
            print('    0≤', a_sumj, '≤', smooth, '      (a.)')

    def __make_constraint_b(self):
        # 构造约束条件:b.
        b_sumij = sum(v[0] for v in self.variables)
        for j in self.xj:
            b_xij = self.xj[j]
            b_sumj = sum(x[0] for x in b_xij)
            d = self.bp.reverse_funder_map[j].d * self.bp.reverse_funder_map[j].p / sum(
                self.bp.reverse_funder_map[i].p for i in self.bp.reverse_funder_map)
            dsum = sum(
                self.bp.reverse_funder_map[i].d * self.bp.reverse_funder_map[i].p / sum(
                    self.bp.reverse_funder_map[j].p for j in self.bp.reverse_funder_map) for i in
                self.bp.reverse_funder_map)

            # 托底资方不受限制，其他资方尽量按照通过率及比例要求分配.
            if self.bp.reverse_funder_map[j].is_base:
                ex = (b_sumj - b_sumij) * PRECISION
            else:
                ex = b_sumj * PRECISION - b_sumij * math.floor(d / dsum * PRECISION + 1)

            self.model.AddLinearConstraint(ex, cp_model.INT_MIN, 0)
            print('   ', ex, '≤', 0, '      (b.)')

    def __make_constraint_c(self):
        # 构造约束条件:c.
        t_sumij = sum(v[0] * math.floor(self.bp.reverse_customer_map[v[1]].m / UNIT) for v in self.variables)
        for i in self.bt:
            t_xij = self.bt[i]  # 某个业务类型对应的变量列表.
            td = self.config.biz_items[i]  # 该业务类型订单量占比.
            t_sum = sum(x[0] * math.floor(self.bp.reverse_customer_map[x[1]].m / UNIT) for x in t_xij)
            td_ex = (t_sum * PRECISION - t_sumij * math.floor(td * PRECISION))
            self.model.AddLinearConstraint(td_ex, cp_model.INT_MIN, 0)
            print('   ', td_ex, '≤', 0, '      (c.)')

    def __make_constraint_d(self):
        # 构造约束条件:funders.
        for j in self.xj:
            d_xij = self.xj[j]
            d_sum = sum(x[0] * math.floor(self.bp.reverse_customer_map[x[1]].p_score) for x in d_xij)
            d_ex = d_sum - len(d_xij) * math.floor(self.bp.reverse_funder_map[j].d_score)
            self.model.AddLinearConstraint(d_ex, cp_model.INT_MIN, 0)
            print('   ', d_ex, '≤', 0, '      (d.)')

    def __make_constraint_e(self):
        # 构造约束条件:funders.
        for j in self.xj:
            d_xij = self.xj[j]
            pctr = self.bp.reverse_funder_map[j].alpha / (self.bp.reverse_funder_map[j].alpha +
                                                          self.bp.reverse_funder_map[j].beta)
            n = len(d_xij)
            lamb = n / (n + self.bp.reverse_funder_map[j].alpha + self.bp.reverse_funder_map[j].beta)
            d_sum = sum(x[0] * math.floor(self.bp.reverse_customer_map[x[1]].pd * lamb * PRECISION) for x in d_xij) + \
                    math.floor(pctr * n * (1 - lamb) * PRECISION) - math.floor(
                self.bp.reverse_funder_map[j].dr * n * PRECISION)

            # self.model.AddLinearConstraint(d_sum, cp_model.INT_MIN, 0)
            print('   ', d_sum, '≤', 0, '      (e.)')

    def __make_constraint_h(self):
        # 构造约束条件:h.
        for i in self.xi:
            h_xij = self.xi[i]
            h_sum = sum(x[0] for x in h_xij)

            self.model.AddLinearConstraint(h_sum, 1, 1)

            print('   ', h_sum, "= 1", '      (h.)')

    def build_problem(self):
        self.__make_objective_function()
        self.__make_constraint_a()
        self.__make_constraint_b()
        self.__make_constraint_c()
        self.__make_constraint_d()
        self.__make_constraint_e()
        self.__make_constraint_h()

        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print('--------------------------------------')
            print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
            for v in self.variables:
                print(f'{v[0].Name}={solver.Value(v[0])}')
        else:
            print('No solution found.')

        # Statistics.
        print('\nStatistics')
        print(f'  status   : {solver.StatusName(status)}')
        print(f'  conflicts: {solver.NumConflicts()}')
        print(f'  branches : {solver.NumBranches()}')
        print(f'  wall time: {solver.WallTime()} s')

        if status == cp_model.OPTIMAL:
            ij_map = {}
            for v in self.variables:
                if solver.Value(v[0]) == 1:
                    ij_map[(v[1], v[2])] = 1

            self.bp.print_graph()
            self.bp.print_graph_base(lambda i, j: (i, j) in ij_map)

        if status == cp_model.INFEASIBLE:
            for var_index in solver.ResponseProto().sufficient_assumptions_for_infeasibility:
                print(var_index, self.model.VarIndexToVarProto(var_index))  # prints "v1"

        return solver

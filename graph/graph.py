#!/usr/bin/python
# Implementacao de grafo em linguagem python
# Autoria: William Oliveira de Lagos

from collections import deque

class Graph:
    def __init__(self):
        self.max = 0
        self.matadj = [[]]
        self.marked = []
    
    def create_nodes(self,n):
        """ 
         * Cria um grafo com nodes 1..n, sem arestas.
         *
         * @param n 
        """
        if n <= 0: raise Exception("Numero de nodos invalido!")
        self.max += n
        self.matadj = [[0 for i in range(self.max)] for i in range(self.max)]
        self.marked = [0 for i in range(self.max)]
    
    def create_graph(self,g):
        i = 1; j = 1; self.max = g.max
        self.matadj = [[0 for i in range(self.max)] for i in range(self.max)]
        while(i < self.max):
            while(j < self.max):
                self.matadj[i][j] = g.matadj[i][j]
                i += 1; j += 1
        self.marked = [0 for i in range(self.max)]
        
    def add_edge(self,orig,dest,weight=-1):
        """
         * Conecta dois nodes com uma aresta direcionada ou nao direcionada ponderada.
         * 
         * @param orig
         * @param dest
        """
        if orig > self.max or orig < 1 or dest > self.max or dest < 1:
            raise Exception("Aresta invalida, orig: %i dest: %i" %(orig,dest))
        elif weight < 0: self.matadj[orig][dest] = 1
        else:           
            self.matadj[orig][dest] = weight
            self.matadj[dest][orig] = weight

    def remove_edge(self,node):
        i = 1
        while(i < len(self.matadj[node])):
            self.matadj[node][i] = 0
            i += 1

    def show(self):
        """
         * Mostra as arestas do grafo.
         * 
        """
        print self.max - 1
        i = 1; j = 1
        while(i < self.max):
            while(j < self.max):
                if self.matadj[i][j] != 0: 
                    print "%d %d\n" % (i,j)
                i += 1; j += 1

    def clear_visited(self):
        i = 1
        while(i < self.max):
            self.marked[i] = False
            i += 1

    def adjacents(self,node):
        """
         * Calcula os adjacentes do node <code>node</code>.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: " + node)
        adj = []; i = 0
        while(i < len(self.matadj[node])):
            if self.matadj[node][i] != 0: adj.append(i)
            i += 1
        return adj

    def breadth(self,node):
        """
         * Retorna um representacao em texto do percurso em largura a partir do node
         * <code>node</code>.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: " + node)
        self.clear_visited()
        q = deque([]); q.append(node)
        visits = []; visits.append(node)
        self.marked[node] = True
        while(len(q) is not 0):
            n = q.popleft()
            for m in self.adjacents(n):
                if m not in self.marked:
                    visits.append(m)
                    q.append(m)
                    self.marked[m] = True
        return visits

    def depth(self,node):
        """
         * Retorna uma representacao em texto do percurso em profundidade a partir
         * do node <code>node</code>.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: %i" % node)
        self.clear_visited()
        visits = []; u = 1
        while(u < self.max):
            if u not in self.marked: self.recursive_depth(visits,u)
            u += 1
        return visits

    def recursive_depth(self,visits,node):
        visits.append(node)
        self.marked[node] = True
        for m in self.adjacents(node):
            if m not in self.marked: self.recursive_depth(visits,m)

    def stack_depth(self,node):
        """
         * 
         * @param node
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: %i" % node)
        # FIXME: n = m parece nao funcionar com o iterador e foreach
        # FIXME: n = m parece nao permitir retomar a construcao da pilha
        self.clear_visited()
        s,visits = [],[]
        s.append(node)
        visits.append(node)
        self.marked[node] = True
        while(len(s) is not 0):
            n = s.pop()
            for m in self.adjacents(n):
                if m not in self.marked:
                    visits.append(m)
                    s.append(m)
                    self.marked[m] = True
                    n = m
        return visits

    def entry_grade(self,node):
        """
         * Calcula o grau de entrada do node <code>node</code>.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: %i" % node)
        c = 0; i = 1
        while(i < len(self.matadj[node])):
            if self.matadj[i][node] != 0: c += 1
            i += 1
        return c

    def exit_grade(self,node):
        """
         * Calcula o grau de saida do node <code>node</code>.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: %i" % node)
#        c = 0; i = 1
#        while(i < len(self.matadj[node])
#            if self.matadj[node][i] != 0: c += 1
#            i += 1
#        return c
        return len(self.adjacents(node))

    def grade(self,node):        
        """
         * Calcula o grau do node <code>node</code>.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: %i" % node)

        return self.entry_grade(node) + self.exit_grade(node)
    

    def font(self,node):
        """
         * Determima se o node <code>node</code> e uma fonte.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: %i" % node)
        return self.entry_grade(node) == 0 and self.exit_grade(node) > 0

    def out(self,node):
        """
         * Determima se o node <code>node</code> e uma fonte.
         * 
         * @param node
         * 
         * @return
        """
        if node > self.max or node < 1:
            raise Exception("Nodo invalido: %i" % node)
        return self.entry_grade(node) > 0 and self.exit_grade(node) == 0

    def occupy_path(self,p):
        # TODO: Implementar a ocupacao de caminhos
        pass

    def search_path(self,font,out):
        # TODO: Implementar a busca por caminhos
        pass

    def top_sort(self):
        """
         * 
         * @return
        """
        cpy = Graph(self)
        l,candidate = [],[]
        for i in range(self.max): candidate.append(i)
        while(len(candidate) > 0):
            changed = False
            for i in range(candidate.size()):
                c = candidate[i]
                if cpy.entry_grade(c) is 0:
                    changed = True
                    l.append(c)
                    cpy.remove_edge(c)
                    del candidate[i]
            if not changed:
                raise Exception("Problema de ciclo")
        return l
#
#
#    public int[] prim(Integer node) {
#        int key[] = new int[self.max]
#        int pred[] = new int[self.max]
#
#        # TODO: Implementar conforme Prim: p.509, Cormem et al.
#        for (int i = 0 i < key.length i++) {
#            key[i] = Integer.self.max_VALUE
#        }
#        key[0] = 0
#        key[node] = 0
#        pred[node] = -1
#
#        List<Integer> candidatos = new ArrayList<Integer>()
#
#        for (int i = 1 i < self.max i++) {
#            candidatos.add(i)
#        }
#        int u
#        while (!candidatos.isEmpty()) {
#            u = extractMin(candidatos, key)
#            for (Integer v : adjacentes(u)) {
#                if (candidatos.contains(v) && self.matadj[u][v] < key[v]) {
#                    pred[v] = u
#                    key[v] = self.matadj[u][v]
#                }
#            }
#        }
#
#        for (int i = 0 i < key.length i++) {
#            // System.out.printf("%4d", key[i])
#            //System.out.printf("%4d", pred[i])
#        }
#        //System.out.println()
#
#        return pred
#    }
#
#    public static int extractMin(List<Integer> candidatos, int[] key) {#!/usr/bin/python
#        if (candidatos.isEmpty()) {
#            throw new IllegalArgumentException()
#        }
#        Integer menor = candidatos.get(0)
#        for (Integer c : candidatos) {
#            if (key[c] < key[menor]) {
#                menor = c
#                //System.out.println(c)
#            }
#        }
#        candidatos.remove(menor)
#        return menor
#    }
#
#    public int[] dijkstra(Integer node) {
#        // 1o. passo: iniciam-se os valores:
#        int key[] = new int[self.max]
#        int pred[] = new int[self.max]
#        for (int i = 0 i < key.length i++) {
#            key[i] = Integer.self.max_VALUE/2
#            pred[i] = -1
#        }
#        key[0] = 0
#        key[node] = 0
#        List<Integer> candidatos = new ArrayList<Integer>()
#        for (int i = 1 i < self.max i++) {
#            candidatos.add(i)
#        }
#        int u
#        while (!candidatos.isEmpty()) {
#            u = extractMin(candidatos, key)
#            for (Integer v : adjacentes(u)) {
#                if (key[u] + self.matadj[u][v] < key[v]) {
#                    key[v] = key[u] + self.matadj[u][v]
#                    pred[v] = u
#                }
#            }
#        }
#        return key
#    }
#    
#    public int[][] floydWarshall() {
#        int d[][] = new int[self.max][self.max]
#        # TODO: Implementar Floyd-Warshall
#        return d
#    }    
#    
#    public int[][] fordFulkerson(int fonte, int sumidouro) {
#        int u[][] = new int[self.max][self.max]
#        for (int i = 0 i < u.length i++) {
#            for (int j = 0 j < u[i].length j++) {
#                u[i][j] = 0
#            }
#        }
#        int p[]
#        while ((p = encontrarCaminho(fonte, sumidouro)) != null) {
#            ocuparCaminho(p)
#        }
#        return u
#    }
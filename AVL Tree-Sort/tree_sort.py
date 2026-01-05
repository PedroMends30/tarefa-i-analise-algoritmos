import time
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.sorted_list = []
        self.comparisons = 0
        self.rotations = 0

    def reset(self):
        self.root = None
        self.sorted_list = []
        self.comparisons = 0
        self.rotations = 0

    def height(self, node):
        return node.height if node else 0

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotate_right(self, y):
        self.rotations += 1
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x

    def rotate_left(self, x):
        self.rotations += 1
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def insert(self, node, key):
        if node is None:
            return Node(key)

        self.comparisons += 1
        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            self.comparisons += 1
            node.right = self.insert(node.right, key)
        else:
            self.comparisons += 1
            node.right = self.insert(node.right, key)

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        balance = self.balance_factor(node)

        if balance > 1:
            if self.balance_factor(node.left) >= 0:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.balance_factor(node.right) <= 0:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def inorder(self, node):
        if node:
            self.inorder(node.left)
            self.sorted_list.append(node.key)
            self.inorder(node.right)

    def tree_sort(self, arr: List[int]) -> List[int]:
        self.reset()
        for key in arr:
            self.root = self.insert(self.root, key)
        self.inorder(self.root)
        return self.sorted_list


class BenchmarkSuite:
    def __init__(self, seed=42):
        random.seed(seed)
        self.results = []

    def generate_test_cases(self, size: int) -> Dict[str, List[int]]:
        return {
            "Aleatório": [random.randint(0, size * 10) for _ in range(size)],
            "Ordenado": list(range(size)),
            "Decrescente": list(range(size, 0, -1)),
            "Parcialmente Ordenado": self._partial(size),
            "Muitas Duplicatas": [random.randint(0, size // 10) for _ in range(size)],
            "Quase Ordenado": self._almost(size)
        }

    def _partial(self, size):
        arr = list(range(size))
        for _ in range(size // 3):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    def _almost(self, size):
        arr = list(range(size))
        for i in range(0, size - 1, 10):
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
        return arr

    def run_single_test(self, arr):
        avl = AVLTree()
        start = time.perf_counter()
        avl.tree_sort(arr)
        end = time.perf_counter()

        height = avl.root.height if avl.root else 0

        return (
            end - start,
            avl.comparisons,
            avl.rotations,
            height
        )

    def run_benchmark(self, sizes, runs=5):
        for size in sizes:
            for name, arr in self.generate_test_cases(size).items():
                times, comps, rots, heights = [], [], [], []

                for _ in range(runs):
                    t, c, r, h = self.run_single_test(arr)
                    times.append(t)
                    comps.append(c)
                    rots.append(r)
                    heights.append(h)

                self.results.append({
                    "size": size,
                    "case": name,
                    "avg_time": np.mean(times),
                    "avg_comparisons": np.mean(comps),
                    "avg_rotations": np.mean(rots),
                    "avg_height": np.mean(heights)
                })

        self.plot()

    def plot(self):
        cases = sorted(set(r["case"] for r in self.results))

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        ax_time, ax_height = axes

        # -------- Tempo --------
        for case in cases:
            data = [r for r in self.results if r["case"] == case]
            data.sort(key=lambda x: x["size"])

            n = [r["size"] for r in data]
            time_ms = [r["avg_time"] * 1000 for r in data]

            ax_time.plot(n, time_ms, marker="o", linewidth=2, label=case)

        ax_time.set_title("Tempo de execução — AVL Tree Sort")
        ax_time.set_xlabel("Tamanho da entrada (n)")
        ax_time.set_ylabel("Tempo médio (ms)")
        ax_time.grid(alpha=0.3)
        ax_time.legend(title="Entrada")

        # -------- Altura --------
        for case in cases:
            data = [r for r in self.results if r["case"] == case]
            data.sort(key=lambda x: x["size"])

            n = [r["size"] for r in data]
            heights = [r["avg_height"] for r in data]

            ax_height.plot(n, heights, marker="s", linewidth=2, label=case)

        ax_height.set_title("Altura final da árvore AVL")
        ax_height.set_xlabel("Tamanho da entrada (n)")
        ax_height.set_ylabel("Altura")
        ax_height.grid(alpha=0.3)
        ax_height.legend(title="Entrada")

        plt.tight_layout()
        plt.show()
        self.print_table()


    def theoretical_height(self, n):
        return 1.44 * np.log2(n + 2)


    def build_table(self):
        table = []

        for r in self.results:
            n = r["size"]
            h_theoretical = self.theoretical_height(n)

            table.append({
                "n": n,
                "case": r["case"],
                "time_ms": r["avg_time"] * 1000,
                "height_measured": r["avg_height"],
                "height_theoretical": h_theoretical,
                "ratio": r["avg_height"] / h_theoretical
            })

        return table


    def print_table(self):
        table = self.build_table()

        header = (
            f"{'n':>6} | {'Caso':>20} | {'Tempo (ms)':>10} | "
            f"{'Altura Medida':>14} | {'Altura Teórica':>15} | {'Razão':>6}"
        )
        print(header)
        print("-" * len(header))

        for row in table:
            print(
                f"{row['n']:6d} | "
                f"{row['case']:20} | "
                f"{row['time_ms']:10.3f} | "
                f"{row['height_measured']:14.2f} | "
                f"{row['height_theoretical']:15.2f} | "
                f"{row['ratio']:6.3f}"
            )


benchmark = BenchmarkSuite(seed=123)
benchmark.run_benchmark(
    sizes=[100, 500, 1000, 2000, 5000, 7000],
    runs=5
)

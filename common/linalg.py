from fractions import Fraction
from math import ceil
from typing import TypeAlias

Matrix: TypeAlias = list[list[Fraction]]


class LinearSystem:
    """
    Represents and solves a system of non-negative integer ax=b
    """

    def __init__(self, a: list[list[int]], b: list[int]):
        self.a = a
        self.b = b
        self.rows = len(b)
        self.cols = len(a[0]) if self.rows > 0 else 0
        self.re_matrix, self.re_pivots = self._row_echelon_form()

    def _row_echelon_form(self) -> tuple[Matrix, dict[int, int]]:
        # Make equation matrix
        matrix: Matrix = [
            [*(Fraction(c, 1) for c in self.a[i]), Fraction(self.b[i], 1)]
            for i in range(self.rows)
        ]

        # Gaussian Elimination to RE form
        i_pivot = 0
        pivots: dict[int, int] = {}  # j -> i of pivot

        for j in range(self.cols):
            if i_pivot >= self.rows:
                break

            # Find pivot
            j_pivot = -1
            for i in range(i_pivot, self.rows):
                if matrix[i][j] != 0:
                    j_pivot = i
                    break
            if j_pivot == -1:
                continue

            # Swap
            matrix[i_pivot], matrix[j_pivot] = matrix[j_pivot], matrix[i_pivot]

            # Normalize
            pivot_val = matrix[i_pivot][j]
            for j_hat in range(j, self.cols + 1):
                matrix[i_pivot][j_hat] /= pivot_val

            # Eliminate
            for i in range(self.rows):
                if i != i_pivot and matrix[i][j] != 0:
                    factor = matrix[i][j]
                    for j_hat in range(j, self.cols + 1):
                        matrix[i][j_hat] -= factor * matrix[i_pivot][j_hat]

            pivots[j] = i_pivot
            i_pivot += 1

        return matrix, pivots

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.a}, {self.b})"

    def is_full_rank(self) -> bool:
        M = self.re_matrix
        for r in range(self.rows):
            all_zeros = all(M[r][c] == 0 for c in range(self.cols))
            if all_zeros and M[r][-1] != 0:
                return False
        return True

    def solve(self) -> tuple[int, ...]:
        """
        Solve the system minimizing sum(x).
        """

        if not self.is_full_rank():
            return ()

        M = self.re_matrix
        P = self.re_pivots  # Maps j -> i
        free_cols = tuple(set(range(self.cols)) - set(P))

        x_min = None
        sum_x_min = float("inf")

        def set_free_vars(idx: int, assigned_free_vars: dict[int, int]) -> None:
            nonlocal sum_x_min, x_min

            sx = sum(assigned_free_vars.values())
            if sx >= sum_x_min:
                return  # Prune, we won't do better than x_min this time

            if idx == len(free_cols):
                # All free vars fixed -> What is the solution?
                # Use assigned vars
                x = [assigned_free_vars.get(j, 0) for j in range(self.cols)]

                # Back substitute to pivots
                for j, i in P.items():
                    xj_f = M[i][-1] - sum(
                        M[i][j_right] * x[j_right]
                        for j_right in range(j + 1, self.cols)
                    )

                    if xj_f.denominator != 1 or xj_f < 0:
                        return  # Bunk result
                    x[j] = int(xj_f)

                sum_x = sum(x)
                if sum_x < sum_x_min:
                    sum_x_min = sum_x
                    x_min = tuple(x)
                return

            # Determine bounds for the current free variable
            j_free = free_cols[idx]

            # Default bounds
            min_val = 0
            max_val = 50000  # Big Enough™

            # Cost Analysis: Does increasing this variable increase total presses?
            # Total = sum(free) + sum(pivots)
            # pivot_i = b_i - k * free_j
            # Cost_coeff = 1 - sum(coeffs of free_j in all pivot rows)
            cost_coeff = Fraction(1, 1)

            # Constraints from pivot rows to tighten min/max
            # x_p + A_curr * x_curr + sum(A_fut * x_fut) = b_eff
            # => x_p = b_eff - A_curr * x_curr - sum(A_fut * x_fut) >= 0

            for i in P.values():
                coeff = M[i][j_free]
                b_i = M[i][-1]

                # Update cost coefficient
                cost_coeff -= coeff

                # Calculate effective constant (Original - contribution of assigned free vars)
                b_eff = b_i
                for assigned_j, assigned_val in assigned_free_vars.items():
                    if assigned_j != j_free:
                        b_eff -= M[i][assigned_j] * assigned_val

                # Check Bounds won't break later
                # Future coeffs for this row are >= 0.
                all_future_non_negative = True
                for j_fut in range(idx + 1, len(free_cols)):
                    fc = free_cols[j_fut]
                    if M[i][fc] < 0:
                        all_future_non_negative = False
                        break

                if coeff > 0 and all_future_non_negative:
                    # x_curr <= b_eff / coeff
                    if b_eff < 0:
                        # Impossible since future terms (>=0) only subtract from b_eff
                        return
                    bound = int(b_eff / coeff)
                    max_val = min(max_val, bound)

                # Check 2: Lower Bound
                # If coeff < 0: x_pivot = b_eff + |coeff| * x_curr - sum(A_fut * x_fut) >= 0
                # |coeff| * x_curr >= sum(A_fut * x_fut) - b_eff
                # x_curr >= (sum(A_fut * x_fut) - b_eff) / |coeff|
                # We need min possible RHS.
                # Min of sum(A_fut * x_fut) is negative infinity if any A_fut < 0.
                # If all A_fut >= 0, min is 0.
                # So if all A_fut >= 0, x_curr >= -b_eff / |coeff|

                if coeff < 0 and all_future_non_negative:
                    needed = b_eff / coeff
                    min_val = max(min_val, ceil(needed))

            if min_val > max_val:
                return

            # Search from low cost to high
            if cost_coeff < 0:
                search_range = range(max_val, min_val - 1, -1)
            else:
                search_range = range(min_val, max_val + 1)

            for val in search_range:
                assigned_free_vars[j_free] = val
                set_free_vars(idx + 1, assigned_free_vars)
                if x_min is not None and cost_coeff >= 0 and idx == len(free_cols) - 1:
                    # On last free var we found a valid solution and cost is positive,
                    # we can stop early because cost will only increase
                    return
                del assigned_free_vars[j_free]

        set_free_vars(0, {})
        return x_min or ()
